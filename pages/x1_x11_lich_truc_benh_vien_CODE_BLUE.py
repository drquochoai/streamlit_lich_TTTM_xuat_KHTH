from func.x1_u1_filtered_PK_theoyeucau import filtered_PK_theo_ten_file_KHTH
import streamlit as st
import pandas as pd
from SETTINGS_FOR_ALL import SETTINGS

def xuat(tenFileDeXuatHienTai):
    """ 1.1 Lịch trực Bệnh viện>CODE BLUE
        Format: 1 ngày 2 hàng, xóa hàng Tr
        Để riêng 1 sheet
        TIM MẠCH:
                BÁO ĐỘNG ĐỎ  ---  CODE BLUE 
    """
    # Hiển thị từng bước của các phép tính, cho debug dễ hơn
    showStep = True
    # 1. Tạo biến mẹ chứa toàn bộ dữ liệu để xuất
    # if f"final_sheet_of_{tenFileDeXuatHienTai}" not in st.session_state:
    #     st.session_state[f"final_sheet_of_{tenFileDeXuatHienTai}"] = pd.DataFrame(columns=["Thứ", "Ngày", "Giờ"])

    # 2. Lấy tên các Cột (Phòng Khám) trong lịch, tương ứng với tên file theo KHTH tenFileDeXuatHienTai
    filtered_PK_theo_KHTH = filtered_PK_theo_ten_file_KHTH(
        tenFileDeXuatHienTai)
    if showStep:
        st.write("filtered_PK_theoyeucau", filtered_PK_theo_KHTH)

    # 3. Lấy sheet lịch tháng
    # get sheet column in full_lich with sheetName = sheetName
    sheetLichThang = st.session_state.full_lich[st.session_state.selected_sheet_name]
    # st.write("st.session_state.full_lich test", st.session_state.full_lich)

    # 3.1 drop 1st row (row 0) because it is "merge cell"
    sheetLichThang = sheetLichThang.drop(0)
    # 4. không cần fillna vì sheet này mình chỉ lấy mỗi S
    """ 4. optional
     loop all 4 first columns in sheetLichThang
        and fillna with above row value if value of that is "nan"
        do not use sheetLichThang.iloc[:, i].fillna(method='ffill') function, just check if value of that is string "nan"
    """
    for i in range(4):
        for j in range(1, len(sheetLichThang)):
            if isinstance(sheetLichThang.iloc[j, i], str):
                if sheetLichThang.iloc[j, i].strip() == "nan":
                    sheetLichThang.iloc[j, i] = sheetLichThang.iloc[j-1, i]
            else:
                if pd.isna(sheetLichThang.iloc[j, i]):
                    sheetLichThang.iloc[j, i] = sheetLichThang.iloc[j-1, i]
    if showStep:
        st.write("#Bảng 4 cột đầu của tháng đã edit", sheetLichThang.iloc[:, 0:4])
    # 6. BIẾN LƯU TRỮ DỮ LIỆU TOÀN BỘ PK XUẤT RA
    # merged_data_ALL_phongkham = pd.DataFrame()

    # 7. Loop qua từng PHÒNG KHÁM ĐỂ LẤY TÊN BÁC SĨ VÀ TẠO FILE
    # filtered_PK_theoyeucau giống st.session_state.ten_PK_theo_KHTH_dict nhưng đã lọc theo file hiện tại của hàm

    # AI return the first 4 columns of sheetLichThang, and columns have the name in filtered_PK_theo_KHTH → save to merged_data_ALL_phongkham
    # Get the first 4 columns of sheetLichThang
    matching_columns = sheetLichThang.columns[:4].tolist() 
    if showStep:
        st.write("matching_columns 1", matching_columns)
    # AI add the columns in filtered_PK_theo_KHTH to matching_columns
    for pk in range(0, len(filtered_PK_theo_KHTH)):
        tenPKTheoLich = filtered_PK_theo_KHTH[pk]['name']
        matching_columns.append(tenPKTheoLich)
    if showStep:
        st.write("matching_columns 2", matching_columns)

    # AI all columns in sheetLichThang that have the name in matching_columns
    all_CLS_data = sheetLichThang[matching_columns].copy()
    if showStep:
        st.markdown("# Merged data of all Phòng Khám theo yêu cầu")
        st.write(all_CLS_data)

    # AI 1 remove columns S
    all_CLS_data = all_CLS_data.drop(columns=["S"])
    if showStep:
        st.markdown("AI remove columns S (số thứ tự)")
        st.write(all_CLS_data)

    # AI 2 from column 4 to the end, rename columns to name_KHTH of filtered_PK_theo_KHTH
    for pk in range(0, len(filtered_PK_theo_KHTH)):
        tenPKTheoLich = filtered_PK_theo_KHTH[pk]['name']
        tenPKCuaKHTH = filtered_PK_theo_KHTH[pk]['name_KHTH']
        all_CLS_data = all_CLS_data.rename(columns={tenPKTheoLich: tenPKCuaKHTH})
        # AI replace value "nan" of column to "", do not use drop nan function
        all_CLS_data[tenPKCuaKHTH] = all_CLS_data[tenPKCuaKHTH].apply(
            lambda x: "" if isinstance(x, str) and x.strip() == "nan" else x
        )
    # SHOW 2
    if showStep:
        st.markdown("rename columns to name_KHTH of filtered_PK_theo_KHTH")
        st.write(all_CLS_data)
    # END 2
    # AI 4: remove row  where "Giờ" is "Tr" in lowercase and reindex all_CLS_data
    all_CLS_data = all_CLS_data[all_CLS_data["Giờ"].str.lower() != "tr"]
    all_CLS_data = all_CLS_data.reset_index(drop=True)
    if showStep:
        st.markdown("remove row where Giờ is Tr")
        st.write(all_CLS_data)
    # AI 5: change value row where "Giờ" S to N and C to Đ
    all_CLS_data["Giờ"] = all_CLS_data["Giờ"].replace({"S": "N", "C": "Đ"})
    if showStep:
        st.markdown('AI 5: change value row where "Giờ" S to N and C to Đ')
        st.write(all_CLS_data)

    # AI 6: function to process value of all_CLS_data[tenPKCuaKHTH]
    # 1. Split the value of all_CLS_data[tenPKCuaKHTH] by "," and strip the value
    # 2. Loop through values and Add "Bs. " to each value of the list and join the list by " - "
    def process_value(value):
        if isinstance(value, str):
            values = [v.strip() for v in value.split(",")]
            if values:
                values = ["Bs. " + v for v in values]
                return " - ".join(values)
        return value

    # AI 7: apply function to all_CLS_data[tenPKCuaKHTH]
    for pk in range(0, len(filtered_PK_theo_KHTH)):
        tenPKCuaKHTH = filtered_PK_theo_KHTH[pk]['name_KHTH']
        all_CLS_data[tenPKCuaKHTH] = all_CLS_data[tenPKCuaKHTH].apply(process_value)

    if showStep:
        st.markdown("AI 7: apply function to all_CLS_data[tenPKCuaKHTH]")
        st.write(all_CLS_data)

    # AI 8: duplicate column tenPKCuaKHTH and rename all two columns to "BÁO ĐỘNG ĐỎ" and "CODE BLUE "
    all_CLS_data[f"BÁO ĐỘNG ĐỎ"] = all_CLS_data[tenPKCuaKHTH]
    all_CLS_data[f"CODE BLUE"] = all_CLS_data[tenPKCuaKHTH]
    all_CLS_data = all_CLS_data.drop(columns=[tenPKCuaKHTH])
    if showStep:
        st.markdown("AI 8: duplicate column tenPKCuaKHTH and rename all two columns to 'BÁO ĐỘNG ĐỎ' and 'CODE BLUE'")
        st.write(all_CLS_data)
        
    # AI final - add all_CLS_data to st.session_state[f"final_sheet_of_{tenFileDeXuatHienTai}"]
    st.session_state[f"final_sheet_of_{tenFileDeXuatHienTai}"] = all_CLS_data
    if showStep:
        st.write(f"✅Xuất xong: {tenFileDeXuatHienTai}✅")
        st.table(st.session_state[f"final_sheet_of_{tenFileDeXuatHienTai}"])


if __name__ == "__main__":
    xuat("1.1 Lịch trực Bệnh viện>CODE BLUE")
