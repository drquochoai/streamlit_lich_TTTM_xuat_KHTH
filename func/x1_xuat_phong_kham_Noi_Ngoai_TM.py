import pandas as pd
import streamlit as st
from func.o1_help_ten_PK_theo_KHTH import xuLyTenDanhSachPK
from SETTINGS_FOR_ALL import SETTINGS
from func.x1_u1_filtered_PK_theoyeucau import filtered_PK_theo_ten_file_KHTH


def xuatPhongKham(tenFileDeXuatHienTai):
    """ 
        Hàm mẹ gọi tenPKHienTai
        filtered_PK_theoyeucau = Lọc các hàng nào trong st.session_state.ten_PK_theo_KHTH_dict có file_sheet_name bằng với tenPKHienTai
        Loop qua từng giá trị của filtered_PK_theoyeucau
        và xử lý các giá trị trong từng hàng

        Xuất phòng khám theo tên sheet.
        Args:
            sheetName (str): Tên sheet có tháng, ví dụ Tháng 05/2025.
    """
    # 1. Tạo biến mẹ chứa toàn bộ dữ liệu để xuất
    # st.session_state[f"final_sheet_of_{tenFileDeXuatHienTai}"] = pd.DataFrame()

    # 2.     # 2. Lấy tên các Cột (Phòng Khám) trong lịch, tương ứng với tên file theo KHTH tenFileDeXuatHienTai  = Lọc các hàng nào trong st.session_state.ten_PK_theo_KHTH_dict có file_sheet_name bằng với tenPKHienTai
    filtered_PK_theoyeucau = filtered_PK_theo_ten_file_KHTH(
        tenFileDeXuatHienTai)
    # st.write("filtered_PK_theoyeucau", filtered_PK_theoyeucau)

    # 3. Lấy sheet lịch tháng
    # get sheet column in full_lich with sheetName = sheetName
    # st.write("st.session_state.full_lich test", st.session_state.full_lich)
    sheetLichThang = st.session_state.full_lich[st.session_state.selected_sheet_name]
    # drop 1st row (row 0) because it is "merge cell"
    sheetLichThang = sheetLichThang.drop(0)
    # fillna of first 4 column with above row value
    # sheetLichThang.iloc[:, 0:4] = sheetLichThang.iloc[:, 0:4].fillna(method='ffill')
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
    # st.table(sheetLichThang.iloc[:, 0:4])

    # Hàm để tính cột Từ giờ, Đến giờ trong lịch
    def calculate_timestring(row):
        time_key = "time_" + row["timecode"]
        # st.write("filtered_PK_theoyeucau[ii] time_key:", st.session_state.ten_PK_theo_KHTH_dict[ii])
        timestring = filtered_PK_theoyeucau[ii].get(time_key, "")
        if timestring == "0":
            # st.write(f"{row.name}", "timestring: 0 number")
            return [0, 0]
        elif timestring == "cả ngày":
            # Chỉ xuất theo hàng bác sĩ là được
            # Để riêng 1 sheet
            return [0, 24]
        elif "-" in timestring:
            val1, val2 = timestring.split("-")
            # print(val1)
            # if val1, val2 not contain ":" return [int(val1) if val1.isdigit() else val1, int(val2) if val2.isdigit() else val2] else return val1, val2
            if ":" in val1 or ":" in val2:
                # print("gia tri", [str(val1), str(val2)])
                return [str(val1), str(val2)]
            # oneline return if val1.isdigit(): int(val1) else val1 and val2 same
            else:
                return [int(val1) if val1.isdigit() else val1, int(val2) if val2.isdigit() else val2]
        else:
            return ["0*error", "0*error"]

    # Hàm mapping Tên bác sĩ với mã bác sĩ
    def map_bacsi(row):
        # st.write("row", row)
        ten_bac_si = row["Họ Tên Bác sĩ"]
        # get value of "MSVN" in ten_danhSachBS
        msvn = st.session_state.ten_danhSachBS[ten_bac_si]
        # print("map_bacsi", st.session_state.ten_danhSachBS[ten_bac_si])
        return msvn
    # 6. BIẾN LƯU TRỮ DỮ LIỆU TOÀN BỘ PK XUẤT RA
    merged_data_ALL_phongkham = pd.DataFrame()

    # 7. Loop qua từng PHÒNG KHÁM ĐỂ LẤY TÊN BÁC SĨ VÀ TẠO FILE
    # filtered_PK_theoyeucau giống st.session_state.ten_PK_theo_KHTH_dict nhưng đã lọc theo file hiện tại của hàm
    for ii in range(0, len(filtered_PK_theoyeucau)):

        # 7.1. Lấy cột tên phòng khám
        # get column name of sheet = ten_PK_theo_KHTH_dict[i]['name'];
        # Exg: PK TM 1 (6h-7h. 7h-16h)(nghỉ 11-12h) ; PK TM 2- suy tim (Bs 6-7h đọc thêm ecg)/nghỉ trua 12-13h
        # st.write("filtered_PK_theoyeucau", filtered_PK_theoyeucau)
        tenPKTheoLich = filtered_PK_theoyeucau[ii]['name']
        tenPKCuaKHTH = filtered_PK_theoyeucau[ii]['name_KHTH']
        # get data of sheet with column name = column_name
        try:
            dataDanhSachBacSi = sheetLichThang[tenPKTheoLich]
            # st.write(dataDanhSachBacSi)
            # dataDanhSachBacSi.columns = dataDanhSachBacSi.columns.astype(str)
            # dataDanhSachBacSi = dataDanhSachBacSi.drop(0)

            # st.write(dataDanhSachBacSi)
            """ Drop row have value is str: "nan" in dataDanhSachBacSi, do not use dropna function
            """
            # Filter out rows where any value is the string "nan"
            # st.write(dataDanhSachBacSi)
            # dataDanhSachBacSi = dataDanhSachBacSi[~dataDanhSachBacSi.astype(str).str.contains("nan")]
            """ merge dataDanhSachBacSi with first 4 columns of sheetLichThang
            """
            merged_data_1_phongkham = pd.concat(
                [sheetLichThang.iloc[:, 0:4], dataDanhSachBacSi], axis=1)

            """ Drop row have value is str: "nan" in merged_data_1_phongkham, do not use dropna function
            """
            # st.write(merged_data_1_phongkham[tenPKTheoLich])
            merged_data_1_phongkham = merged_data_1_phongkham[
                ~merged_data_1_phongkham[tenPKTheoLich].astype(
                    str).str.fullmatch(r"nan")
            ]
            # st.write(merged_data_1_phongkham)
            """ 
            in merged_data: create some columns with
                for each dulieu1 of SETTINGS['cauTrucCotFilePhongKhamGuiKHTH']
                    create column with name = col,
                    if value is not null, set all value of that column as value
                    else I will calculate value of that column
              """
            for dulieu1 in SETTINGS['cauTrucCotFilePhongKhamGuiKHTH']:
                col_name = dulieu1.get('col')
                if col_name:
                    if 'value' in dulieu1 and dulieu1['value'] is not None:
                        merged_data_1_phongkham[col_name] = dulieu1['value']
                    else:
                        """ 
                         Xử lý cột Phòng khám = tenPKCuaKHTH
                        """
                        if col_name == "Phòng khám":
                            merged_data_1_phongkham[col_name] = tenPKCuaKHTH
                            """
                            Xử lý cột Họ Tên Bác sĩ = giá trị của cột tenPKTheoLich (tương ứng tên bác sĩ)

                            """
                        elif col_name == "Họ Tên Bác sĩ":
                            merged_data_1_phongkham[col_name] = merged_data_1_phongkham[tenPKTheoLich]
                            # lamda function that replace value of each row (as ten_bac_si) in merged_data_1_phongkham[tenPKTheoLich] "Họ Tên Bác sĩ" with st.session_state.ten_danhSachBS_tenbstheokhth[ten_bac_si]
                            
                            merged_data_1_phongkham[col_name] = merged_data_1_phongkham[col_name].apply(
                                lambda ten_bac_si: st.session_state.ten_danhSachBS_tenbstheokhth.get(ten_bac_si, ten_bac_si)
                            )

                            """
                            Xử lý cột Ngày:
                                - Là ngày ở cột Ngày

                            """
                        elif col_name == "Ngày":
                            oldNgay = pd.to_datetime(
                                merged_data_1_phongkham["Ngày"])
                            merged_data_1_phongkham[col_name] = oldNgay

                        elif col_name == "Từ giờ":
                            """
                            timecode = get value of "Giờ" in merged_data_1_phongkham[col_name] to lowercase
                            timestring = get value of that ten_PK_theo_KHTH_dict[i]["time_"+timecode ]
                                split timestring by "-" and get first value
                            """
                            # set this column to mixed type
                            # merged_data_1_phongkham[col_name] = merged_data_1_phongkham[col_name].astype(str)
                            timecode = merged_data_1_phongkham["Giờ"].str.lower()
                            merged_data_1_phongkham["timecode"] = timecode
                            # create new column "timestring" in merged_data_1_phongkham with function to calculate base on timecode
                            merged_data_1_phongkham[col_name] = merged_data_1_phongkham.apply(
                                lambda row: calculate_timestring(row)[0], axis=1
                            )
                        elif col_name == "Đến giờ":
                            merged_data_1_phongkham[col_name] = merged_data_1_phongkham.apply(
                                lambda row: calculate_timestring(row)[1], axis=1
                            )

                        elif col_name == "Mã Bác sĩ":
                            # set value of column "Mã Bác sĩ" = value of "Họ Tên Bác sĩ" in dictionary st.session_state.ten_danhSachBS[ten_bac_si] as number
                            merged_data_1_phongkham[col_name] = merged_data_1_phongkham["Họ Tên Bác sĩ"].apply(
                                lambda ten: int(st.session_state.ten_danhSachBS_tenbstheokhth_msnv.get(ten, 0))
                            )
                                

                        else:
                            # check if col_name is in merged_data_1_phongkham.columns
                            # if not, create column with name = col_name
                            if col_name not in merged_data_1_phongkham.columns:
                                merged_data_1_phongkham[col_name] = ""

            # in merged_data_1_phongkham, drop columns: timecode, Unnamed: 0, Thứ, Ngày
            merged_data_1_phongkham = merged_data_1_phongkham.drop(
                columns=["timecode", "Unnamed: 0", "Thứ", "Ngày", "Giờ", tenPKTheoLich, "S"], errors="ignore")

            # st.write("merged_data_1_phongkham before drop", merged_data_1_phongkham)
            # # merged_data_1_phongkham remove row have value in column "Tu giờ" = "0*error" or "0"
            # merged_data_1_phongkham = merged_data_1_phongkham[~merged_data_1_phongkham["Từ giờ"].astype(
            #     str).str.contains("0*error|0")]
            # st.write("merged_data_1_phongkham after drop", merged_data_1_phongkham)
            # merged_data_1_phongkham drop column ["Từ giờ"] = 0  and ["Đến giờ"] = 0
            merged_data_1_phongkham = merged_data_1_phongkham[
                (merged_data_1_phongkham["Từ giờ"] != 0) & (merged_data_1_phongkham["Đến giờ"] != 0)]

            # merge tin to merged_data_ALL_phongkham
            merged_data_ALL_phongkham = pd.concat(
                [merged_data_ALL_phongkham, merged_data_1_phongkham], axis=0)

            # st.write(f"merged_data_1_phongkham {tenPKTheoLich}", merged_data_1_phongkham)
        except:
            continue
        #
    st.session_state[f"final_sheet_of_{tenFileDeXuatHienTai}"] = merged_data_ALL_phongkham
    # st.write(f"merged_data_ALL_phongkham {tenPKTheoLich}", merged_data_ALL_phongkham)
    st.write(f"✅Xuất xong: {tenFileDeXuatHienTai}✅")


