from datetime import datetime, date
from flask_login import current_user
from sqlalchemy import func
from sqlalchemy.engine import row
from sqlalchemy.orm import joinedload, join, outerjoin
from models import BenhNhan, NhanVien, YTa, BacSi, ThuNgan, QuanTri, LichKham, HoaDon, Thuoc, ChiTietDonThuoc, \
    PhieuKham, Comment, HoSoBenhNhan, DonVi
from clinicapp.app import db, app
import hashlib
import cloudinary.uploader
from flask import session, flash, redirect, url_for, render_template, request
from enum import Enum


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
    print(model)

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
            'doanh_thu': doanh_thu,
            'so_benh_nhan': so_benh_nhan,
            'tyle': round(ty_le, 2),
        })

    report.sort(key=lambda x: x['ngay_kham'])
    return report, tong_doanh_thu


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


def add_comment(content):
    if not current_user.is_authenticated:
        raise ValueError("User must be authenticated to comment")

    c = Comment(content=content, user_id=current_user.idBenhNhan)

    db.session.add(c)
    db.session.commit()
    return c


def load_phieu_kham():
    results = db.session.query(
        PhieuKham.idPhieuKham,
        PhieuKham.ngayTao,
        PhieuKham.trieuChung,
        PhieuKham.chanDoan,
        PhieuKham.id_benhnhan,
        PhieuKham.id_bacsi
    ).all()

    phieu_kham_list = []
    for result in results:
        ngayTao = result.ngayTao.strftime('%d/%m/%Y') if result.ngayTao else None
        phieu_kham_list.append({
            'idPhieuKham': result.idPhieuKham,
            'ngayTao': ngayTao,
            'trieuChung': result.trieuChung,
            'chanDoan': result.chanDoan,
            'id_benhnhan': result.id_benhnhan,
            'id_bacsi': result.id_bacsi
        })

    return phieu_kham_list


def tim_phieukham_theo_id(id):
    result = db.session.query(
        PhieuKham.idPhieuKham,
        PhieuKham.ngayTao.label('ngaytao'),
        PhieuKham.trieuChung.label('trieu_chung'),
        PhieuKham.chanDoan.label('chan_doan'),
        BenhNhan.hoTen.label('ten_benhnhan'),
        BacSi.hoTen.label('ten_bacsi')
    ).join(BenhNhan, PhieuKham.id_benhnhan == BenhNhan.idBenhNhan) \
        .join(BacSi, PhieuKham.id_bacsi == BacSi.idBacSi) \
        .filter(PhieuKham.idPhieuKham == id).first()

    if result:
        ngaytao = result.ngaytao.strftime('%d/%m/%Y') if result.ngaytao else None
        return {
            'idPhieuKham': result.idPhieuKham,
            'ngayTao': ngaytao,
            'trieuChung': result.trieu_chung,
            'chanDoan': result.chan_doan,
            'ten_benhnhan': result.ten_benhnhan,
            'ten_bacsi': result.ten_bacsi
        }
    return None


def tim_phieukham_theo_ngaytao(ngayTao):
    results = db.session.query(
        PhieuKham.idPhieuKham,
        PhieuKham.ngayTao.label('ngaytao'),
        PhieuKham.trieuChung.label('trieu_chung'),
        PhieuKham.chanDoan.label('chan_doan'),
        BenhNhan.hoTen.label('ten_benhnhan'),
        BacSi.hoTen.label('ten_bacsi')
    ).join(BenhNhan, PhieuKham.id_benhnhan == BenhNhan.idBenhNhan) \
        .join(BacSi, PhieuKham.id_bacsi == BacSi.idBacSi) \
        .filter(PhieuKham.ngayTao == ngayTao).all()

    if results:
        phieu_kham_list = []
        for result in results:
            ngaytao = result.ngaytao.strftime('%d/%m/%Y') if result.ngaytao else None
            phieu_kham_list.append({
                'idPhieuKham': result.idPhieuKham,
                'ngayTao': ngaytao,
                'trieuChung': result.trieu_chung,
                'chanDoan': result.chan_doan,
                'ten_benhnhan': result.ten_benhnhan,
                'ten_bacsi': result.ten_bacsi
            })
        return phieu_kham_list
    return None


def thuoc_theo_phieukham(id_phieukham):
    try:
        thuoc_query = db.session.query(
            Thuoc.idThuoc,
            Thuoc.tenThuoc,
            Thuoc.loaiThuoc,
            ChiTietDonThuoc.soLuongThuoc
        ).join(ChiTietDonThuoc, Thuoc.idThuoc == ChiTietDonThuoc.id_thuoc) \
            .join(PhieuKham, ChiTietDonThuoc.id_phieukham == PhieuKham.idPhieuKham) \
            .filter(PhieuKham.idPhieuKham == id_phieukham).all()

        if thuoc_query:
            thuoc_list = []
            for thuoc in thuoc_query:
                thuoc_list.append({
                    'idThuoc': thuoc.idThuoc,
                    'tenThuoc': thuoc.tenThuoc,
                    'loaiThuoc': thuoc.loaiThuoc.name,
                    'soLuongThuoc': thuoc.soLuongThuoc
                })
            return thuoc_list
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None


def find_phieukham_by_id(id_phieukham):
    return PhieuKham.query.filter_by(idPhieuKham=id_phieukham).first()


def make_invoice(id_phieukham, tienkham, tienthuoc, id_thungan):
    phieukham = find_phieukham_by_id(id_phieukham)

    if not phieukham:
        raise ValueError(f"PhieuKham with ID {id_phieukham} not found.")

    hoa_don = HoaDon(
        ngayKham=phieukham.ngayTao,
        tienKham=tienkham,
        tienThuoc=tienthuoc,
        id_thungan=id_thungan
    )

    db.session.add(hoa_don)
    db.session.commit()

    phieukham.id_hoadon = hoa_don.idHoaDon
    db.session.commit()

    return hoa_don


def load_comment():
    return Comment.query.all()


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
    benhnhan = BenhNhan.query.filter_by(idBenhNhan=id).first()
    kq = {
        'idBenhNhan': benhnhan.idBenhNhan,
        'hoTen': benhnhan.hoTen,
        'gioiTinh': benhnhan.gioiTinh,
        'ngaySinh': benhnhan.ngaySinh.strftime('%d/%m/%Y'),
        'diaChi': benhnhan.diaChi,
        'avatar': benhnhan.avatar
    }
    return kq

if __name__ == '__main__':
    with app.app_context():
        print(get_id_benhnhan(1))

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


def get_LichKham_by_Yta():
    if 'lich_kham_ids' in session:
        if session['lich_kham_ids']:
            dsLickKham_id = session.get('lich_kham_ids')
            dslickKham = []
            print(dsLickKham_id)
            # Duyệt qua các id trong session['lich_kham_ids'] và lấy thông tin chi tiết
            for id in dsLickKham_id:
                # Lấy thông tin phiếu khám và bệnh nhân
                lichKham = db.session.query(
                    LichKham.idLichKham,
                    LichKham.id_benhnhan,
                    LichKham.ngayKham,
                    BenhNhan.hoTen,
                    BenhNhan.ngaySinh,
                    BenhNhan.diaChi,
                    BenhNhan.gioiTinh,
                    BenhNhan.avatar,
                    BenhNhan.cccd
                ).join(BenhNhan, BenhNhan.idBenhNhan == LichKham.id_benhnhan).filter(LichKham.idLichKham == id).first()

                if lichKham:
                    dslickKham.append(lichKham)

            kq = []
            for i, row in enumerate(dslickKham, start=1):
                if row:  # Kiểm tra nếu kết quả không phải None
                    # Tạo dữ liệu trả về cho từng phiếu khám
                    kq.append({
                        'stt': i,
                        'id_lich': row.idLichKham,
                        'id_benhnhan': row.id_benhnhan,
                        'hoVaTen': row.hoTen,
                        'gioiTinh': row.gioiTinh,
                        'namSinh': row.ngaySinh.strftime("%d/%m/%Y") if row.ngaySinh else None,
                        'diaChi': row.diaChi,
                        'ngayKham': row.ngayKham.strftime("%d/%m/%Y") if row.ngayKham else None,
                        'avatar': row.avatar,
                        'cccd': row.cccd,
                        'tinhTrang': 0  # Có thể thay thế bằng enum hoặc trạng thái thực tế của phiếu khám
                    })

            # Sắp xếp theo trạng thái và thứ tự
            kq.sort(key=lambda x: (x['tinhTrang'], x['stt']))
            return kq

    # Trả về danh sách rỗng nếu không có thông tin
    return []


# if __name__ == '__main__':
#     with app.test_request_context():  # Thay app.app_context() bằng test_request_context()
#         # Đặt giá trị cho session tại đây nếu cần
#         session['lich_kham_ids'] = [1]  # Ví dụ về việc gán giá trị cho session
#         print(get_LichKham_by_Yta())




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

    phieuKham = PhieuKham(ngayTao=datetime.strptime(ngayKham, "%Y-%m-%d"),
                          id_benhnhan=int(idBenhNhan), trieuChung=trieuChung,
                          chanDoan=chanDoan, id_bacsi=int(idBacSi), id_hoadon=None)

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
            'ngayTao': result.ngayTao.strftime('%d/%m/%Y'),
            'tinhTrang': result.tinhTrang,
            'id_benhnhan': str(result.id_benhnhan),
            'hoTen': result.hoTen,
            'ngaySinh': result.ngaySinh.strftime('%d/%m/%Y'),
            'diaChi': result.diaChi,
            'avatar': result.avatar,
            'gioiTinh': 'Nam' if result.gioiTinh else 'Nữ',
            'sdt': str(result.sdt),
            'cccd': str(result.cccd)
        }
    else:
        return []


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
            'ngayTao': row.ngayTao.strftime('%d/%m/%Y'),
            'trieuChung': row.trieuChung,
            'chanDoan': row.chanDoan,
            'id_bacsi': row.id_bacsi,
            'idBacSi': row.idBacSi,
            'hoTen': row.hoTen,
            'gioiTinh': 'Nam' if row.gioiTinh else 'Nữ',
            'chuyenKhoa': row.chuyenKhoa,
            'avatar': row.avatar,
            'ngaySinh': row.ngaySinh.strftime('%d/%m/%Y')
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


def getListPhieuKham(idBenhNhan):
    listLichKham = db.session.query(PhieuKham).filter(PhieuKham.id_benhnhan == idBenhNhan).all()
    return listLichKham



def get_current_date_as_string():
    output_format = '%d/%m/%Y'
    return datetime.today().strftime(output_format)


def add_HoSoBenhNhan(id_benhnhan):
    try:
        hoso = HoSoBenhNhan(
            ngayTao=datetime.now(),
            tinhTrang="Binh Thuong",
            id_benhnhan=id_benhnhan
        )
        db.session.add(hoso)
        db.session.commit()
        return f"Đã tạo hồ sơ cho bệnh nhân ID {id_benhnhan}"
    except Exception as e:
        db.session.rollback()
        print(f"Lỗi trong add_HoSoBenhNhan: {e}")
        raise e


def get_hoadon_by_benhnhan(id_benhnhan):
    result = (
        db.session.query(HoaDon)
        .join(PhieuKham, HoaDon.idHoaDon == PhieuKham.id_hoadon)
        .filter(PhieuKham.id_benhnhan == id_benhnhan)
        .all()
    )
    return result


def get_lichsu_hoadon():
    return HoaDon.query.all()