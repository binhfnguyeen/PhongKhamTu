from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, DATE
from sqlalchemy.orm import relationship
from clinicapp.app import app, db

class NguoiDung(db.Model):
    __abstract__ = True
    hoTen = Column(String(50), nullable=False)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(50), nullable=False)
    gioiTinh = Column(Boolean)
    ngaySinh = Column(DATE)
    cccd = Column(String(12), unique=True)
    diaChi = Column(String(100))
    sdt = Column(String(10), unique=True)

class BenhNhan(NguoiDung):
    idBenhNhan = Column(Integer, primary_key=True, autoincrement=True)


class NhanVien(NguoiDung):
    idNhanVien = Column(Integer, primary_key=True, autoincrement=True)
    bangCap = Column(String(50))
    ngayVaoLam = Column(DATE)


class YTa(NhanVien):
    idYTa = Column(Integer, ForeignKey(NhanVien.idNhanVien), nullable=False, primary_key=True)


class BacSi(NhanVien):
    idBacSi = Column(Integer, ForeignKey(NhanVien.idNhanVien), nullable=False, primary_key=True)
    chuyenKhoa = Column(String(50))


class ThuNgan(NhanVien):
    idThuNgan = Column(Integer, ForeignKey(NhanVien.idNhanVien), nullable=False, primary_key=True)


class QuanTri(NhanVien):
    idQuanTri = Column(Integer, ForeignKey(NhanVien.idNhanVien), nullable=False, primary_key=True)
    phongBan = Column(String(50))


class HoSoBenhNhan(db.Model):
    idHoSo = Column(Integer, primary_key=True, autoincrement=True)
    ngayTao = Column(DATE)
    tinhTrang = Column(String(50))
    id_benhnhan = Column(Integer, ForeignKey(BenhNhan.idBenhNhan), nullable=False)


class LichKham(db.Model):
    idLichKham = Column(Integer, primary_key=True, autoincrement=True)
    ngayDangKy = Column(DATE)
    ngayKham = Column(DATE)
    id_benhnhan = Column(Integer, ForeignKey(BenhNhan.idBenhNhan), nullable=False)
    id_yta = Column(Integer, ForeignKey(YTa.idYTa), nullable=False)

class Thuoc(db.Model):
    idThuoc = Column(Integer, primary_key=True, autoincrement=True)
    tenThuoc = Column(String(50))
    huongDanSuDung = Column(String(100))

class HoaDon(db.Model):
    idHoaDon = Column(Integer, primary_key=True, autoincrement=True)
    ngayKham = Column(DATE)
    tienKham = Column(Float)
    tienThuoc = Column(Float)
    id_thungan = Column(Integer, ForeignKey(ThuNgan.idThuNgan), nullable=False)


class PhieuKham(db.Model):
    idPhieuKham = Column(Integer, primary_key=True, autoincrement=True)
    ngayTao = Column(DATE)
    trieuChung = Column(String(50))
    chanDoan = Column(String(50))
    id_benhnhan = Column(Integer, ForeignKey(BenhNhan.idBenhNhan), nullable=False)
    id_bacsi = Column(Integer, ForeignKey(BacSi.idBacSi), nullable=False)
    id_hoadon = Column(Integer, ForeignKey(HoaDon.idHoaDon), nullable=False)


class ChiTietDonThuoc(db.Model):
    id_phieukham = Column(Integer, ForeignKey(PhieuKham.idPhieuKham), primary_key=True)
    id_thuoc = Column(Integer, ForeignKey(Thuoc.idThuoc), primary_key=True)
    soLuongThuoc = Column(Integer)

class DonViThuoc(db.Model):
    idDonViThuoc = Column(Integer, primary_key=True, autoincrement=True)
    donVi = Column(String(50))
    id_thuoc = Column(Integer, ForeignKey(Thuoc.idThuoc), nullable=False)


class LoaiThuoc(db.Model):
    idLoaiThuoc = Column(Integer, primary_key=True, autoincrement=True)
    tenLoaiThuoc = Column(String(50))


class DanhMucThuoc(db.Model):
    id_thuoc = Column(Integer, ForeignKey(Thuoc.idThuoc), primary_key=True)
    id_loaithuoc = Column(Integer, ForeignKey(LoaiThuoc.idLoaiThuoc), primary_key=True)
    giaThuoc = Column(Float)
    huongDanSuDung = Column(String(100))
    hamLuong = Column(Float)



if __name__ == '__main__':
    with app.app_context():
        db.create_all()
