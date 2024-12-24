from flask import render_template, request, redirect, url_for, jsonify, session, flash
from sqlalchemy.sql.functions import current_user
from clinicapp.app import app, login, db
import dao
from flask_login import login_user, logout_user, current_user
from datetime import datetime

from clinicapp.app.models import BenhNhan


@app.route('/')
def index():
    return render_template('home.html')


@app.route('/login', methods=['post', 'get'])
def login_process():
    if request.method.__eq__("POST"):
        username = request.form.get('username')
        password = request.form.get('password')
        user = dao.auth_user(username=username, password=password)
        if user:

            login_user(user)
            return redirect('/')
        else:
            flash('Đăng nhập thất bại! Kiểm tra tên đăng nhập và mật khẩu.', 'danger')

    return render_template('login.html')


@app.route('/logout')
def logout_process():
    logout_user()
    return redirect('/login')


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
            result = dao.update_lichkham(user_id, ngayDangKy, ngayKham=None, idYTa=None)
            return redirect('/')


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


@app.route('/chonlichkham', methods=['POST'])
def choose_appointment():
    lichkham_id = request.form.get('lichkham_id')
    lichkham_duoc_chon = dao.get_lichkham(lichkham_id=lichkham_id)
    user_info = dao.get_user(lichkham_duoc_chon.id_benhnhan)

    list_lichkham_duoc_chon = session.get('lichkham_duoc_chon', [])
    list_lichkham_duoc_chon_ids = [lk['idLichKham'] for lk in list_lichkham_duoc_chon]

    lich_kham_ids = session.get('lich_kham_ids', [])

    if len(list_lichkham_duoc_chon) >= 40:
        flash('Danh sách bệnh nhân đã đạt tối đa 40 người.', 'danger')
        return redirect('/dsk_yta')

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

        lich_kham_ids.append(lichkham_duoc_chon.idLichKham)
        session['lichkham_duoc_chon'] = list_lichkham_duoc_chon
        session['lich_kham_ids'] = lich_kham_ids

        print(session['lichkham_duoc_chon'])
        print(session['lich_kham_ids'])

    return redirect('/dsk_yta')


@app.route('/themngaykham', methods=["post"])
def update_ngaykham():
    print("Request Form Data:", request.form)
    lichkham_id = request.form.get('lichkham_id')
    ngayKham = request.form.get('ngayKham')
    ngaykham_format = datetime.strptime(ngayKham, '%Y-%m-%d').date()

    print(f"lichkham_id: {lichkham_id}, ngayKham: {ngayKham}")
    yta = dao.get_current_yta_by_id(current_user.idYTa)

    lichkham_duoc_chon = session.get('lichkham_duoc_chon', [])

    for lich in lichkham_duoc_chon:
        if lich['idLichKham'] == lichkham_id:
            lich['ngayKham'] = ngaykham_format
    try:
        dao.yta_update_lichkham(lichkham_id=lichkham_id, ngayKham=ngaykham_format, yta_id=yta.idYTa)
        flash('Ngày khám đã được cập nhật thành công!', 'success')
    except Exception as e:
        flash(f'Có lỗi xảy ra khi cập nhật ngày khám: {e}', 'danger')

    return redirect('/dsk_yta')


@app.route('/xoalichkham', methods=['POST'])
def delete_appointment():
    lichkham_id = int(request.form.get('lichkham_id'))

    list_lichkham_duoc_chon = session.get('lichkham_duoc_chon', [])
    lich_kham_ids = session.get('lich_kham_ids', [])

    list_lichkham_duoc_chon = [lich for lich in list_lichkham_duoc_chon if lich['idLichKham'] != lichkham_id]
    session['lichkham_duoc_chon'] = list_lichkham_duoc_chon

    if lichkham_id in lich_kham_ids:
        lich_kham_ids.remove(lichkham_id)
        session['lich_kham_ids'] = lich_kham_ids

    print(session['lich_kham_ids'])
    return redirect('/dsk_yta')


@app.route('/lapphieukham', methods=['GET','POST'])
def lapphieukham():
    benhnhan = dao.get_id_benhnhan(request.form.get('id_benhnhan'))
    hosobenhnhan = dao.get_TT_HoSoBenhNhan(request.form.get('id_benhnhan'))
    lichSuKhamBenh = dao.get_LSKB(request.form.get('id_benhnhan'))
    print(hosobenhnhan)
    print(lichSuKhamBenh)
    thuoc = dao.get_thuoc()
    return render_template('lapphieukham/lapphieukham_LapPhieu.html', date=dao.get_current_date_as_string(),
                           benhnhan=benhnhan, hosobenhnhan = hosobenhnhan, thuoc=thuoc, tinh_trang=dao.TINH_TRANG, lichSuKhamBenh=lichSuKhamBenh)


@app.route('/lichkham', methods=['GET'])
def lichkham():
    lichKhamToday = dao.get_LichKham_Today()
    # tinh trang bi thay doi
    if (dao.check_reload_LichKham(lichKhamToday, session.get('lichKhamToday', []))):
        return render_template('lapphieukham/lichkham.html', tinh_trang=dao.TINH_TRANG, date=dao.get_current_date_as_string())

    session['lichKhamToday'] = lichKhamToday
    print(session['lichKhamToday'])
    return render_template('lapphieukham/lichkham.html', tinh_trang=dao.TINH_TRANG,date=dao.get_current_date_as_string())


@app.route('/api/luuNhap', methods=['POST'])
def luuNhap():
    # Lưu thông tin vào session với ID bệnh nhân làm khóa
    list = session.get('List_PK_Nhap')

    if list is None: list = {}

    listThuoc = session.get('list_thuoc')

    if listThuoc is None: listThuoc = {}

    idBenhNhan = str(request.json.get('idBenhNhan'))
    ngayKham = str(request.json.get('ngayKham'))
    trieuChung = str(request.json.get('trieuChung'))
    chanDoan = str(request.json.get('chanDoan'))
    toaThuoc = request.json.get('listThuoc', [])

    list[idBenhNhan] = {
        "ngayKham": ngayKham,
        "trieuChung": trieuChung,
        "chanDoan": chanDoan,
    }

    for thuoc in toaThuoc:
        id = thuoc.get('idThuoc')
        listThuoc[idBenhNhan][id] = {
            "tenThuoc": thuoc.get('tenThuoc'),
            "donVi": thuoc.get('donVi'),
            "soLuong": thuoc.get('soLuong'),
            "cachDung": thuoc.get('cachDung'),
        }

    session['List_PK_Nhap'] = list
    session['listThuoc'] = listThuoc
    # cập nhật lịch khám
    lichKhamToday = session['lichKhamToday']
    for lich in lichKhamToday:
        if lich['idBenhNhan'] == idBenhNhan:
            lich['tinh_trang'] = 2
            break
    session['lichKhamToday'] = lichKhamToday
    print(lichKhamToday)
    print(list)
    print(listThuoc)
    return jsonify({})

@app.route('/api/luuPhieuKham', methods=['POST'])
def luuPhieuKham():
    try:
        def json_get(key, default=None, data_type=str):
            value = request.json.get(key, default)
            return data_type(value) if value is not None else default

        idBenhNhan = json_get('idBenhNhan')
        ngayKham = json_get('ngayKham')
        trieuChung = json_get('trieuChung')
        chanDoan = json_get('chanDoan')
        listThuoc = request.json.get('listThuoc', [])
        idBacSi = '2'
        for thuoc in listThuoc:
            # Lấy tên thuốc và loại bỏ tất cả khoảng trắng thừa
            tenThuocRaw = thuoc['tenThuoc']
            tenThuocClean = ' '.join(tenThuocRaw.split())  # Loại bỏ khoảng trắng thừa
            thuoc['tenThuoc'] = tenThuocClean

        # Gọi hàm lưu phiếu khám
        print(
            f"Gọi luuPhieuKham với: idBenhNhan={idBenhNhan}, idBacSi={idBacSi}, ngayKham={ngayKham}, trieuChung={trieuChung}, chanDoan={chanDoan}, listThuoc={listThuoc}")
        dao.luuPhieuKham(idBenhNhan=idBenhNhan, idBacSi=idBacSi, ngayKham=ngayKham, trieuChung=trieuChung,
                         chanDoan=chanDoan, listThuoc=listThuoc)
        print('da goi ham luu')
        # Cập nhật trạng thái lịch khám trong session

        lichKham = session.get('lichKhamToday', [])
        print(lichKham)

        for i in lichKham:
            if int(i['id_benhnhan']) == int(idBenhNhan):
                i['tinhTrang'] = 2
                flash('Tình trạng khám đã được cập nhật thành công!', 'success')
                print(i)
                break
        session['lichKhamToday'] = lichKham
        print(lichKham)
        return jsonify({'success': True, 'message': 'Phiếu khám đã được lưu.'}), 200

    except Exception as e:
        # Trả về lỗi nếu có vấn đề xảy ra
        return jsonify({'err': True, 'message': str(e)}), 500


@app.route('/get_luuNhap/<idBenhNhan>', methods=['GET'])
def get_luuNhan(idBenhNhan):
    # Lấy dữ liệu nháp từ session
    drafts = session.get('List_PK_Nhap', {})
    draft_data = drafts.get(idBenhNhan, None)  # Lấy dữ liệu nháp cho bệnh nhân cụ thể

    if draft_data:
        return jsonify({'status': 'success', 'data': draft_data}), 200
    else:
        return jsonify({'status': 'not_found'}), 404


@app.route('/tracuuthuoc')
def tracuuthuoc():
    dsthuoc = dao.get_thuoc()
    return render_template('lapphieukham/tracuuthuoc.html', dsthuoc=dsthuoc)


@app.route('/api/thuoc', methods=['GET'])
def get_list_thuoc():
    thuoc = dao.get_thuoc()
    return jsonify(thuoc)


@app.route('/baocaothongke')
def baocaothongke():
    return render_template('baocaothongke.html')


@app.route('/thanhtoan')
def thanhtoan():
    return render_template('thanhtoan.html')


# Route để lưu ngày vào session
if __name__ == '__main__':
    app.run(debug=True)
