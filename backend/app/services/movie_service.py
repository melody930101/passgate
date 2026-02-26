from datetime import date
from sqlalchemy.orm import Session

from app.models.movie import Movie


class MovieService:
    @staticmethod
    def get_active(db: Session):
        today = date.today()
        return db.query(Movie).filter(
            Movie.is_active == 1,
            Movie.start_date <= today,
            Movie.end_date >= today
        ).order_by(Movie.start_date.desc()).all()

    @staticmethod
    def get_all(db: Session):
        return db.query(Movie).order_by(Movie.created_at.desc()).all()

    @staticmethod
    def create(db: Session, data, created_by: int):
        m = Movie(
            name=data.name,
            start_date=data.start_date,
            end_date=data.end_date,
            price=data.price,
            remark=data.remark,
            is_active=1,
            created_by=created_by
        )
        db.add(m)
        db.commit()
        db.refresh(m)
        return m

    @staticmethod
    def update(db: Session, id: int, data):
        m = db.query(Movie).filter(Movie.id == id).first()
        if not m:
            raise ValueError('电影不存在')
        m.name = data.name
        m.start_date = data.start_date
        m.end_date = data.end_date
        m.price = data.price
        m.remark = data.remark
        db.commit()
        db.refresh(m)
        return m

    @staticmethod
    def deactivate(db: Session, id: int):
        m = db.query(Movie).filter(Movie.id == id).first()
        if not m:
            raise ValueError('电影不存在')
        m.is_active = 0
        db.commit()
