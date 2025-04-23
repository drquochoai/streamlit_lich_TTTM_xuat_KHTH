from func.x1_u1_filtered_PK_theoyeucau import filtered_PK_theo_ten_file_KHTH
import streamlit as st
import pandas as pd
def xuat(tenFileDeXuatHienTai):
    """ 
        Xuất file 1.3 Lịch DS BS trả kết quả
        Chỉ xuất theo hàng bác sĩ là được
        Để riêng 1 sheet
    """
    # Hiển thị từng bước của các phép tính, cho debug dễ hơn
    showStep= False
    # 1. Tạo biến mẹ chứa toàn bộ dữ liệu để xuất
    st.session_state[f"final_sheet_of_{tenFileDeXuatHienTai}"] = pd.DataFrame()

    # 2. Lấy tên các Cột (Phòng Khám) trong lịch, tương ứng với tên file theo KHTH tenFileDeXuatHienTai
    filtered_PK_theo_KHTH = filtered_PK_theo_ten_file_KHTH(tenFileDeXuatHienTai)
    # st.write("filtered_PK_theoyeucau", filtered_PK_theo_KHTH)

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
    st.write("#Bảng 4 cột đầu của tháng đã edit", sheetLichThang.iloc[:, 0:4])
    # 6. BIẾN LƯU TRỮ DỮ LIỆU TOÀN BỘ PK XUẤT RA
    merged_data_ALL_phongkham = pd.DataFrame()

    # 7. Loop qua từng PHÒNG KHÁM ĐỂ LẤY TÊN BÁC SĨ VÀ TẠO FILE
    # filtered_PK_theoyeucau giống st.session_state.ten_PK_theo_KHTH_dict nhưng đã lọc theo file hiện tại của hàm
    for pk in range(0, len(filtered_PK_theo_KHTH)):
        # 7.1. Lấy dữ liệu từ selected_sheet_name
        # st.write("st.session_state.full_lich", st.session_state.full_lich)
        sheet = st.session_state.full_lich[st.session_state.selected_sheet_name]
        if showStep:
            st.write("sheet", sheet)
        # 7.2. Lấy cột tên phòng khám
        # get column name of sheet = ten_PK_theo_KHTH_dict[pk]['name'];
        # Exg: PK TM 1 (6h-7h. 7h-16h)(nghỉ 11-12h) ; PK TM 2- suy tim (Bs 6-7h đọc thêm ecg)/nghỉ trua 12-13h
        # st.write("filtered_PK_theo_KHTH", filtered_PK_theo_KHTH)
        tenPKTheoLich = filtered_PK_theo_KHTH[pk]['name']
        tenPKCuaKHTH = filtered_PK_theo_KHTH[pk]['name_KHTH']
        try:
            # 7.3 Lấy cột bác sĩ, của phòng khám từ sheetLichThang
            dataDanhSachBacSi = sheetLichThang[tenPKTheoLich]

            # 7.3.1 ngayUnique = sheetLichThang["Ngày"] không dupicated: mục đích để 1 lát merge ra 1 file theo ngày này để tên bác sĩ map đúng ngày, ngày nào k có tên bác sĩ thì sẽ để tên bs trống
            ngayUnique = sheetLichThang["Ngày"].unique()
            # st.write("ngayUnique", ngayUnique)
            """ 7.4 merge dataDanhSachBacSi with first 4 columns of sheetLichThang
            """
            merged_data_1_phongkham = pd.concat([sheetLichThang.iloc[:, 0:4], dataDanhSachBacSi], axis=1)
            if showStep:
                st.write("7.4 merge dataDanhSachBacSi with first 4 columns of sheetLichThang", merged_data_1_phongkham)

            """ 7.5 Drop row Ten bác sĩ have value is str: "nan" in merged_data_1_phongkham, do not use dropna function
            """
            merged_data_1_phongkham = merged_data_1_phongkham[
                ~merged_data_1_phongkham[tenPKTheoLich].astype(str).str.fullmatch(r"nan")
            ]
            if showStep:
                st.write("7.5 Drop row have value is str", merged_data_1_phongkham)

            # 7.6 merged_data_1_phongkham:
            # Remove duplicate rows of column "Ngày"
            # keep first row where column ~[tenPKTheoLich].astype(str).str.fullmatch(r"nan")
            # First, filter out rows where tenPKTheoLich is "nan"
            merged_data_1_phongkham = merged_data_1_phongkham.drop_duplicates(subset=["Ngày"], keep="first")
            if showStep:
                st.write(" 7.6 Remove duplicate rows keep first", merged_data_1_phongkham)
            # 7.6.1 convert column "Ngày" to datetime format
            merged_data_1_phongkham["Ngày"] = pd.to_datetime(merged_data_1_phongkham["Ngày"], format="mixed", errors="coerce")
            # 7.7 merged_data_1_phongkham to ngayUnique, keep all ngayUnique row, mapping  "Ngày" column
            # Create a DataFrame from ngayUnique as datetime
            ngayUnique = pd.to_datetime(ngayUnique, format="mixed", errors="coerce")
            ngay_df = pd.DataFrame({"Ngày": ngayUnique})
            if showStep:
                st.write("ngay_df", ngay_df)
            # Merge with merged_data_1_phongkham on "Ngày" using a left join
            # This keeps all dates in ngayUnique and maps the corresponding data
            merged_data_1_phongkham = pd.merge(ngay_df, merged_data_1_phongkham, on="Ngày", how="left")

            # Reset the index of the merged DataFrame
            merged_data_1_phongkham.reset_index(drop=True, inplace=True)

            # Display the result after mapping to ngayUnique
            if showStep:
                st.write("7.7 mapped to ngayUnique", merged_data_1_phongkham)

            
            # 7.7 drop column "S" and "Giờ"
            merged_data_1_phongkham = merged_data_1_phongkham.drop(columns=["S", "Giờ"])
            if showStep:
                st.write("7.7 drop column S and Giờ", merged_data_1_phongkham)
            # 7.8 move column "Thứ" to first column
            merged_data_1_phongkham = merged_data_1_phongkham[["Thứ"] + [col for col in merged_data_1_phongkham.columns if col != "Thứ"]]
            # 7.9 if column "Thứ" is empty, fillna with "CN"
            merged_data_1_phongkham["Thứ"] = merged_data_1_phongkham["Thứ"].fillna("CN")
            # 7.10 rename column tenPKTheoLich to tenPKCuaKHTH
            merged_data_1_phongkham = merged_data_1_phongkham.rename(columns={tenPKTheoLich: tenPKCuaKHTH})
            # 7.11 filte nan of column tenPKCuaKHTH to ""
            merged_data_1_phongkham[tenPKCuaKHTH] = merged_data_1_phongkham[tenPKCuaKHTH].fillna("")
            if showStep:
                st.write("7.11 move column Thứ to first column", merged_data_1_phongkham)

            # 7.11.1 add new Ma BS column
            # AI 3 from columns 4 of all_CLS_data: add on the right of each column a new column name Mã BS, value is blank string 
            num_cols = len(merged_data_1_phongkham.columns)
            # We need to process the original columns only, so we'll:
            # 1. Get the original column names up front
            start_col = 2  # Start from the 3rd column (index 2)
            original_columns = merged_data_1_phongkham.columns[start_col:num_cols].tolist()
            # 2. Use enumerate to track our position as we insert
            for offset, col_name in enumerate(original_columns):
                # Calculate position: start at 4 (3+1), then add 2 for each column we've processed
                # because each insertion shifts positions by 1
                insert_pos = start_col+1 + (offset * 2)
                # all_CLS_data.columns._set_name(f"Mã BS", allow_duplicates=True)  # Risky!
                merged_data_1_phongkham.insert(insert_pos, "Mã BS "+ col_name, "")
                # if row of col_name value is not blank, set value of column "Mã BS" to value of st.session_state["ten_"] get row of col_name value
                try:
                    merged_data_1_phongkham["Mã BS " + col_name] = merged_data_1_phongkham.apply(
                    lambda row: st.session_state["ten_danhSachBS"][row[col_name]] if str(row[col_name]).strip() != "" else "",
                    axis=1
                )
                except KeyError:
                    st.warning(f"KeyError: {col_name} not found in st.session_state['ten_danhSachBS']")        
                
            if showStep:
                st.markdown("7.11.1 add on the right of each column a new column name Mã BS, value is blank string")
                st.write(merged_data_1_phongkham)
            # END 3



            # 7.12 add to master mother sheet
            st.session_state[f"final_sheet_of_{tenFileDeXuatHienTai}"] = pd.concat([st.session_state[f"final_sheet_of_{tenFileDeXuatHienTai}"], merged_data_1_phongkham], axis=0)
            if showStep:
                st.write("7.12 add to master mother sheet", st.session_state[f"final_sheet_of_{tenFileDeXuatHienTai}"])
        except KeyError:
            st.warning(f"Không tìm thấy cột {tenPKTheoLich} trong sheet {st.session_state.selected_sheet_name}")
            continue
    st.write(f"✅Xuất xong: {tenFileDeXuatHienTai}✅")

if __name__ == "__main__":
    xuat("1.3 Lịch DS BS trả kết quả")