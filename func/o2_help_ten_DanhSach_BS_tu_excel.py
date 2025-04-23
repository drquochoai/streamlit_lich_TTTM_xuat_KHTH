import streamlit as st
import pandas as pd
from SETTINGS_FOR_ALL import SETTINGS

sheetNamedefault = SETTINGS.get("sheetName", {}).get("danhSachBacSi")

@st.cache_data
def xuLyTenDanhSachBS(full_lich, sheetName=sheetNamedefault):
    """
    Extract data from the sheet "danhsachbacsi" and return a dictionary containing the "nameBS" and "msnv" from columns 1 and 2.
    """
    # get data of the sheet default phongKham
    ten_danhSachBSFull = full_lich[sheetName]

    # ten_danhSachBS: drop columns where the first row value is nan, use != 'nan' instead of dropna
    ten_danhSachBSFull = ten_danhSachBSFull.loc[:, ten_danhSachBSFull.iloc[0].astype(str) != "nan"]
    
    # print(ten_danhSachBS)
    # set 2st row as header
    ten_danhSachBSFull.columns = ten_danhSachBSFull.iloc[0]
    
    # drop first row and second row (row 0) because it is "code"

    # Drop the first two rows as they contain "code"
    ten_danhSachBSFull = ten_danhSachBSFull.iloc[1:]
    # now ten_danhSachBSFull has 3 columns: "tenbs" and "msnv" and "shortname"
    # turn into dictionary with key = "nameBS", value = "msnv" and save to ten_danhSachBS
    ten_danhSachBS = ten_danhSachBSFull.set_index("tenbs")["msnv"].to_dict()
    # turn into dictionary with key = "shortname", value = "msnv" and save to ten_danhSachBS_shortname
    ten_danhSachBS_shortname = ten_danhSachBSFull.set_index("shortname")["msnv"].to_dict()
    # turn into dictionary with key = "shortname", value = "msnv" and save to ten_danhSachBS_shortname
    ten_danhSachBS_tenbstheokhth = ten_danhSachBSFull.set_index("tenbs")["tenbstheokhth"].to_dict()
    # turn into dictionary with key = "shortname", value = "msnv" and save to ten_danhSachBS_shortname
    ten_danhSachBS_tenbstheokhth_msnv = ten_danhSachBSFull.set_index("tenbstheokhth")["msnv"].to_dict()
    # print(ten_danhSachBS)
    st.session_state.ten_danhSachBS = ten_danhSachBS
    st.session_state.ten_danhSachBS_shortname = ten_danhSachBS_shortname
    st.session_state.ten_danhSachBS_tenbstheokhth = ten_danhSachBS_tenbstheokhth
    st.session_state.ten_danhSachBS_tenbstheokhth_msnv = ten_danhSachBS_tenbstheokhth_msnv
    # st.write("ten_danhSachBS", st.session_state)
    return ten_danhSachBS

if __name__ == "__main__":
    # Test the function with a sample DataFrame
    sample_data = {
        "HoTen": ["Nguyen Van A", "Tran Thi B", "Le Van C"],
        "MSVN": ["123456", "654321", "789012"],
    }
    sample_df = pd.DataFrame(sample_data)
    result = xuLyTenDanhSachBS(sample_df)
    print(result)