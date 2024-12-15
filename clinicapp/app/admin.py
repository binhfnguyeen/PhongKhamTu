from flask import redirect, request, url_for
from flask_admin import AdminIndexView, Admin, BaseView, expose
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from models import HoaDon, ChiTietDonThuoc, Thuoc, NhanVien, BenhNhan
import dao
from clinicapp.app import app, db


class MyAdminIndexView(AdminIndexView):
    @expose('/')
    def index(self):
        user_count = BenhNhan.query.count()
        nhan_vien_count = NhanVien.query.count()

        return self.render('admin/index.html', user_count=user_count, nhan_vien_count=nhan_vien_count)


admin = Admin(app=app, name="Clinic Admin", template_mode="bootstrap4", index_view=MyAdminIndexView())


class AdminView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.idQuanTri


class HoaDonView(AdminView):
    column_list = ['ngayKham', 'tienKham', 'tienThuoc']


class NhanVienView(AdminView):
    column_list = ['hoTen', 'username', 'password', 'sdt', 'gioiTinh', 'ngaySinh', 'diaChi']

    column_formatters = {
        'gioiTinh': lambda v, c, m, p: 'Nam' if m.gioiTinh else 'Nữ'
    }


class DoanhThuView(BaseView):
    @expose('/', methods=['GET', 'POST'])
    def index(self):
        if request.method == 'POST':
            month_year = request.form.get('month_year_baocao')
            if month_year:
                year, month = month_year.split('-')
                print(year)
                print(month)
                year = int(year)
                month = int(month)
                report_data, tong_doanh_thu = dao.thong_ke_theo_ngay(month, year)
                return self.render('admin/baocaodoanhthu.html', report_data=report_data, month=month, year=year, tong_doanh_thu=tong_doanh_thu)
            else:
                return self.render('admin/baocaodoanhthu.html', error="Vui lòng chọn tháng và năm.")
        return self.render('admin/baocaodoanhthu.html')


class SuDungThuocView(BaseView):
    @expose('/')
    def index(self):
        return self.render('admin/baocaosudungthuoc.html')


admin.add_view(HoaDonView(HoaDon, db.session, name="Hóa đơn"))
admin.add_view(NhanVienView(NhanVien, db.session, name="Nhân Viên"))
admin.add_view(DoanhThuView(name="Báo cáo doanh thu"))
admin.add_view(SuDungThuocView(name="Báo cáo sử dụng thuốc"))
