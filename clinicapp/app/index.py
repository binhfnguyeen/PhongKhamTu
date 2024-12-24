from flask import render_template, request, redirect, session, flash, jsonify
from sqlalchemy.sql.functions import current_user
from clinicapp.app import app, login, db
import dao
from flask_login import login_user, logout_user, current_user
from datetime import datetime


@app.route('/')
def index():
    comments=dao.load_comment()
    return render_template('home.html', list_comment=comments)


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

                if hasattr(current_user, 'idBenhNhan') and current_user.idBenhNhan:
                    a = dao.add_HoSoBenhNhan(current_user.idBenhNhan)
                    print("Ho so" + a)

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

        lich_kham_ids = session.get('lich_kham_ids', [])

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

            lich_kham_ids.append(lichkham_duoc_chon.idLichKham)

            session['lichkham_duoc_chon'] = list_lichkham_duoc_chon
            session['lich_kham_ids'] = lich_kham_ids

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


@app.route('/lichkham', methods=['GET' , 'POST'])
def lichkham():
    lichKhamToday = dao.get_LichKham_by_Yta()

    # if (dao.check_reload_LichKham(lichKhamToday, session.get('lichKhamToday', []))):
    #     return render_template('lapphieukham/lichkham.html', tinh_trang=dao.TINH_TRANG, date=dao.get_current_date_as_string())
    del session['lichKhamToday']
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
        idBacSi =  '4'
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
    danh_sach_phieu_kham = dao.load_phieu_kham()
    return render_template('thanhtoan.html', danh_sach_phieu_kham=danh_sach_phieu_kham)


@app.route('/api/search_by_id', methods=['POST'])
def search_by_id():
    data = request.get_json()
    id_phieukham = data.get('idPhieuKham')

    if not id_phieukham:
        return jsonify({"error": "Mã phiếu khám là bắt buộc"}), 400

    phieu_kham = dao.tim_phieukham_theo_id(id_phieukham)

    if phieu_kham:
        return jsonify([phieu_kham]), 200
    else:
        return jsonify({"error": "Không tìm thấy phiếu khám với mã này"}), 404


@app.route('/api/search_date_created', methods=["post"])
def time_theo_ngay_tao():
    data = request.get_json()
    ngay_tao = data.get('ngayTao')

    if not ngay_tao:
        return jsonify({"error": "Ngày tạo là bắt buộc"}), 400

    from datetime import datetime
    try:
        ngay_tao = datetime.strptime(ngay_tao, '%Y-%m-%d').date()
    except ValueError:
        return jsonify({"error": "Định dạng ngày tạo không hợp lệ. Vui lòng sử dụng định dạng yyyy-mm-dd"}), 400

    phieu_kham_list = dao.tim_phieukham_theo_ngaytao(ngay_tao)

    if phieu_kham_list:
        return jsonify(phieu_kham_list), 200
    else:
        return jsonify({"error": "Không tìm thấy phiếu khám nào với ngày tạo này"}), 404


@app.route('/api/viewdetail/<id_phieukham>', methods=['GET'])
def view_detail(id_phieukham):
    try:
        print(f"Received ID: {id_phieukham}")
        phieukham = dao.tim_phieukham_theo_id(id_phieukham)
        thuoc = dao.thuoc_theo_phieukham(id_phieukham)
        if phieukham:
            return jsonify({
                'idPhieuKham': phieukham['idPhieuKham'],
                'ngayTao': phieukham['ngayTao'],
                'trieuChung': phieukham['trieuChung'],
                'chanDoan': phieukham['chanDoan'],
                'ten_benhnhan': phieukham['ten_benhnhan'],
                'ten_bacsi': phieukham['ten_bacsi'],
                'thuoc': thuoc
            })
        return jsonify({
            'status': 'error',
            'message': 'Không tìm thấy phiếu khám'
        }), 404
    except Exception as e:
        print(f"Error: {e}")  # Log error message
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@app.route('/api/make_invoice/<id_phieukham>', methods=["post"])
def save_invoice(id_phieukham):
    if current_user.is_authenticated and current_user.idThuNgan:
        try:
            data = request.get_json()
            tienkham = data.get('tienkham')
            tienthuoc = data.get('tienthuoc')

            if not tienkham or not tienthuoc:
                return jsonify({"error": "Vui lòng nhập đủ tiền khám và tiền thuốc."}), 400

            hoa_don = dao.make_invoice(id_phieukham=id_phieukham, tienkham=tienkham, tienthuoc=tienthuoc,
                                       id_thungan=current_user.idThuNgan)

            return jsonify({
                "message": "Hóa đơn đã được lập thành công.",
                "hoa_don": {
                    "idHoaDon": hoa_don.idHoaDon,
                    "ngayKham": hoa_don.ngayKham,
                    "tienKham": hoa_don.tienKham,
                    "tienThuoc": hoa_don.tienThuoc,
                    "id_thungan": hoa_don.id_thungan
                }
            }), 200
        except Exception as e:
            return jsonify({"error": f"Lỗi khi tạo hóa đơn: {str(e)}"}), 500
    else:
        return jsonify({"error": "Bạn phải đăng nhập và có quyền thu ngân để lập hóa đơn."}), 403


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
