import random
import string
from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.config import settings
from app.models.ticket import Ticket
from app.models.movie import Movie
from app.models.staff import Staff
from app.services.qrcode_service import generate_qr_base64


def _gen_ticket_code() -> str:
    date_part = datetime.now().strftime('%Y%m%d')
    rand = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    return f'TK-{date_part}-{rand}'


class TicketService:
    @staticmethod
    def create(db: Session, data, issuer_id: int):
        movie = db.query(Movie).filter(Movie.id == data.movie_id).first()
        if not movie:
            raise ValueError('电影不存在')
        today = date.today()
        if movie.start_date > today or movie.end_date < today:
            raise ValueError('电影不在有效期内')
        if not movie.is_active:
            raise ValueError('电影已下架')

        code = _gen_ticket_code()
        t = Ticket(
            ticket_code=code,
            movie_id=data.movie_id,
            phone=data.phone.strip(),
            quantity=max(1, min(10, data.quantity)),
            status='unused',
            issuer_id=issuer_id
        )
        db.add(t)
        db.commit()
        db.refresh(t)

        qr_base64 = generate_qr_base64(code)
        return {
            'id': t.id,
            'ticket_code': code,
            'movie_name': movie.name,
            'phone': t.phone,
            'quantity': t.quantity,
            'end_date': str(movie.end_date),
            'qr_base64': qr_base64,
            'issued_at': t.issued_at.strftime('%Y-%m-%d %H:%M')
        }

    @staticmethod
    def check_unused(db: Session, movie_id: int, phone: str) -> dict:
        count = db.query(Ticket).filter(
            Ticket.movie_id == movie_id,
            Ticket.phone == phone,
            Ticket.status == 'unused'
        ).count()
        return {'has_unused': count > 0, 'count': count}

    @staticmethod
    def get_detail(db: Session, ticket_id: int, user: Staff) -> dict:
        t = db.query(Ticket).filter(Ticket.id == ticket_id).first()
        if not t:
            raise ValueError('票务不存在')
        if user.role != 'admin' and t.issuer_id != user.id and t.checker_id != user.id:
            raise ValueError('无权查看')
        movie = db.query(Movie).filter(Movie.id == t.movie_id).first()
        issuer = db.query(Staff).filter(Staff.id == t.issuer_id).first()
        checker = db.query(Staff).filter(Staff.id == t.checker_id).first() if t.checker_id else None
        qr_base64 = generate_qr_base64(t.ticket_code)
        result = {
            'id': t.id,
            'ticket_code': t.ticket_code,
            'movie_name': movie.name if movie else '',
            'phone': t.phone,
            'quantity': t.quantity,
            'status': t.status,
            'issued_at': t.issued_at.strftime('%Y-%m-%d %H:%M') if t.issued_at else '',
            'issuer_name': issuer.name if issuer and user.role == 'admin' else None,
            'end_date': str(movie.end_date) if movie else '',
            'qr_base64': qr_base64
        }
        if t.status == 'used':
            result['checked_at'] = t.checked_at.strftime('%Y-%m-%d %H:%M') if t.checked_at else ''
            result['checker_name'] = checker.name if checker and user.role == 'admin' else None
        return result

    @staticmethod
    def get_issue_history(db: Session, user: Staff, page: int, page_size: int, movie_id: int | None, status: str | None):
        q = db.query(Ticket).join(Movie, Ticket.movie_id == Movie.id)
        if user.role != 'admin':
            q = q.filter(Ticket.issuer_id == user.id)
        if movie_id:
            q = q.filter(Ticket.movie_id == movie_id)
        if status:
            q = q.filter(Ticket.status == status)
        q = q.order_by(Ticket.issued_at.desc())
        total = q.count()
        items = q.offset((page - 1) * page_size).limit(page_size).all()

        result = []
        for t in items:
            movie = db.query(Movie).filter(Movie.id == t.movie_id).first()
            issuer = db.query(Staff).filter(Staff.id == t.issuer_id).first()
            result.append({
                'id': t.id,
                'movie_name': movie.name if movie else '',
                'phone': t.phone,
                'quantity': t.quantity,
                'issued_at': t.issued_at.strftime('%Y-%m-%d %H:%M') if t.issued_at else '',
                'status': t.status,
                'issuer_name': issuer.name if issuer and user.role == 'admin' else None
            })
        return {'total': total, 'items': result}

    @staticmethod
    def void(db: Session, id: int, user_id: int):
        t = db.query(Ticket).filter(Ticket.id == id).first()
        if not t:
            raise ValueError('票务不存在')
        if t.status != 'unused':
            raise ValueError('只能作废未核销的票')
        t.status = 'voided'
        t.voided_by = user_id
        t.voided_at = datetime.now(ZoneInfo(settings.TIMEZONE)).replace(tzinfo=None)
        db.commit()

    @staticmethod
    def verify(db: Session, ticket_code: str, checker_id: int):
        t = db.query(Ticket).filter(Ticket.ticket_code == ticket_code).first()
        if not t:
            return {'success': False, 'title': '无效二维码', 'details': [{'key': '提示', 'val': '确认是否为正确票务码'}]}

        movie = db.query(Movie).filter(Movie.id == t.movie_id).first()
        today = date.today()

        if t.status == 'used':
            checker = db.query(Staff).filter(Staff.id == t.checker_id).first()
            return {
                'success': False,
                'title': '重复核销',
                'details': [
                    {'key': '已核销时间', 'val': t.checked_at.strftime('%Y-%m-%d %H:%M') if t.checked_at else ''},
                    {'key': '核销人', 'val': checker.name if checker else ''}
                ]
            }

        if t.status == 'voided':
            return {'success': False, 'title': '票已作废', 'details': [{'key': '提示', 'val': '请联系出票工作人员'}]}

        if movie and movie.end_date < today:
            return {
                'success': False,
                'title': '票已过期',
                'details': [
                    {'key': '电影', 'val': movie.name},
                    {'key': '有效期至', 'val': str(movie.end_date)}
                ]
            }

        t.status = 'used'
        t.checker_id = checker_id
        t.checked_at = datetime.now(ZoneInfo(settings.TIMEZONE)).replace(tzinfo=None)
        db.commit()

        phone_masked = t.phone[:3] + '****' + t.phone[-4:] if len(t.phone) == 11 else t.phone
        return {
            'success': True,
            'title': '核销成功',
            'details': [
                {'key': '电影', 'val': movie.name if movie else ''},
                {'key': '手机', 'val': phone_masked},
                {'key': '张数', 'val': str(t.quantity)},
                {'key': '出票时间', 'val': t.issued_at.strftime('%m-%d %H:%M') if t.issued_at else ''}
            ]
        }

    @staticmethod
    def get_check_history(db: Session, user: Staff, page: int, page_size: int, movie_id: int | None,
                         start_date: date | None = None, end_date: date | None = None):
        q = db.query(Ticket).filter(Ticket.status == 'used')
        if user.role != 'admin':
            q = q.filter(Ticket.checker_id == user.id)
        if movie_id:
            q = q.filter(Ticket.movie_id == movie_id)
        if start_date:
            q = q.filter(func.date(Ticket.checked_at) >= start_date)
        if end_date:
            q = q.filter(func.date(Ticket.checked_at) <= end_date)
        q = q.order_by(Ticket.checked_at.desc())
        items = q.offset((page - 1) * page_size).limit(page_size).all()
        result = []
        for t in items:
            movie = db.query(Movie).filter(Movie.id == t.movie_id).first()
            checker = db.query(Staff).filter(Staff.id == t.checker_id).first()
            result.append({
                'id': t.id,
                'movie_name': movie.name if movie else '',
                'phone': t.phone,
                'quantity': t.quantity,
                'checked_at': t.checked_at.strftime('%Y-%m-%d %H:%M') if t.checked_at else '',
                'checker_name': checker.name if checker and user.role == 'admin' else None
            })
        return {'total': len(result), 'items': result}

    @staticmethod
    def get_today_stats(db: Session, user_id: int):
        tz = ZoneInfo(settings.TIMEZONE)
        now = datetime.now(tz)
        today = now.date()
        start = datetime.combine(today, datetime.min.time())
        end = datetime.combine(today, datetime.max.time())

        issued = db.query(Ticket).filter(Ticket.issuer_id == user_id, Ticket.issued_at >= start, Ticket.issued_at <= end).count()
        checked = db.query(Ticket).filter(Ticket.checker_id == user_id, Ticket.checked_at >= start, Ticket.checked_at <= end).count()
        return {'issued_today': issued, 'checked_today': checked}
