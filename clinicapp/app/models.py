from datetime import date, datetime, timedelta
from random import choice, randint
from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, DATE, Enum
# from sqlalchemy.orm import relationship
from datetime import date

from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, DATE, Enum, DateTime
from enum import Enum as DonViEnum

from sqlalchemy.orm import relationship

from clinicapp.app import app, db
from flask_login import UserMixin
from datetime import datetime


class NguoiDung(db.Model):
    __table_args__ = {"extend_existing": True}
    __abstract__ = True
    hoTen = Column(String(50), nullable=False)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(50), nullable=False)
    gioiTinh = Column(Boolean)
    ngaySinh = Column(DATE)
    cccd = Column(String(12), unique=True)
    diaChi = Column(String(100))
    sdt = Column(String(10), unique=True)
    avatar = Column(String(100),
                    default='https://res.cloudinary.com/dwivkhh8t/image/upload/v1732798321/male_fqyusr.png')


class BenhNhan(NguoiDung, UserMixin):
    __table_args__ = {"extend_existing": True}
    __tablename__ = 'benhnhan'
    idBenhNhan = Column(Integer, primary_key=True, autoincrement=True)

    def get_id(self):
        return (self.idBenhNhan)


class Comment(db.Model):
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True, autoincrement=True)
    content = Column(String(255), nullable=False)
    user_id = Column(Integer, ForeignKey(BenhNhan.idBenhNhan), nullable=False)
    created_date = Column(DateTime, default=datetime.now())

    user = relationship('BenhNhan', backref='comments', lazy=True)


class NhanVien(NguoiDung, UserMixin):
    __table_args__ = {"extend_existing": True}
    idNhanVien = Column(Integer, primary_key=True, autoincrement=True)
    bangCap = Column(String(50), default="Cử Nhân")
    ngayVaoLam = Column(DATE)

    def get_id(self):
        return (self.idNhanVien)


class YTa(NhanVien):
    __table_args__ = {"extend_existing": True}
    idYTa = Column(Integer, ForeignKey(NhanVien.idNhanVien), nullable=False, primary_key=True)

    def get_id(self):
        return (self.idYTa)


class BacSi(NhanVien):
    __table_args__ = {"extend_existing": True}
    idBacSi = Column(Integer, ForeignKey(NhanVien.idNhanVien), nullable=False, primary_key=True)
    chuyenKhoa = Column(String(50))

    def get_id(self):
        return (self.idBacSi)


class ThuNgan(NhanVien):
    __table_args__ = {"extend_existing": True}
    idThuNgan = Column(Integer, ForeignKey(NhanVien.idNhanVien), nullable=False, primary_key=True)

    def get_id(self):
        return (self.idThuNgan)


class QuanTri(NhanVien):
    __table_args__ = {"extend_existing": True}
    idQuanTri = Column(Integer, ForeignKey(NhanVien.idNhanVien), nullable=False, primary_key=True)
    phongBan = Column(String(50))

    def get_id(self):
        return (self.idQuanTri)


class HoSoBenhNhan(db.Model):
    __table_args__ = {'extend_existing': True}
    idHoSo = Column(Integer, primary_key=True, autoincrement=True)
    ngayTao = Column(DATE)
    tinhTrang = Column(String(50))
    id_benhnhan = Column(Integer, ForeignKey(BenhNhan.idBenhNhan), nullable=False)
    benhnhan = db.relationship('BenhNhan', backref='hosobenhnhan')

class LichKham(db.Model):
    __table_args__ = {'extend_existing': True}
    idLichKham = Column(Integer, primary_key=True, autoincrement=True)
    ngayDangKy = Column(DATE)
    ngayKham = Column(DATE)
    id_benhnhan = Column(Integer, ForeignKey(BenhNhan.idBenhNhan), nullable=False)
    id_yta = Column(Integer, ForeignKey(YTa.idYTa), nullable=True)

    yta = db.relationship('YTa', backref='lichkhams', lazy=True)
    benhnhan = db.relationship('BenhNhan', backref='lichkhams')


class DonVi(DonViEnum):
    VIEN = 1
    CHAI = 2
    VY = 3

    def readable(cls, value):
        mapping = {
            cls.VIEN: "Viên",
            cls.CHAI: "Chai",
            cls.VY: "Vỉ"
        }
        return mapping.get(value, "Không xác định")


class Thuoc(db.Model):
    __table_args__ = {'extend_existing': True}
    idThuoc = Column(Integer, primary_key=True, autoincrement=True)
    tenThuoc = Column(String(50))
    loaiThuoc = Column(Enum(DonVi), default=DonVi.VIEN)
    huongDanSuDung = Column(String(100))


class HoaDon(db.Model):
    __table_args__ = {'extend_existing': True}
    idHoaDon = Column(Integer, primary_key=True, autoincrement=True)
    ngayKham = Column(DATE)
    tienKham = Column(Float)
    tienThuoc = Column(Float)
    id_thungan = Column(Integer, ForeignKey(ThuNgan.idThuNgan), nullable=False)


class PhieuKham(db.Model):
    __table_args__ = {'extend_existing': True}
    idPhieuKham = Column(Integer, primary_key=True, autoincrement=True)
    ngayTao = Column(DATE)
    trieuChung = Column(String(50))
    chanDoan = Column(String(50))
    # loiKhuyen = Column(String(50))
    id_benhnhan = Column(Integer, ForeignKey(BenhNhan.idBenhNhan), nullable=False)
    id_bacsi = Column(Integer, ForeignKey(BacSi.idBacSi), nullable=False)
    id_hoadon = Column(Integer, ForeignKey(HoaDon.idHoaDon))

    bacsi = db.relationship('BacSi', backref='phieukham')


class ChiTietDonThuoc(db.Model):
    __table_args__ = {'extend_existing': True}
    id_phieukham = Column(Integer, ForeignKey(PhieuKham.idPhieuKham), primary_key=True)
    id_thuoc = Column(Integer, ForeignKey(Thuoc.idThuoc), primary_key=True)
    soLuongThuoc = Column(Integer)
    phieukham = db.relationship('PhieuKham', backref=db.backref('thuocs', lazy='dynamic'))
    thuoc = db.relationship('Thuoc', backref=db.backref('phieukham', lazy='dynamic'))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()

        import hashlib
        # benh_nhan = BenhNhan(
        #     hoTen="Nguyễn Văn A",
        #     username="nguyenvana",
        #     password=str(hashlib.md5('123456'.encode('utf-8')).hexdigest()),
        #     gioiTinh=True,  # True cho nam, False cho nữ
        #     ngaySinh=date(1990, 1, 1),
        #     cccd="123456789012",
        #     diaChi="Hà Nội",
        #     sdt="0123456789",
        # )
        #
        # # Thêm vào cơ sở dữ liệu và commit
        # db.session.add(benh_nhan)
        # db.session.commit()
        #
        # yta = YTa(
        #     bangCap="Trung cấp Y tế",
        #     ngayVaoLam="2020-03-01",
        #     hoTen="Tran To B",
        #     username="yta_tob",
        #     password=str(hashlib.md5('123456'.encode('utf-8')).hexdigest()),
        #     gioiTinh=False,
        #     ngaySinh="1995-05-12",
        #     cccd="095256781812",
        #     diaChi="123 Đường ABC, Quận 1",
        #     sdt="0987654441",
        # )
        #
        # db.session.add(yta)
        # db.session.commit()
        #
        # bac_si = BacSi(
        #     ngayVaoLam="2015-06-01",
        #     bangCap="Bác sĩ chuyên khoa I",
        #     hoTen="Nguyen Van A",
        #     username="bacsi_a",
        #     password=str(hashlib.md5('123456'.encode('utf-8')).hexdigest()),
        #     gioiTinh=True,
        #     ngaySinh="1985-01-15",
        #     cccd="123456788011",
        #     diaChi="456 Đường XYZ, Quận 2",
        #     sdt="0912345678",
        #     chuyenKhoa="Nội tiết",
        # )
        #
        # db.session.add(bac_si)
        # db.session.commit()
        #
        # thu_ngan = ThuNgan(
        #     ngayVaoLam="2021-06-01",
        #     bangCap="Cử Nhân",
        #     hoTen="Nguyen Tuyet B",
        #     username="thungan_a",
        #     password=str(hashlib.md5('123456'.encode('utf-8')).hexdigest()),
        #     gioiTinh=False,
        #     ngaySinh="2001-01-15",
        #     cccd="100056788011",
        #     diaChi="456 Đường XYZ, Quận 10",
        #     sdt="0912333668",
        # )
        #
        # db.session.add(thu_ngan)
        # db.session.commit()
        #
        quan_tri = QuanTri(
            ngayVaoLam="2019-11-01",
            bangCap="Cử Nhân",
            hoTen="Nguyen Duc A",
            username="quantri_quanab",
            password=str(hashlib.md5('123456'.encode('utf-8')).hexdigest()),
            gioiTinh=True,
            ngaySinh="1999-11-16",
            cccd="111054779911",
            diaChi="Nguyễn Văn Linh, Quận 7",
            sdt="0992243168",
            phongBan="PB_IT"
        )

        db.session.add(quan_tri)
        db.session.commit()
        #
        # quan_tri = QuanTri(
        #     ngayVaoLam="2019-11-01",
        #     bangCap="Cử Nhân",
        #     hoTen="Ngo Duc Ken",
        #     username="quantri_kend",
        #     password=str(hashlib.md5('123456'.encode('utf-8')).hexdigest()),
        #     gioiTinh=True,
        #     ngaySinh="1999-11-16",
        #     cccd="095250177891",
        #     diaChi="Nguyễn Văn Linh, Quận 7",
        #     sdt="0992444468",
        #     phongBan="PB_IT"
        # )
        #
        # db.session.add(quan_tri)
        # db.session.commit()
        #
        # thuoc1 = Thuoc(
        #     tenThuoc="Paracetamol",
        #     loaiThuoc=DonVi.VIEN,
        #     huongDanSuDung="Uống 1 viên mỗi 6 giờ"
        # )
        #
        # thuoc2 = Thuoc(
        #     tenThuoc="Vitamin C",
        #     loaiThuoc=DonVi.VIEN,
        #     huongDanSuDung="Uống 1 viên mỗi ngày"
        # )
        #
        # thuoc3 = Thuoc(
        #     tenThuoc="Amoxicillin",
        #     loaiThuoc=DonVi.CHAI,
        #     huongDanSuDung="Uống 10ml mỗi 8 giờ"
        # )
        #
        # thuoc4 = Thuoc(
        #     tenThuoc="Cefuroxime",
        #     loaiThuoc=DonVi.VY,
        #     huongDanSuDung="Tiêm 2 mũi mỗi ngày"
        # )
        #
        # db.session.add_all([thuoc1, thuoc2, thuoc3, thuoc4])
        # db.session.commit()
        #
        # hoa_don1 = HoaDon(
        #     ngayKham="2024-12-01",
        #     tienKham=500000,
        #     tienThuoc=200000,
        #     id_thungan=5
        # )
        #
        # hoa_don2 = HoaDon(
        #     ngayKham="2024-12-02",
        #     tienKham=700000,
        #     tienThuoc=300000,
        #     id_thungan=5
        # )
        #
        # hoa_don3 = HoaDon(
        #     ngayKham="2024-12-03",
        #     tienKham=400000,
        #     tienThuoc=150000,
        #     id_thungan=5
        # )
        #
        # db.session.add_all([hoa_don1, hoa_don2, hoa_don3])
        # db.session.commit()

        # chi_tiet1 = ChiTietDonThuoc(
        #     id_phieukham=1,
        #     id_thuoc=1,
        #     soLuongThuoc=10
        # )
        #
        # chi_tiet2 = ChiTietDonThuoc(
        #     id_phieukham=2,
        #     id_thuoc=2,
        #     soLuongThuoc=5
        # )
        #
        # db.session.add_all([chi_tiet1, chi_tiet2])
        # db.session.commit()


