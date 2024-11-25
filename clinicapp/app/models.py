from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, DATE
from sqlalchemy.orm import relationship
from clinicapp.app import app, db

class BenhNhan(db.Model):
    idBenhNhan = Column(Integer, primary_key=True, autoincrement=True)
    hoTen = Column(String(50), nullable=False)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(50), nullable=False)
    gioiTinh = Column(Boolean)
    ngaySinh = Column(DATE)
    cccd = Column(String(12), unique=True)
    diaChi = Column(String(100))
    sdt = Column(String(10), unique=True)





