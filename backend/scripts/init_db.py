"""
初始化数据库：创建表结构 + 默认管理员账号
用法: python -m scripts.init_db
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.database import engine, Base
from app.models import Staff, Movie, Ticket
from app.core.security import hash_password


def init_db():
    Base.metadata.create_all(bind=engine)

    from sqlalchemy.orm import sessionmaker
    Session = sessionmaker(bind=engine)
    db = Session()

    # 若已有管理员则跳过
    admin = db.query(Staff).filter(Staff.username == 'admin').first()
    if not admin:
        admin = Staff(
            username='admin',
            password_hash=hash_password('admin123'),
            name='管理员',
            role='admin'
        )
        db.add(admin)
        db.commit()
        print('已创建默认管理员: admin / admin123')
    else:
        print('管理员已存在')

    db.close()
    print('数据库初始化完成')


if __name__ == '__main__':
    init_db()
