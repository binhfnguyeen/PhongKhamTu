from datetime import datetime, date
from sqlalchemy import func
from sqlalchemy.engine import row
from sqlalchemy.orm import joinedload, join, outerjoin

from clinicapp.app.models import BenhNhan, NhanVien, YTa, BacSi, ThuNgan, QuanTri, LichKham, Thuoc, HoSoBenhNhan, \
    PhieuKham, ChiTietDonThuoc, HoaDon, DonVi
from clinicapp.app import db, app
import hashlib
import cloudinary.uploader
from flask import session, flash, redirect, url_for, render_template, request
from enum import Enum


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

    benh_nhan = BenhNhan.query.filter(BenhNhan.username.__eq__(username.strip()),
                                      BenhNhan.password.__eq__(password)).first()
    if benh_nhan:
        return benh_nhan

    y_ta = YTa.query.filter(YTa.username.__eq__(username.strip()), YTa.password.__eq__(password)).first()
    if y_ta:
        return y_ta

    bac_si = BacSi.query.filter(BacSi.username.__eq__(username.strip()), BacSi.password.__eq__(password)).first()
    if bac_si:
        return bac_si

    thu_ngan = ThuNgan.query.filter(ThuNgan.username.__eq__(username.strip()),
                                    ThuNgan.password.__eq__(password)).first()
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
                            YTa.hoTen.label('yta_name')).join(YTa, LichKham.id_yta == YTa.idYTa, isouter=True).filter(
        LichKham.id_benhnhan == user_id).all()


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


# lập phiếu khám function

TINH_TRANG = {
    0: ["Chưa lưu",
        "btn-danger",
        "-danger"
        ],
    1: [
        "Lưu nháp",
        "btn-outline-secondary",
        "-muted",
    ],
    2: [
        "Đã lưu",
        "btn-outline-success",
        "-success"
    ]
}


def get_id_benhnhan(id):
    return BenhNhan.query.filter_by(idBenhNhan=id).first()


def get_LichKham_Today():
    today = date.today()
    try:
        lichkham_today = (
            db.session.query(LichKham)
            .options(joinedload(LichKham.benhnhan))  # Load quan hệ benhnhan
            .filter(LichKham.ngayKham == today)
            .all()
        )

        kq = []
        for i, row in enumerate(lichkham_today, start=1):
            if row.benhnhan:  # Kiểm tra nếu benhnhan không phải None
                kq.append({
                    'stt': i,
                    'id_lich': row.idLichKham,
                    'id_benhnhan': row.benhnhan.idBenhNhan,
                    'hoVaTen': row.benhnhan.hoTen,
                    'gioiTinh': row.benhnhan.gioiTinh,
                    'namSinh': row.benhnhan.ngaySinh.strftime("%d/%m/%Y"),
                    'diaChi': row.benhnhan.diaChi,
                    'ngayKham': row.ngayKham.strftime("%d/%m/%Y"),
                    'tinhTrang': 0  # Có thể thay bằng enum hoặc giá trị thực
                })

        kq.sort(key=lambda x: (x['tinhTrang'], x['stt']))
        print(kq)  # Debug, có thể loại bỏ trong production
        return kq
    except Exception as e:
        print(f"Lỗi khi truy vấn dữ liệu: {e}")
        return []


def get_patient_and_appointment():
    # Lấy idLichKham từ session
    id_lich_kham = session.get('idLichKham')

    if not id_lich_kham:
        return None  # Trả về None nếu không có ID trong session

    # Truy vấn dữ liệu với join
    result = db.session.query(
        BenhNhan.hoTen,
        BenhNhan.username,
        BenhNhan.gioiTinh,
        BenhNhan.ngaySinh,
        BenhNhan.cccd,
        BenhNhan.diaChi,
        BenhNhan.sdt,
        LichKham.ngayDangKy,
        LichKham.ngayKham
    ).join(
        LichKham, BenhNhan.idBenhNhan == LichKham.id_benhnhan
    ).filter(
        LichKham.idLichKham == id_lich_kham
    ).first()

    # Kiểm tra kết quả
    if result:
        # Định dạng kết quả trả về dưới dạng từ điển
        return {
            'hoTen': result.hoTen,
            'username': result.username,
            'gioiTinh': 'Nam' if result.gioiTinh else 'Nữ',
            'ngaySinh': str(result.ngaySinh),
            'cccd': result.cccd,
            'diaChi': result.diaChi,
            'sdt': result.sdt,
            'ngayDangKy': str(result.ngayDangKy),
            'ngayKham': str(result.ngayKham)
        }
    else:
        return None


def check_reload_LichKham(listLK, listCheck):
    if listCheck == None or listLK == None:
        return False

    for lichkham in listLK:
        for check in listCheck:
            if (lichkham['stt'] == check['stt']):
                if (lichkham['tinhTrang'] != check['tinhTrang']):
                    return True
    return False


def luuPhieuKham(idBenhNhan, idBacSi, listThuoc, ngayKham, trieuChung, chanDoan):
    print("vao luu phieu kham")
    print(f"Gọi luuPhieuKham với: idBenhNhan={idBenhNhan}, idBacSi={idBacSi},"
          f" ngayKham={ngayKham}, trieuChung={trieuChung}, chanDoan={chanDoan}, listThuoc={listThuoc}")

    phieuKham = PhieuKham(ngayTao=datetime.strptime(ngayKham, '%Y-%m-%d'),
                          id_benhnhan=int(idBenhNhan), trieuChung=trieuChung,
                          chanDoan=chanDoan, id_bacsi=int(idBacSi))

    db.session.add(phieuKham)
    db.session.commit()
    print(f"Da tao phieu kham: {phieuKham}")
    idPhieuKham = int(phieuKham.idPhieuKham)
    print(f"Da tao phieu kham: {idPhieuKham}")
    for thuoc in listThuoc:
        thuocIN = ChiTietDonThuoc(id_phieukham=idPhieuKham,
                                  id_thuoc=int(thuoc['idThuoc']), soLuongThuoc=int(thuoc['soLuong']))
        db.session.add(thuocIN)
        print(f"Da tao list thuoc: {thuocIN}")
    db.session.commit()
    print(f"Da tao da tao xong")
    return {"status": "success", "message": "Phieu Kham da duoc luu thanh cong."}


def get_LSKB(idBenhNhan):
    benhNhan = get_TT_HoSoBenhNhan(idBenhNhan=idBenhNhan)
    listPhieuKham = get_ListPhieuKham(idBenhNhan=benhNhan['id_benhnhan'])
    listPhieuKham.sort(key=lambda x: x['ngayTao'], reverse=True)
    listPhieuKham_result = []
    for phieuKham in listPhieuKham:
        donThuoc = get_ListThuoc(phieuKham['idPhieuKham'])
        listPhieuKham_result.append({
            'idPhieuKham': phieuKham['idPhieuKham'],
            'ngayTao': phieuKham['ngayTao'],
            'trieuChung': phieuKham['trieuChung'],
            'chanDoan': phieuKham['chanDoan'],
            'id_bacsi': phieuKham['id_bacsi'],
            'idBacSi': phieuKham['idBacSi'],
            'hoTen': phieuKham['hoTen'],
            'gioiTinh': phieuKham['gioiTinh'],
            'chuyenKhoa': phieuKham['chuyenKhoa'],
            'avatar': phieuKham['avatar'],
            'ngaySinh': phieuKham['ngaySinh'],
            'donThuoc': donThuoc
        })
    return listPhieuKham_result


def get_TT_HoSoBenhNhan(idBenhNhan):
    result = db.session.query(HoSoBenhNhan.idHoSo,
                              HoSoBenhNhan.ngayTao,
                              HoSoBenhNhan.tinhTrang,
                              HoSoBenhNhan.id_benhnhan,
                              BenhNhan.hoTen,
                              BenhNhan.ngaySinh,
                              BenhNhan.diaChi,
                              BenhNhan.avatar,
                              BenhNhan.gioiTinh,
                              BenhNhan.sdt,
                              BenhNhan.cccd
                              ).join(
        BenhNhan, BenhNhan.idBenhNhan == HoSoBenhNhan.id_benhnhan
    ).filter(
        HoSoBenhNhan.id_benhnhan == idBenhNhan
    ).first()

    if result:
        return {
            'idHoSo': str(result.idHoSo),
            'ngayTao': result.ngayTao.strftime('%d.%m.%Y'),
            'tinhTrang': result.tinhTrang,
            'id_benhnhan': str(result.id_benhnhan),
            'hoTen': result.hoTen,
            'ngaySinh': result.ngaySinh.strftime('%d.%m.%Y'),
            'diaChi': result.diaChi,
            'avatar': result.avatar,
            'gioiTinh': 'Nam' if result.gioiTinh else 'Nữ',
            'sdt': str(result.sdt),
            'cccd': str(result.cccd)
        }
    else:
        return None


def get_ListPhieuKham(idBenhNhan):
    listPK = db.session.query(
        PhieuKham.idPhieuKham,
        PhieuKham.ngayTao,
        PhieuKham.trieuChung,
        PhieuKham.chanDoan,
        PhieuKham.id_bacsi,
        BacSi.idBacSi,
        BacSi.hoTen,
        BacSi.gioiTinh,
        BacSi.chuyenKhoa,
        BacSi.avatar,
        BacSi.ngaySinh
    ).join(
        BacSi, BacSi.idBacSi == PhieuKham.id_bacsi
    ).filter(
        PhieuKham.id_benhnhan == idBenhNhan
    ).all()

    listPhieuKham_result = []
    for row in listPK:
        listPhieuKham_result.append({
            'idPhieuKham': row.idPhieuKham,
            'ngayTao': row.ngayTao.strftime('%d.%m.%Y'),
            'trieuChung': row.trieuChung,
            'chanDoan': row.chanDoan,
            'id_bacsi': row.id_bacsi,
            'idBacSi': row.idBacSi,
            'hoTen': row.hoTen,
            'gioiTinh': 'Nam' if row.gioiTinh else 'Nữ',
            'chuyenKhoa': row.chuyenKhoa,
            'avatar': row.avatar,
            'ngaySinh': row.ngaySinh.strftime('%d.%m.%Y')
        })
    return listPhieuKham_result


def get_ListThuoc(idPhieuKham):
    listThuoc = db.session.query(
        ChiTietDonThuoc.id_thuoc,
        ChiTietDonThuoc.soLuongThuoc,
        ChiTietDonThuoc.id_phieukham,
        Thuoc.tenThuoc,
        Thuoc.huongDanSuDung,
        Thuoc.loaiThuoc
    ).join(
        Thuoc, Thuoc.idThuoc == ChiTietDonThuoc.id_thuoc
    ).filter(
        ChiTietDonThuoc.id_phieukham == idPhieuKham
    ).all()

    listThuoc_result = []
    i = 1
    for row in listThuoc:
        loaiThuoc = ''
        if row.loaiThuoc == DonVi.VIEN:
            loaiThuoc = 'Viên'
        elif row.loaiThuoc == DonVi.CHAI:
            loaiThuoc = 'Chai'
        elif row.loaiThuoc == DonVi.VY:
            loaiThuoc = 'Vỹ'
        listThuoc_result.append({
            'stt': i,
            'idThuoc': str(row.id_thuoc),
            'soLuongThuoc': str(row.soLuongThuoc),
            'loaiThuoc': loaiThuoc,
            'idPhieuKham': str(row.id_phieukham),
            'tenThuoc': row.tenThuoc,
            'huongDanSuDung': row.huongDanSuDung,
        })
        i += 1
    return listThuoc_result


if __name__ == '__main__':
    with app.app_context():
        print(get_LSKB(5))


def get_thuoc():
    # Lấy tất cả các thuốc từ cơ sở dữ liệu
    thuocs = Thuoc.query.all()

    # Danh sách thuốc sau khi chuyển đổi enum loại thuốc sang tiếng Việt
    danh_sach_thuoc = []

    for thuoc in thuocs:
        tenLoaiThuoc = DonVi.readable(DonVi, thuoc.loaiThuoc)  # Đổi enum thuốc sang tiếng Việt
        thuoc_info = {
            'idThuoc': thuoc.idThuoc,
            'tenThuoc': thuoc.tenThuoc,
            'loaiThuoc': tenLoaiThuoc,
            'huongDanSuDung': thuoc.huongDanSuDung
        }
        danh_sach_thuoc.append(thuoc_info)

    return danh_sach_thuoc


if __name__ == '__main__':
    with app.app_context():
        print(get_thuoc())


def getListPhieuKham(idBenhNhan):
    listLichKham = db.session.query(PhieuKham).filter(PhieuKham.id_benhnhan == idBenhNhan).all()
    return listLichKham


def benhnhan_to_dict(bn):
    bn1 = BenhNhan.query.filter_by(idBenhNhan=bn).first()
    return bn1.__dict__


def get_current_date_as_string():
    output_format = '%d/%m/%Y'
    return datetime.today().strftime(output_format)
