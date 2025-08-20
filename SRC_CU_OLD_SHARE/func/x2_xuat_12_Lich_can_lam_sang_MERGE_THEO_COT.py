from math import e
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
    showStep = True
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
        st.markdown("AI 1 remove columns S")
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
        st.markdown("AI 2 from column 4 to the end, rename columns to name_KHTH of filtered_PK_theo_KHTH")
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
    def add_msnv_tenbacsi(row):
        try:
            # if str(row[col_name]).strip() != "" and str(row[col_name]) in st.session_state["ten_danhSachBS"]:
            #     return st.session_state["ten_danhSachBS"][row[col_name]]
            # else if str(row[col_name]).strip() contain "," inside it, then split by "," then return st.session_state["ten_danhSachBS_shortname"] and then join again by ","
            #    else return ""
            if str(row[col_name]).strip() != "":
                if str(row[col_name]) in st.session_state["ten_danhSachBS"]:
                    return st.session_state["ten_danhSachBS"][row[col_name]]
                elif str(row[col_name]) in st.session_state["ten_danhSachBS_shortname"]:
                    return st.session_state["ten_danhSachBS_shortname"][row[col_name]]
                elif "," in str(row[col_name]):
                # Split by ",", add "BS." to all elements of the list and then join again by ","
                    return ", ".join([f"{st.session_state["ten_danhSachBS_shortname"][item.strip()]}" for item in str(row[col_name]).split(",")])
                else:
                    return ""
            else:
                return ""
        except KeyError:
            st.warning(f"KeyError: {col_name} not found in st.session_state['ten_danhSachBS']")
            return ""

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
        # if row of col_name value is not blank, set value of column "Mã BS" to value of st.session_state["ten_"] get row of col_name value
        try:
            all_CLS_data["Mã BS " + col_name] = all_CLS_data.apply(
                lambda row: add_msnv_tenbacsi(row),
                axis=1
            )
        except KeyError:
            st.warning(f"KeyError: {col_name} not found in st.session_state['ten_danhSachBS']")        
        
    if showStep:
        st.markdown("add on the right of each column a new column name Mã BS, value is blank string")
        st.write(all_CLS_data)
    # END 3
    
    # AI 4: Each column from 4 to the end, check if value in lower is not contain ".", or not contain "bs", or not contain "," then set value of that cell to "BS." + value of that cell
    # write docs for the function
    
    def fix_ten_bacsi(x):
        """
        Hàm fix_ten_bacsi thực hiện chuẩn hóa định dạng tên bác sĩ.
        Tham số:
            x: Dữ liệu đầu vào có thể là kiểu chuỗi.
               Nếu x không phải là chuỗi hoặc là chuỗi rỗng sau khi loại bỏ khoảng trắng,
               hàm trả về x không thay đổi.
               Nếu x là chuỗi:
                 - Nếu chuỗi không chứa dấu chấm ('.'), không chứa chuỗi 'bs' và không chứa dấu phẩy (','),
                   hàm sẽ thêm tiền tố 'BS. ' vào trước chuỗi.
                 - Nếu chuỗi chứa dấu phẩy (','), hàm sẽ tách chuỗi theo dấu phẩy,
                   thêm 'BS. ' vào đầu mỗi đoạn sau khi loại bỏ khoảng trắng thừa,
                   và nối lại các phần với nhau bằng dấu phẩy.
                 - Trường hợp khác (đã có sẵn định dạng), trả về x ban đầu.
        Trả về:
            Chuỗi đã được chuẩn hóa định dạng tên bác sĩ hoặc giá trị x ban đầu nếu không phải chuỗi hợp lệ.
        """
        
        if isinstance(x, str) and x.strip() != "":
            if (("." in x.lower()) or ("bs" in x.lower())) and x in st.session_state["ten_danhSachBS_tenbstheokhth"]:
                return st.session_state["ten_danhSachBS_tenbstheokhth"][x]
            elif ("." not in x.lower()) and ("bs" not in x.lower()) and ("," not in x.lower()):
                return "BS. " + x
            elif ("," in x.lower()):
                # Split by ",", add "BS." to all elements of the list and then join again by ","
                return ", ".join([f"BS. {item.strip()}" for item in x.split(",")])
            else:
                return x
        else:
            return x
    for col in all_CLS_data.columns[3:]:
        if not col.startswith("Mã BS"):
            all_CLS_data[col] = all_CLS_data[col].apply(lambda x: fix_ten_bacsi(x))
    if showStep:
        st.markdown("AI 4: Each column from 4 to the end, check if value in lower is not contain '.', or not contain 'bs', or not contain ',' then set value of that cell to 'BS.' + value of that cell")
        st.write(all_CLS_data)

    # AI final - add all_CLS_data to st.session_state[f"final_sheet_of_{tenFileDeXuatHienTai}"]
    st.session_state[f"final_sheet_of_{tenFileDeXuatHienTai}"] = all_CLS_data


    st.write(f"✅Xuất xong: {tenFileDeXuatHienTai}✅")
    st.table(st.session_state[f"final_sheet_of_{tenFileDeXuatHienTai}"])


if __name__ == "__main__":
    xuat("1.2 Lịch Cận lâm sàng")
