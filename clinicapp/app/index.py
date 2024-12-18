from flask import render_template, request, redirect
from sqlalchemy.sql.functions import current_user

from clinicapp.app import app, login
import dao
from flask_login import login_user, logout_user, current_user
from datetime import datetime


@app.route('/')
def index():
    return render_template('home.html')


@app.route('/login', methods=['post', 'get'])
def login_process():
    err_msg = ''
    if request.method.__eq__("POST"):
        username = request.form.get('username')
        password = request.form.get('password')
        user = dao.auth_user(username=username, password=password)
        if user:
            login_user(user)
            return redirect('/')
        else:
            err_msg = 'Đăng nhập thất bại! Kiểm tra tên đăng nhập và mật khẩu. '

    return render_template('login.html', err_msg=err_msg)


@app.route('/logout')
def logout_process():
    logout_user()
    return redirect('/login')


@app.route('/register', methods=['get', 'post'])
def signup_process():
    err_msg = ''
    if request.method.__eq__("POST"):
        password = request.form.get('password')
        confirm = request.form.get('confirm')
        if password.__eq__(confirm):
            data = request.form.copy()
            del data['confirm']
            dao.add_user(avatar=request.files.get('avatar'), **data)
            return redirect('/login')
        else:
            err_msg = 'Mật khẩu không khớp!'
    return render_template('register.html', err_msg=err_msg)


@app.route('/trangcanhan')
def user_profile():
    if current_user.is_authenticated:
        user_info = None

        if hasattr(current_user, 'idBenhNhan') and current_user.idBenhNhan:
            user = dao.get_id_user(current_user.idBenhNhan)
            if user:
                user_info = user
        elif hasattr(current_user, 'idYTa') and current_user.idYTa:
            yta = dao.get_id_yta(current_user.idYTa)
            if yta:
                user_info = yta
        elif hasattr(current_user, 'idBacSi') and current_user.idBacSi:
            bacsi = dao.get_id_bacsi(current_user.idBacSi)
            if bacsi:
                user_info = bacsi
        elif hasattr(current_user, 'idThuNgan') and current_user.idThuNgan:
            thungan = dao.get_id_thungan(current_user.idThuNgan)
            if thungan:
                user_info = thungan

        return render_template('trangcanhan.html', user_info=user_info)
    return render_template('login.html')


@app.route('/luuthongtin', methods=["get", "post"])
def update_profile():
    if request.method.__eq__("POST"):
        if current_user.is_authenticated:
            name = request.form.get('name')
            gioitinh_str = request.form.get('gioitinh')
            ngaysinh_str = request.form.get('ngaysinh')
            cccd = request.form.get('cccd')
            diachi = request.form.get('diachi')
            sdt = request.form.get('sdt')

            if gioitinh_str == '1':
                gioitinh = True
            elif gioitinh_str == '0':
                gioitinh = False
            else:
                gioitinh = None

            if ngaysinh_str:
                ngaysinh = datetime.strptime(ngaysinh_str, '%Y-%m-%d').date()
            else:
                ngaysinh = None

            if hasattr(current_user, 'idBenhNhan') and current_user.idBenhNhan:
                dao.update_profile(
                    user_id=current_user.idBenhNhan,
                    name=name.strip(),
                    gioiTinh=gioitinh,
                    ngaySinh=ngaysinh,
                    cccd=cccd.strip(),
                    diaChi=diachi.strip(),
                    sdt=sdt.strip()
                )
            elif hasattr(current_user, 'idYTa') and current_user.idYTa:
                dao.update_profile(
                    user_id=current_user.idYTa,
                    name=name.strip(),
                    gioiTinh=gioitinh,
                    ngaySinh=ngaysinh,
                    cccd=cccd.strip(),
                    diaChi=diachi.strip(),
                    sdt=sdt.strip()
                )
            elif hasattr(current_user, 'idBacSi') and current_user.idBacSi:
                dao.update_profile(
                    user_id=current_user.idBacSi,
                    name=name.strip(),
                    gioiTinh=gioitinh,
                    ngaySinh=ngaysinh,
                    cccd=cccd.strip(),
                    diaChi=diachi.strip(),
                    sdt=sdt.strip()
                )
            elif hasattr(current_user, 'idThuNgan') and current_user.idThuNgan:
                dao.update_profile(
                    user_id=current_user.idThuNgan,
                    name=name.strip(),
                    gioiTinh=gioitinh,
                    ngaySinh=ngaysinh,
                    cccd=cccd.strip(),
                    diaChi=diachi.strip(),
                    sdt=sdt.strip()
                )

            return redirect('/trangcanhan')

    return render_template("login.html")


@login.user_loader
def get_user_by_id(user_id):
    user = dao.get_id_user(user_id)
    if user:
        return user

    yta = dao.get_id_yta(user_id)
    if yta:
        return yta

    bacsi = dao.get_id_bacsi(user_id)
    if bacsi:
        return bacsi

    thungan = dao.get_id_thungan(user_id)
    if thungan:
        return thungan

    return None

@app.route('/datlichkham')
def datlichkham():
    return render_template('datlichkham.html')


@app.route('/lapphieukham')
def lapphieukham():
    return render_template('lapphieukham.html')


@app.route('/baocaothongke')
def baocaothongke():
    return render_template('baocaothongke.html')


@app.route('/thanhtoan')
def thanhtoan():
    return render_template('thanhtoan.html')


if __name__ == '__main__':
    app.run(debug=True)
