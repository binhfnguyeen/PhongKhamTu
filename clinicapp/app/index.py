from flask import render_template, request, redirect, session, flash, jsonify
from sqlalchemy.sql.functions import current_user
from clinicapp.app import app, login
import dao
from flask_login import login_user, logout_user, current_user
from datetime import datetime


@app.route('/')
def index():
    return render_template('home.html', list_comment=dao.load_comment())


@app.route('/login', methods=['post', 'get'])
def login_process():
    if request.method.__eq__("POST"):
        username = request.form.get('username')
        password = request.form.get('password')
        user = dao.auth_user(username=username, password=password, role="benhnhan")
        yta = dao.auth_user(username=username, password=password, role="yta")
        bacsi = dao.auth_user(username=username, password=password, role="bacsi")
        thungan = dao.auth_user(username=username, password=password, role="thungan")
        quantri = dao.auth_user(username=username, password=password, role="quantri")

        if user:
            login_user(user)
            return redirect('/')

        if yta:
            login_user(yta)
            return redirect('/')

        if bacsi:
            login_user(bacsi)
            return redirect('/')

        if thungan:
            login_user(thungan)
            return redirect('/')

        if quantri:
            login_user(quantri)
            return redirect('/')

    flash('Đăng nhập thất bại! Kiểm tra tên đăng nhập và mật khẩu.', 'danger')
    return render_template('login.html')


@app.route("/login-admin", methods=['post'])
def login_admin_process():
    if request.method.__eq__("POST"):
        username = request.form.get('username')
        password = request.form.get('password')
        quantri = dao.auth_user(username=username, password=password, role="quantri")
        if quantri:
            login_user(quantri)
            print(f"Logged in user: {current_user}")
            flash('Đăng nhập thành công!', 'success')
            return redirect('/admin')

        flash('Đăng nhập thất bại! Kiểm tra tên đăng nhập và mật khẩu.', 'danger')
        return redirect('/admin')


@app.route('/logout')
def logout_process():
    if current_user.is_authenticated:
        logout_user()
        flash('Đăng xuất thành công!', 'success')
    else:
        flash('Bạn chưa đăng nhập!', 'warning')
    return redirect('/login')


@app.route('/logout-admin')
def logout_admin_process():
    if current_user.is_authenticated and current_user.idQuanTri:
        logout_user()
        flash('Đăng xuất thành công!', 'success')
    else:
        flash('Bạn chưa đăng nhập!', 'warning')
    return redirect('/admin')


@app.route('/register', methods=['get', 'post'])
def signup_process():
    if request.method.__eq__("POST"):
        password = request.form.get('password')
        confirm = request.form.get('confirm')
        if password.__eq__(confirm):
            data = request.form.copy()
            del data['confirm']
            dao.add_user(avatar=request.files.get('avatar'), **data)
            flash('Đăng ký thành công! Vui lòng đăng nhập.', 'success')
            return redirect('/login')
        else:
            flash('Mật khẩu không khớp!', 'danger')
    return render_template('register.html')


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

            try:
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
                flash("Lưu thông tin thành công!", "success")
                return redirect('/trangcanhan')

            except Exception as e:
                flash("Lưu sai thông tin!", "danger")
                return redirect('/trangcanhan')

    flash("Lưu thông tin không thành công!", "warning")
    return render_template("login.html")


@login.user_loader
def get_user_by_id(user_id):
    user = dao.get_id_user(user_id)
    if user:
        print(f"Found BenhNhan: {user}")
        return user

    yta = dao.get_id_yta(user_id)
    if yta:
        print(f"Found YTa: {yta}")
        return yta

    bacsi = dao.get_id_bacsi(user_id)
    if bacsi:
        print(f"Found BacSi: {bacsi}")
        return bacsi

    thungan = dao.get_id_thungan(user_id)
    if thungan:
        print(f"Found ThuNgan: {thungan}")
        return thungan

    quantri = dao.get_id_quantri(user_id)
    if quantri:
        print(f"Found QuanTri: {quantri}")
        return quantri

    print("No user found")
    return None


@app.route('/datlichkham')
def datlichkham():
    if hasattr(current_user, 'idBenhNhan') and current_user.idBenhNhan:
        user_info = None
        user = dao.get_id_user(current_user.idBenhNhan)
        if user:
            user_info = user
        return render_template("datlichkham.html", user_info=user_info)
    else:
        return redirect('/')


@app.route('/taolichhen', methods=["get", "post"])
def make_a_appointment():
    if request.method.__eq__("POST"):
        if current_user.is_authenticated:
            user_id = current_user.idBenhNhan
            ngayDangKy = request.form.get('ngayDangKy')

            try:
                result = dao.update_lichkham(user_id, ngayDangKy, ngayKham=None, idYTa=None)
                if result:
                    flash("Đăng ký lịch hẹn thành công!", "success")
                else:
                    flash("Không thể đăng ký lịch hẹn. Vui lòng thử lại!", "warning")
            except Exception as e:
                flash(f"Đã xảy ra lỗi khi tạo lịch hẹn: {str(e)}", "danger")

            return redirect('/datlichkham')

    flash("Bạn cần đăng nhập để tạo lịch hẹn!", "warning")
    return redirect('/login')


@app.route('/dsk_benhnhan')
def dsk_benhnhan():
    if hasattr(current_user, 'idBenhNhan') and current_user.idBenhNhan:
        lichkham_list = dao.get_ds_lichkham_relationship(current_user.idBenhNhan)
        return render_template('danhsachkham_benhnhan.html', lichkham_list=lichkham_list)
    else:
        return redirect('/')


@app.route('/dsk_yta')
def dsk_yta():
    if hasattr(current_user, 'idYTa') and current_user.idYTa:
        list_lichkham = dao.get_danhsach_lichkham_benhnhan()
        lichkham_duoc_chon = session.get('lichkham_duoc_chon', [])
        return render_template('danhsachkham_yta.html',
                               danhsach=list_lichkham, lichkham_duoc_chon=lichkham_duoc_chon)
    else:
        return redirect('/')


@app.route('/api/chonlichkham', methods=['POST'])
def choose_appointment():
    try:
        data = request.get_json()
        lichkham_id = data.get('lichkham_id')

        if not lichkham_id:
            return jsonify({'error': 'Thiếu lichkham_id'}), 400

        lichkham_duoc_chon = dao.get_lichkham(lichkham_id=lichkham_id)
        if not lichkham_duoc_chon:
            return jsonify({'error': 'Lịch khám không tồn tại'}), 404

        user_info = dao.get_user(lichkham_duoc_chon.id_benhnhan)
        if not user_info:
            return jsonify({'error': 'Bệnh nhân không tồn tại'}), 404

        list_lichkham_duoc_chon = session.get('lichkham_duoc_chon', [])
        list_lichkham_duoc_chon_ids = [lk['idLichKham'] for lk in list_lichkham_duoc_chon]

        if len(list_lichkham_duoc_chon) >= 40:
            return jsonify({'error': 'Danh sách bệnh nhân đã đạt tối đa 40 người.'}), 400

        if lichkham_duoc_chon.idLichKham not in list_lichkham_duoc_chon_ids:
            list_lichkham_duoc_chon.append({
                'idLichKham': lichkham_duoc_chon.idLichKham,
                'idBenhNhan': user_info.idBenhNhan,
                'hoTen': user_info.hoTen,
                'gioiTinh': "Nam" if user_info.gioiTinh else "Nữ",
                'ngaySinh': user_info.ngaySinh.strftime('%d/%m/%Y'),
                'diaChi': user_info.diaChi,
                'ngayDangKy': lichkham_duoc_chon.ngayDangKy.strftime('%d/%m/%Y'),
                'ngayKham': lichkham_duoc_chon.ngayKham.strftime(
                    '%d/%m/%Y') if lichkham_duoc_chon.ngayKham else 'Chưa xác định',
            })
            session['lichkham_duoc_chon'] = list_lichkham_duoc_chon

            print(session['lichkham_duoc_chon'])
        return jsonify({'success': True, 'lichkham_duoc_chon': session['lichkham_duoc_chon']})

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/themngaykham', methods=["post"])
def update_ngaykham():
    try:
        data = request.get_json()
        lichkham_id = data.get('lichkham_id')
        ngayKham = data.get('ngayKham')

        if not lichkham_id or not ngayKham:
            return jsonify({'success': False, 'message': 'Thiếu thông tin.'}), 400

        ngaykham_format = datetime.strptime(ngayKham, '%Y-%m-%d').date()

        yta = dao.get_current_yta_by_id(current_user.idYTa)
        dao.yta_update_lichkham(lichkham_id=lichkham_id, ngayKham=ngaykham_format, yta_id=yta.idYTa)

        return jsonify({
            'success': True,
            'message': 'Ngày khám đã được cập nhật thành công!',
            'ngayKham': ngaykham_format.strftime('%d/%m/%Y')
        }), 200

    except Exception as e:
        return jsonify({'success': False, 'message': f'Có lỗi xảy ra: {str(e)}'}), 500


@app.route('/api/xoalichkham', methods=['POST'])
def delete_appointment():
    lichkham_id = int(request.json.get('lichkham_id'))

    list_lichkham_duoc_chon = session.get('lichkham_duoc_chon', [])

    list_lichkham_duoc_chon = [lich for lich in list_lichkham_duoc_chon if lich['idLichKham'] != lichkham_id]
    session['lichkham_duoc_chon'] = list_lichkham_duoc_chon

    print(session['lichkham_duoc_chon'])
    return jsonify({"success": True, "message": "Xóa lịch khám thành công!"})


@app.route('/api/xoahetlichkham', methods=['POST'])
def delete_all_appointments():
    list_lichkham_duoc_chon = session.get('lichkham_duoc_chon', [])

    if not list_lichkham_duoc_chon:
        return jsonify({"success": False, "message": "Không có lịch khám nào để xóa!"})

    session['lichkham_duoc_chon'] = []

    print(session['lichkham_duoc_chon'])
    return jsonify({"success": True, "message": "Xóa tất cả lịch khám thành công!"})


@app.route('/lapphieukham')
def lapphieukham():
    return render_template('lapphieukham.html')


@app.route('/baocaothongke')
def baocaothongke():
    return render_template('baocaothongke.html')


@app.route('/thanhtoan')
def thanhtoan():
    return render_template('thanhtoan.html')


@app.route('/api/comments', methods=['post'])
def add_comment():
    content = request.json.get('content')
    print(f"Received content: {content}")  # Debug log
    try:
        c = dao.add_comment(content=content)
        return {
            'content': c.content,
            'created_date': c.created_date.strftime("%Y-%m-%d %H:%M:%S"),
            'user': {
                'avatar': current_user.avatar,
                'hoTen': current_user.hoTen
            }
        }, 200
    except Exception as e:
        print(f"Error: {e}")  # Debug lỗi
        return {'error': str(e)}, 400


if __name__ == '__main__':
    from clinicapp.app import admin

    app.run(debug=True)
