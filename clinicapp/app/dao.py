from datetime import datetime
from sqlalchemy import func
from clinicapp.app.models import BenhNhan, NhanVien, YTa, BacSi, ThuNgan, QuanTri, LichKham
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

    y_ta = YTa.query.filter(YTa.username.__eq__(username.strip()), YTa.password.__eq__(password)).first()
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
        db.session.commit()

    if thungan:
        thungan.hoTen = name
        thungan.gioiTinh = gioiTinh
        thungan.ngaySinh = ngaySinh
        thungan.cccd = cccd
        thungan.diaChi = diaChi
        thungan.sdt = sdt
        db.session.commit()


def update_lichkham(user_id, ngayDangKy, ngayKham=None, idYTa=None):
    if not user_id or not ngayDangKy:
        return {"status": "error", "message": "Thiếu thông tin bắt buộc."}

    try:
        user = BenhNhan.query.filter_by(idBenhNhan=user_id).first()

        if not user:
            return {"status": "error", "message": "Không tìm thấy bệnh nhân."}

        lichkham = LichKham(
            ngayDangKy=ngayDangKy,
            ngayKham=ngayKham,
            id_benhnhan=user.idBenhNhan,
            id_yta=idYTa,
        )
        db.session.add(lichkham)
        db.session.commit()

        return {"status": "success", "message": "Lich kham da duoc dang ky thanh cong."}
    except Exception as e:
        db.session.rollback()
        return {"status": "error", "message": f"Loi khi cap nhat lich kham: {str(e)}"}


def get_danhsach_lichkham(user_id):
    return LichKham.query.filter_by(id_benhnhan=user_id).all()


def get_ds_lichkham_relationship(user_id):
    return db.session.query(LichKham.idLichKham,
                            LichKham.ngayDangKy,
                            LichKham.ngayKham,
                            YTa.hoTen.label('yta_name')).join(YTa, LichKham.id_yta == YTa.idYTa, isouter=True).filter(LichKham.id_benhnhan == user_id).all()


def get_danhsach_lichkham_benhnhan():
    return db.session.query(
        LichKham.idLichKham,
        LichKham.ngayDangKy,
        LichKham.ngayKham,
        BenhNhan.hoTen.label('benhnhan_name'),
        BenhNhan.gioiTinh.label('benhnhan_gioitinh'),
        func.date_format(BenhNhan.ngaySinh, '%d/%m/%Y').label('benhnhan_ngaysinh'),
        BenhNhan.diaChi.label('benhnhan_diachi')).join(BenhNhan, LichKham.id_benhnhan == BenhNhan.idBenhNhan).all()


def get_lichkham(lichkham_id):
    return LichKham.query.filter_by(idLichKham=lichkham_id).first()


def get_user(user_id):
    return BenhNhan.query.filter_by(idBenhNhan=user_id).first()


def get_current_yta_by_id(yta_id):
    return YTa.query.filter_by(idYTa=yta_id).first()


def yta_update_lichkham(lichkham_id, ngayKham, yta_id):
    try:
        lichkham = LichKham.query.filter_by(idLichKham=lichkham_id).first()
        if not lichkham:
            raise Exception("Không tìm thấy lịch khám với ID: {}".format(lichkham_id))
        lichkham.ngayKham = ngayKham
        lichkham.id_yta = yta_id
        db.session.commit()
        print(f"Lịch khám {lichkham_id} đã được cập nhật thành công!")

    except Exception as e:
        db.session.rollback()
        print(f"Lỗi khi cập nhật lịch khám: {e}")
        raise

