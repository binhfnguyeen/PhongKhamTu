from datetime import datetime
from sqlalchemy import func
from models import BenhNhan, NhanVien, YTa, BacSi, ThuNgan, QuanTri, LichKham, HoaDon, Thuoc, ChiTietDonThuoc, PhieuKham
from clinicapp.app import db, app
import hashlib
import cloudinary.uploader


def get_object_by_id(model, id):
    if not model or not id:
        return None

    return model.query.get(id)


def get_id_user(id):
    return get_object_by_id(BenhNhan, id)


def get_id_yta(id):
    return get_object_by_id(YTa, id)


def get_id_bacsi(id):
    return get_object_by_id(BacSi, id)


def get_id_thungan(id):
    return get_object_by_id(ThuNgan, id)


def get_id_quantri(id):
    return get_object_by_id(QuanTri, id)


def auth_user(username, password, role):
    password_hashed = hashlib.md5(password.strip().encode('utf-8')).hexdigest()

    model_map = {
        "benhnhan": BenhNhan,
        "yta": YTa,
        "bacsi": BacSi,
        "thungan": ThuNgan,
        "quantri": QuanTri
    }

    model = model_map.get(role)
    if model:
        return model.query.filter(model.username == username.strip(), model.password == password_hashed).first()
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


def tong_tienkham_theo_ngay_trong_thang(month, year):
    tong_tienkham = db.session.query(
        HoaDon.ngayKham,
        func.sum(HoaDon.tienKham).label('tong_tien_kham')
    ).filter(
        func.extract('month', HoaDon.ngayKham) == month,
        func.extract('year', HoaDon.ngayKham) == year
    ).group_by(HoaDon.ngayKham).all()

    result = [
        {
            'ngay_kham': hoa_don.ngayKham.strftime('%d-%m-%Y'),
            'tong_tien_kham': hoa_don.tong_tien_kham
        } for hoa_don in tong_tienkham
    ]

    return result


def tong_tienthuoc_theo_ngay_trong_thang(month, year):
    tong_tienthuoc = db.session.query(
        HoaDon.ngayKham,
        func.sum(HoaDon.tienThuoc).label('tong_tien_thuoc')
    ).filter(
        func.extract('month', HoaDon.ngayKham) == month,
        func.extract('year', HoaDon.ngayKham) == year
    ).group_by(HoaDon.ngayKham).all()

    result = [
        {
            'ngay_kham': hoa_don.ngayKham.strftime('%d-%m-%Y'),
            'tong_tien_thuoc': hoa_don.tong_tien_thuoc
        } for hoa_don in tong_tienthuoc
    ]

    return result


def tong_benhnhan_theo_ngay_trong_thang(month, year):
    tong_benhnhan = db.session.query(
        HoaDon.ngayKham,
        func.count(HoaDon.idHoaDon).label('so_benh_nhan')
    ).filter(
        func.extract('month', HoaDon.ngayKham) == month,
        func.extract('year', HoaDon.ngayKham) == year
    ).group_by(HoaDon.ngayKham).all()

    result = [
        {
            'ngay_kham': hoa_don.ngayKham.strftime('%d-%m-%Y'),
            'so_benh_nhan': hoa_don.so_benh_nhan
        } for hoa_don in tong_benhnhan
    ]

    return result


def thong_ke_theo_ngay(month, year):
    tien_kham = tong_tienkham_theo_ngay_trong_thang(month, year)
    tien_thuoc = tong_tienthuoc_theo_ngay_trong_thang(month, year)
    benh_nhan = tong_benhnhan_theo_ngay_trong_thang(month, year)

    report = []
    tong_doanh_thu = 0
    for ngay in tien_kham:
        ngay_kham = ngay['ngay_kham']
        tong_tien_kham = ngay['tong_tien_kham']
        tong_tien_thuoc = next((item['tong_tien_thuoc'] for item in tien_thuoc if item['ngay_kham'] == ngay_kham), 0)
        so_benh_nhan = next((item['so_benh_nhan'] for item in benh_nhan if item['ngay_kham'] == ngay_kham), 0)

        doanh_thu = tong_tien_kham + tong_tien_thuoc
        tong_doanh_thu += doanh_thu
        ty_le = (so_benh_nhan / doanh_thu) * 100 if doanh_thu != 0 else 0

        report.append({
            'ngay_kham': ngay_kham,
            'doanh_thu': f"{doanh_thu:,.0f}",
            'so_benh_nhan': so_benh_nhan,
            'tyle': round(ty_le, 2),
        })

    report.sort(key=lambda x: x['ngay_kham'])
    return report, f"{tong_doanh_thu:,.0f}"


def thong_ke_su_dung_thuoc_theo_ngay(month, year):
    try:
        results = db.session.query(
            Thuoc.tenThuoc,
            Thuoc.loaiThuoc.label("don_vi"),
            func.sum(ChiTietDonThuoc.soLuongThuoc).label("tong_so_luong"),
            func.count(ChiTietDonThuoc.id_thuoc).label("so_lan_dung")
        ).join(
            ChiTietDonThuoc, ChiTietDonThuoc.id_thuoc == Thuoc.idThuoc
        ).join(
            PhieuKham, ChiTietDonThuoc.id_phieukham == PhieuKham.idPhieuKham
        ).filter(
            func.extract("month", PhieuKham.ngayTao) == month,
            func.extract("year", PhieuKham.ngayTao) == year
        ).group_by(
            Thuoc.tenThuoc,
            Thuoc.loaiThuoc
        ).order_by(
            Thuoc.tenThuoc.asc()
        ).all()

        report = [
            {
                "ten_thuoc": r.tenThuoc,
                "don_vi": r.don_vi.name,
                "tong_so_luong": r.tong_so_luong,
                "so_lan_dung": r.so_lan_dung
            }
            for r in results
        ]

        return report
    except Exception as e:
        print(f"Lỗi khi thống kê sử dụng thuốc: {e}")
        return {"status": "error", "message": str(e)}