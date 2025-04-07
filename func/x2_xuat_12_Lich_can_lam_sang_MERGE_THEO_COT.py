from func.x1_u1_filtered_PK_theoyeucau import filtered_PK_theo_ten_file_KHTH
import streamlit as st
import pandas as pd
from SETTINGS_FOR_ALL import SETTINGS

def xuat(tenFileDeXuatHienTai):
    """
        Xuất file "1.2 Lịch Cận lâm sàng"
        Format: 1 ngày 3 hàng giống như xuất phòng khám
        Để riêng 1 sheet
    """
    # Hiển thị từng bước của các phép tính, cho debug dễ hơn
    showStep = False
    # 1. Tạo biến mẹ chứa toàn bộ dữ liệu để xuất
    # if f"final_sheet_of_{tenFileDeXuatHienTai}" not in st.session_state:
    #     st.session_state[f"final_sheet_of_{tenFileDeXuatHienTai}"] = pd.DataFrame(columns=["Thứ", "Ngày", "Giờ"])

    # 2. Lấy tên các Cột (Phòng Khám) trong lịch, tương ứng với tên file theo KHTH tenFileDeXuatHienTai
    filtered_PK_theo_KHTH = filtered_PK_theo_ten_file_KHTH(
        tenFileDeXuatHienTai)
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
        st.markdown("AI remove columns S")
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
        st.markdown("AI remove columns S")
        st.write(all_CLS_data)
    # END 2

    # AI 2.9: --START rearrange all_CLS_data columns from column 3 to the order of SETTINGS["thuTuPhongCanLamSang"]
    # Get the desired column order from SETTINGS
    desired_order = SETTINGS["thuTuPhongCanLamSang"]

    # Get the current columns of the DataFrame
    current_columns = all_CLS_data.columns.tolist()

    # Split columns into:
    # 1. Columns before index 3 (unchanged)
    # 2. Columns from index 3 onward (to be reordered)
    fixed_columns = current_columns[:3]  # Keep first 3 columns as-is
    columns_to_reorder = current_columns[3:]  # Columns to rearrange

    # Reorder columns_to_reorder based on desired_order
    # (Only keep columns that exist in both lists)
    reordered_columns = [col for col in desired_order if col in columns_to_reorder]

    # Combine fixed columns + reordered columns + any remaining columns not in desired_order
    final_columns = fixed_columns + reordered_columns + [
        col for col in columns_to_reorder if col not in desired_order
    ]
    # Apply the new column order to the DataFrame
    all_CLS_data = all_CLS_data[final_columns]

    if showStep:
        st.markdown("Rearranged columns based on SETTING['thuTuPhongCanLamSang']")
        st.write(all_CLS_data)
    # END 2.9

    # AI 3 from columns 4 of all_CLS_data: add on the right of each column a new column name Mã BS, value is blank string 
    num_cols = len(all_CLS_data.columns)
    # We need to process the original columns only, so we'll:
    # 1. Get the original column names up front
    original_columns = all_CLS_data.columns[3:num_cols].tolist()
    # 2. Use enumerate to track our position as we insert
    for offset, col_name in enumerate(original_columns):
        # Calculate position: start at 4 (3+1), then add 2 for each column we've processed
        # because each insertion shifts positions by 1
        insert_pos = 4 + (offset * 2)
        # all_CLS_data.columns._set_name(f"Mã BS", allow_duplicates=True)  # Risky!
        all_CLS_data.insert(insert_pos, "Mã BS "+ col_name, "")
        
    if showStep:
        st.markdown("add on the right of each column a new column name Mã BS, value is blank string")
        st.write(all_CLS_data)
    # END 3
    
    # AI final - add all_CLS_data to st.session_state[f"final_sheet_of_{tenFileDeXuatHienTai}"]
    st.session_state[f"final_sheet_of_{tenFileDeXuatHienTai}"] = all_CLS_data
    # for pk in range(0, len(filtered_PK_theo_KHTH)):
    #     # 7.1. Lấy dữ liệu từ selected_sheet_name
    #     # st.write("st.session_state.full_lich", st.session_state.full_lich)
    #     sheet = st.session_state.full_lich[st.session_state.selected_sheet_name]
    #     if showStep:
    #         st.write("7.1. Lấy dữ liệu từ selected_sheet_name", sheet)
    #     # 7.2. Lấy cột tên phòng khám
    #     # get column name of sheet = ten_PK_theo_KHTH_dict[pk]['name'];
    #     # Exg: PK TM 1 (6h-7h. 7h-16h)(nghỉ 11-12h) ; PK TM 2- suy tim (Bs 6-7h đọc thêm ecg)/nghỉ trua 12-13h
    #     # st.write("filtered_PK_theo_KHTH", filtered_PK_theo_KHTH)
    #     tenPKTheoLich = filtered_PK_theo_KHTH[pk]['name']
    #     tenPKCuaKHTH = filtered_PK_theo_KHTH[pk]['name_KHTH']
    #     if showStep:
    #         st.write("tenPKTheoLich: ", tenPKTheoLich,
    #                  "tenPKCuaKHTH: ", tenPKCuaKHTH)
    #     try:
    #         # 7.3 Lấy cột bác sĩ, của phòng khám từ sheetLichThang
    #         dataDanhSachBacSi = sheetLichThang[tenPKTheoLich]

    #         # 7.3.1 ngayUnique = sheetLichThang["Ngày"] không dupicated: mục đích để 1 lát merge ra 1 file theo ngày này để tên bác sĩ map đúng ngày, ngày nào k có tên bác sĩ thì sẽ để tên bs trống. Chỉ áp dụng cho file có 1 ngày thôi
    #         # ngayUnique = sheetLichThang["Ngày"].unique()
    #         # st.write("ngayUnique", ngayUnique)

    #         # 7.4 merge dataDanhSachBacSi with first 4 columns of sheetLichThang
    #         merged_data_1_phongkham = pd.concat(
    #             [sheetLichThang.iloc[:, 0:4], dataDanhSachBacSi], axis=1)
    #         if showStep:
    #             st.write(
    #                 "7.4 merge dataDanhSachBacSi with first 4 columns of sheetLichThang", merged_data_1_phongkham)

    #         """ 7.5 Drop row Ten bác sĩ have value is str: "nan" in merged_data_1_phongkham, do not use dropna function
    #         """
    #         # merged_data_1_phongkham = merged_data_1_phongkham[
    #         #     ~merged_data_1_phongkham[tenPKTheoLich].astype(str).str.fullmatch(r"nan")
    #         # ]
    #         # if showStep:
    #         #     st.write("7.5 Drop row have value is str", merged_data_1_phongkham)

    #         # 7.6 merged_data_1_phongkham: Chỉ áp dụng cho file có 1 ngày thôi
    #         # Remove duplicate rows of column "Ngày"
    #         # keep first row where column ~[tenPKTheoLich].astype(str).str.fullmatch(r"nan")
    #         # First, filter out rows where tenPKTheoLich is "nan"
    #         # merged_data_1_phongkham = merged_data_1_phongkham.drop_duplicates(subset=["Ngày"], keep="first")
    #         # if showStep:
    #         #     st.write(" 7.6 Remove duplicate rows keep first", merged_data_1_phongkham)

    #         # 7.6.1 convert column "Ngày" to datetime format
    #         merged_data_1_phongkham["Ngày"] = pd.to_datetime(
    #             merged_data_1_phongkham["Ngày"], format="mixed", errors="coerce")
    #         if showStep:
    #             st.write('7.6.1 convert column "Ngày" to datetime format',
    #                      merged_data_1_phongkham)

    #         # 7.7 merged_data_1_phongkham to ngayUnique, keep all ngayUnique row, mapping  "Ngày" column
    #         # Create a DataFrame from ngayUnique as datetime
    #         # ngayUnique = pd.to_datetime(ngayUnique, format="mixed", errors="coerce")
    #         # ngay_df = pd.DataFrame({"Ngày": ngayUnique})
    #         # if showStep:
    #         #     st.write("ngay_df", ngay_df)
    #         # Merge with merged_data_1_phongkham on "Ngày" using a left join
    #         # This keeps all dates in ngayUnique and maps the corresponding data
    #         # merged_data_1_phongkham = pd.merge(ngay_df, merged_data_1_phongkham, on="Ngày", how="left")

    #         # Reset the index of the merged DataFrame
    #         # merged_data_1_phongkham.reset_index(drop=True, inplace=True)

    #         # # Display the result after mapping to ngayUnique
    #         # if showStep:
    #         #     st.write("7.7 mapped to ngayUnique", merged_data_1_phongkham)
    #         # --END-- 7.7 merge theo ngayUnique

    #         # 7.7 drop column "S" and "Giờ"
    #         merged_data_1_phongkham = merged_data_1_phongkham.drop(columns=[
    #                                                                "S"])
    #         if showStep:
    #             st.write("7.7 drop column S and Giờ", merged_data_1_phongkham)
    #         # 7.8 move column "Thứ" to first column
    #         # merged_data_1_phongkham = merged_data_1_phongkham[["Thứ"] + [col for col in merged_data_1_phongkham.columns if col != "Thứ"]]

    #         # # 7.9 if column "Thứ" is empty, fillna with "CN"
    #         # merged_data_1_phongkham["Thứ"] = merged_data_1_phongkham["Thứ"].fillna(
    #         #     "CN")
            
    #         # 7.10 rename column tenPKTheoLich to tenPKCuaKHTH
    #         merged_data_1_phongkham = merged_data_1_phongkham.rename(
    #             columns={tenPKTheoLich: tenPKCuaKHTH})
    #         # 7.11 merged_data_1_phongkham[tenPKCuaKHTH] replace value "nan" of column to "", do not use drop nan function
    #         merged_data_1_phongkham[tenPKCuaKHTH] = merged_data_1_phongkham[tenPKCuaKHTH].apply(
    #             lambda x: "" if isinstance(x, str) and x.strip() == "nan" else x
    #         )

    #         if showStep:
    #             st.write("7.11 replace value nan of column to space, do not use drop nan function",
    #                      merged_data_1_phongkham)

    #         # 7.11 MERGE INTO ONE add to master mother sheet, Theo cột !!
    #         # Set "Thứ" and "Ngày" as index for both DataFrames before concatenation
    #         st.session_state[f"final_sheet_of_{tenFileDeXuatHienTai}"] = st.session_state[f"final_sheet_of_{tenFileDeXuatHienTai}"].merge(
    #             merged_data_1_phongkham,
    #             on=["Thứ", "Giờ", "Ngày"],
    #             how="right"
    #         )
    #         if showStep:
    #             st.write(" 7.11 MERGE INTO ONE add to master mother sheet, Theo cột !!", st.session_state[f"final_sheet_of_{tenFileDeXuatHienTai}"])

    #     except KeyError as e:
    #         st.warning(
    #             f"Không tìm thấy cột {tenPKTheoLich} trong sheet {st.session_state.selected_sheet_name}")
    #         st.warning(e)
    #         st.write(sheetLichThang[tenPKTheoLich])
    #         continue
    st.write(f"✅Xuất xong: {tenFileDeXuatHienTai}✅")
    st.table(st.session_state[f"final_sheet_of_{tenFileDeXuatHienTai}"])


if __name__ == "__main__":
    xuat("1.2 Lịch Cận lâm sàng")
