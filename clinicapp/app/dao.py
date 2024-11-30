from clinicapp.app.models import BenhNhan, NhanVien, YTa, BacSi, ThuNgan, QuanTri
from clinicapp.app import db, app
import hashlib
import cloudinary.uploader


def get_id_user(id):
    return BenhNhan.query.get(id)


def get_id_yta(id):
    return YTa.query.get(id)


def get_id_bacsi(id):
    return BacSi.query.get(id)


def get_id_thungan(id):
    return ThuNgan.query.get(id)


def auth_user(username, password):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())

    benh_nhan = BenhNhan.query.filter(BenhNhan.username.__eq__(username.strip()),BenhNhan.password.__eq__(password)).first()
    if benh_nhan:
        return benh_nhan

    y_ta = YTa.query.filter(YTa.username.__eq__(username.strip()),YTa.password.__eq__(password)).first()
    if y_ta:
        return y_ta

    bac_si = BacSi.query.filter(BacSi.username.__eq__(username.strip()),BacSi.password.__eq__(password)).first()
    if bac_si:
        return bac_si

    thu_ngan = ThuNgan.query.filter(ThuNgan.username.__eq__(username.strip()),ThuNgan.password.__eq__(password)).first()
    if thu_ngan:
        return thu_ngan

    return None


def add_user(name, username, password, avatar=None):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    u = BenhNhan(hoTen=name, username=username, password=password)

    if avatar:
        res = cloudinary.uploader.upload(avatar)
        u.avatar = res.get('secure_url')

    db.session.add(u)
    db.session.commit()


def update_profile(user_id, name, gioiTinh, ngaySinh, cccd, diaChi, sdt):
    user = BenhNhan.query.filter_by(idBenhNhan=user_id).first()
    yta = YTa.query.filter_by(idYTa=user_id).first()
    bacsi = BacSi.query.filter_by(idBacSi=user_id).first()
    thungan = ThuNgan.query.filter_by(idThuNgan=user_id).first()
    if user:
        user.hoTen = name
        user.gioiTinh = gioiTinh
        user.ngaySinh = ngaySinh
        user.cccd = cccd
        user.diaChi = diaChi
        user.sdt = sdt
        db.session.commit()

    if yta:
        yta.hoTen = name
        yta.gioiTinh = gioiTinh
        yta.ngaySinh = ngaySinh
        yta.cccd = cccd
        yta.diaChi = diaChi
        yta.sdt = sdt
        db.session.commit()

    if bacsi:
        bacsi.hoTen = name
        bacsi.gioiTinh = gioiTinh
        bacsi.ngaySinh = ngaySinh
        bacsi.cccd = cccd
        bacsi.diaChi = diaChi
        bacsi.sdt = sdt
        bacsi.session.commit()

    if thungan:
        thungan.hoTen = name
        thungan.gioiTinh = gioiTinh
        thungan.ngaySinh = ngaySinh
        thungan.cccd = cccd
        thungan.diaChi = diaChi
        thungan.sdt = sdt
        db.session.commit()