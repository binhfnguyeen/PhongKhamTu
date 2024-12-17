from flask import request
from flask_admin import AdminIndexView, Admin, BaseView, expose
from flask_admin.contrib.sqla import ModelView
from flask_admin.form import Select2Widget
from flask_login import current_user
from wtforms.fields.choices import SelectField
from models import Thuoc, NhanVien, BenhNhan, DonVi, YTa, BacSi, ThuNgan, QuanTri
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


class ThuocView(AdminView):
    can_edit = True
    can_create = True
    can_delete = True
    column_display_pk = True
    can_view_details = True
    can_export = True
    column_searchable_list = ['tenThuoc']
    column_filters = ['tenThuoc', 'loaiThuoc']
    column_list = ['idThuoc', 'tenThuoc', 'loaiThuoc', 'huongDanSuDung']
    column_labels = {
        'idThuoc': 'Mã thuốc',
        'tenThuoc': 'Tên thuốc',
        'loaiThuoc': 'Loại thuốc',
        'huongDanSuDung': 'Hướng dẫn sử dụng'
    }

    def on_model_change(self, form, model, is_created):
        if is_created:
            if not model.loaiThuoc:
                model.loaiThuoc = DonVi.VIEN
        return super().on_model_change(form, model, is_created)

    form_extra_fields = {
        'loaiThuoc': SelectField(
            'Loại thuốc',
            choices=[(tag.name, tag.name) for tag in DonVi]
        )
    }

    form_widget_args = {
        'loaiThuoc': {
            'widget': Select2Widget()
        }
    }


class YTaView(AdminView):
    can_edit = True
    can_create = True
    can_delete = True
    column_display_pk = True
    can_view_details = True
    can_export = True
    column_searchable_list = ['hoTen']
    column_filters = ['idYTa', 'gioiTinh']
    column_list = ['idYTa', 'hoTen', 'username', 'password', 'sdt', 'gioiTinh', 'ngaySinh', 'diaChi']

    column_formatters = {
        'gioiTinh': lambda v, c, m, p: 'Nam' if m.gioiTinh else 'Nữ'
    }

    column_labels = {
        'idYTa': 'ID',
        'hoTen': 'Họ tên',
        'username': 'Tài khoản',
        'password': 'Mật khẩu',
        'gioiTinh': 'Giới tính',
        'ngaySinh': 'Ngày Sinh',
        'sdt': 'Số điện thoại',
        'diaChi': 'Địa chỉ'
    }

    def on_model_change(self, form, model, is_created):
        if is_created:
            if model.gioiTinh is None:
                model.gioiTinh = True  # Default to 'Nam'
        return super().on_model_change(form, model, is_created)

    form_extra_fields = {
        'gioiTinh': SelectField(
            'Giới tính',
            choices=[(True, 'Nam'), (False, 'Nữ')],
            default=True
        )
    }

    form_widget_args = {
        'gioiTinh': {
            'widget': Select2Widget()
        }
    }

    def get_search_form(self):
        form = super(YTaView, self).get_search_form()
        form.gioiTinh.choices = [(True, 'Nam'), (False, 'Nữ')]  # Custom filter choices
        return form


class BacSiView(AdminView):
    can_edit = True
    can_create = True
    can_delete = True
    column_display_pk = True
    column_list = ['idBacSi', 'hoTen', 'chuyenKhoa', 'username', 'password', 'sdt', 'gioiTinh', 'ngaySinh', 'diaChi']

    column_formatters = {
        'gioiTinh': lambda v, c, m, p: 'Nam' if m.gioiTinh else 'Nữ'
    }

    column_labels = {
        'idBacSi': 'ID',
        'hoTen': 'Họ tên',
        'chuyenKhoa': 'Chuyên khoa',
        'username': 'Tài khoản',
        'password': 'Mật khẩu',
        'gioiTinh': 'Giới tính',
        'ngaySinh': 'Ngày Sinh',
        'sdt': 'Số điện thoại',
        'diaChi': 'Địa chỉ'
    }


class ThuNganView(AdminView):
    can_edit = True
    can_create = True
    can_delete = True
    column_display_pk = True
    column_list = ['idThuNgan', 'hoTen', 'username', 'password', 'sdt', 'gioiTinh', 'ngaySinh', 'diaChi']

    column_formatters = {
        'gioiTinh': lambda v, c, m, p: 'Nam' if m.gioiTinh else 'Nữ'
    }

    column_labels = {
        'idThuNgan': 'ID',
        'hoTen': 'Họ tên',
        'username': 'Tài khoản',
        'password': 'Mật khẩu',
        'gioiTinh': 'Giới tính',
        'ngaySinh': 'Ngày Sinh',
        'sdt': 'Số điện thoại',
        'diaChi': 'Địa chỉ'
    }


class QuanTriView(AdminView):
    can_edit = True
    can_create = True
    can_delete = True
    column_display_pk = True
    column_list = ['idQuanTri', 'hoTen', 'username', 'password', 'sdt', 'gioiTinh', 'ngaySinh', 'diaChi']

    column_formatters = {
        'gioiTinh': lambda v, c, m, p: 'Nam' if m.gioiTinh else 'Nữ'
    }

    column_labels = {
        'idQuanTri': 'ID',
        'hoTen': 'Họ tên',
        'username': 'Tài khoản',
        'password': 'Mật khẩu',
        'gioiTinh': 'Giới tính',
        'ngaySinh': 'Ngày Sinh',
        'sdt': 'Số điện thoại',
        'diaChi': 'Địa chỉ'
    }


class DoanhThuView(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.idQuanTri

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
                return self.render('admin/baocaodoanhthu.html', report_data=report_data, month=month, year=year,
                                   tong_doanh_thu=tong_doanh_thu)
            else:
                return self.render('admin/baocaodoanhthu.html', error="Vui lòng chọn tháng và năm.")
        return self.render('admin/baocaodoanhthu.html')


class SuDungThuocView(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.idQuanTri

    @expose('/', methods=['GET', 'POST'])
    def index(self):
        if request.method == 'POST':
            month_year = request.form.get('month_year_baocao')
            if month_year:
                year, month = month_year.split('-')

                report_data = dao.thong_ke_su_dung_thuoc_theo_ngay(month, year)
                return self.render('admin/baocaosudungthuoc.html', report_data=report_data, month=month, year=year)
            else:
                return self.render('admin/baocaodoanhthu.html', error="Vui lòng chọn tháng và năm.")
        return self.render('admin/baocaosudungthuoc.html')


admin.add_view(ThuocView(Thuoc, db.session, name="Danh sách thuốc"))
admin.add_view(DoanhThuView(name="Báo cáo doanh thu"))
admin.add_view(SuDungThuocView(name="Báo cáo sử dụng thuốc"))
admin.add_view(YTaView(YTa, db.session, name="Y tá"))
admin.add_view(BacSiView(BacSi, db.session, name="Bác sĩ"))
admin.add_view(ThuNganView(ThuNgan, db.session, name="Thu ngân"))
admin.add_view(QuanTriView(QuanTri, db.session, name="Quản trị"))
