const btnScrollTop = document.getElementById('btnScrollTop');

// Hiển thị nút khi cuộn xuống
window.addEventListener('scroll', () => {
    if (window.scrollY > 200) {
        btnScrollTop.style.display = 'flex'; // Hiển thị nút
    } else {
        btnScrollTop.style.display = 'none'; // Ẩn nút
    }
});

// Cuộn lên đầu trang khi nhấn nút
btnScrollTop.addEventListener('click', () => {
    window.scrollTo({top: 0, behavior: 'smooth'});
});


document.addEventListener("DOMContentLoaded", function () {
    $('#datepicker').datepicker({
        format: 'dd/mm/yyyy',
        autoclose: true,
        todayHighlight: true
    });
});



//
// function savePhieuKham() {
//     const idBenhNhan = '{{ benhnhan.idBenhNhan }}'; // Lấy ID bệnh nhân từ template
//     const idBacSi = '1'; // Lấy ID bác sĩ từ template
//     const trieuChung = document.getElementById('trieuchungInput').value;
//     const chanDoan = document.getElementById('chandoanInput').value;
//     const ngayTao = new Date().toISOString().split('T')[0]; // Lấy ngày hiện tại
//     const donthuoc = []
//     document.querySelectorAll('#donThuoc tbody tr').forEach((row) => {
//         const idThuoc = row.querySelector('.inputTenThuoc').getAttribute('name');
//         const tenThuoc = row.querySelector('.inputTenThuoc').value;
//         const donVi = row.querySelector('.inputDonViThuoc').value;
//         const soLuong = row.querySelector('.inputSoLuongThuoc').value;
//         const cachDung = row.querySelector('.inputCachDung').value;
//
//         listThuoc.push({
//             idThuoc: idThuoc,
//             tenThuoc: tenThuoc,
//             donVi: donVi,
//             soLuong: soLuong,
//             cachDung: cachDung
//         });
//     });
//
//     fetch('/api/lapPhieuKham', {
//         method: 'POST',
//         headers: {
//             'Content-Type': 'application/json'
//         },
//         body: JSON.stringify({
//             idBenhNhan: idBenhNhan,
//             idBacSi: idBacSi,
//             trieuChung: trieuChung,
//             chanDoan: chanDoan,
//             ngayTao: ngayTao
//         })
//     })
//         .then(response => {
//             if (!response.ok) {
//                 throw new Error('Có lỗi xảy ra khi lưu phiếu khám.');
//             }
//             return response.json();
//         })
//         .then(data => {
//             Swal.fire("Đã lưu phiếu khám thành công!", {
//                 icon: "success",
//             }).then(() => {
//                 // Chuyển hướng đến trang khác nếu cần
//                 window.location.href = '/lapphieukham/lichkham.html';
//             });
//         })
//         .catch(error => {
//             Swal.fire("Có lỗi xảy ra khi lưu phiếu khám.", {
//                 icon: "error",
//             });
//         });
// }


