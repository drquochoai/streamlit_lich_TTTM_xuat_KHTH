from venv import create
import streamlit as st
from func.o1_help_ten_PK_theo_KHTH import xuLyTenDanhSachPK
from SETTINGS_FOR_ALL import SETTINGS

import func.x1_xuat_phong_kham_Noi_Ngoai_TM as x1_xuat_phong_kham_Noi_Ngoai_TM
import func.x5_xuat_15_Lich_kham_oncall as x5_xuat_15_Lich_kham_oncall
import func.x3_xuat_13_Lich_DS_BS_tra_ket_qua as x3_xuat_13_Lich_DS_BS_tra_ket_qua
import func.x2_xuat_12_Lich_can_lam_sang_MERGE_THEO_COT as x2_xuat_12_Lich_can_lam_sang_MERGE_THEO_COT
import func.x4_xuat_14_Lich_Oncall_VIP____ as x4_xuat_14_Lich_Oncall_VIP
import pages.x1_x11_lich_truc_benh_vien_CODE_BLUE as x1_x11_lich_truc_benh_vien_CODE_BLUE
import func.x1_x11_lich_truc_benh_vien_TRUC as x1_x11_lich_truc_benh_vien_TRUC
import func.x1_x11_lich_truc_benh_vien_HOI_CHAN as x1_x11_lich_truc_benh_vien_HOI_CHAN
def xuat_all_combined():
    """ loop through st.session_state.ten_PK_theo_KHTH_unique
        check of checkbox is checked or not
        if checked, get the name of checkbox and add to list ten_PK_export
        if unchecked, remove the name of checkbox from list ten_PK_export
        and then call function xuatPhongKham with full_lich and ten_PK_export as arguments
    """
    for tenFileDeXuatHienTai in st.session_state.ten_PK_theo_KHTH_unique:
        if st.session_state.get(f"cb_export_{tenFileDeXuatHienTai}", False):

            st.write(f"## Xuất: {tenFileDeXuatHienTai}...")
            # st.spinner(f"Đang xuất file: '{tenFileDeXuatHienTai}'...")

            if tenFileDeXuatHienTai == "22. PK Nội tim mạch.xlsx" or tenFileDeXuatHienTai == "21. PK Ngoại Tim mạch.xlsx" or tenFileDeXuatHienTai == "1.2 Lịch Cận lâm sàng":
                # call function xuatPhongKham with full_lich and tenFileDeXuatHienTai as arguments
                x1_xuat_phong_kham_Noi_Ngoai_TM.xuatPhongKham(tenFileDeXuatHienTai)

            # elif tenFileDeXuatHienTai.startswith("1.2 Lịch Cận lâm sàng"):
            #     x2_xuat_12_Lich_can_lam_sang_MERGE_THEO_COT.xuat(tenFileDeXuatHienTai)
                
            elif tenFileDeXuatHienTai.startswith("1.3 Lịch DS BS trả kết quả"):
                x3_xuat_13_Lich_DS_BS_tra_ket_qua.xuat(tenFileDeXuatHienTai)

            elif tenFileDeXuatHienTai.startswith("1.4 Lịch Oncall Vip Bệnh viện"):
                x4_xuat_14_Lich_Oncall_VIP.xuat(tenFileDeXuatHienTai)

            elif tenFileDeXuatHienTai.startswith("1.5. Lịch khám oncall các Chuyên khoa Khu tiêu chuẩn"):
                x5_xuat_15_Lich_kham_oncall.xuat(tenFileDeXuatHienTai)

            elif tenFileDeXuatHienTai.startswith("1.1 Lịch trực Bệnh viện>LỊCH TRỰC CODE BLUE"):
                x5_xuat_15_Lich_kham_oncall.xuat(tenFileDeXuatHienTai)

            elif tenFileDeXuatHienTai.startswith("1.1 Lịch trực Bệnh viện>CODE BLUE"):
                x1_x11_lich_truc_benh_vien_CODE_BLUE.xuat(tenFileDeXuatHienTai)

            elif tenFileDeXuatHienTai.startswith("1.1 Lịch trực Bệnh viện>TRỰC"):
                x1_x11_lich_truc_benh_vien_TRUC.xuat(tenFileDeXuatHienTai)

            elif tenFileDeXuatHienTai.startswith("1.1 Lịch trực Bệnh viện>HỘI CHẨN"):
                x1_x11_lich_truc_benh_vien_HOI_CHAN.xuat(tenFileDeXuatHienTai)
    # Auto move to next page after exporting
    st.switch_page("pages/1_🪙💛Thống_kê.py")
    