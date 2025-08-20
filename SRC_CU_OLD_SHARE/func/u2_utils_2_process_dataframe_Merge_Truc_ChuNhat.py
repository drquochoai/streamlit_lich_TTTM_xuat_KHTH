import pandas as pd
import streamlit as st
def process_value_bacsi(value):
    if isinstance(value, str):
        values = [v.strip() for v in value.split(",")]
        if values:
            values = ["Bs. " + v for v in values]
            return " - ".join(values)
    return value

def process_dataframe_Merge_Truc_co_SangChieu(df, name_of_column="TenBS"):
    """
    Finds duplicate rows with "Thứ" as "CN" and same "Ngày", merges "TenBS" values,
    and returns a DataFrame with one row per merged group with "Giờ" as "C".

    Args:
        df (pd.DataFrame): Input DataFrame with columns "Thứ", "Ngày", "Giờ", "TenBS".

    Returns:
        pd.DataFrame: Processed DataFrame with merged "TenBS" and "Giờ" as "C" for duplicates.
    """

    # 1. Filter rows where "Thứ" is "CN"
    df_cn = df

    if df_cn.empty:
        return pd.DataFrame(columns=df.columns) # Return empty DataFrame if no "CN" rows

    # 2. Identify duplicate "Ngày" within "CN" rows
    duplicate_ngay = df_cn[df_cn.duplicated(subset=['Ngày'], keep=False)]

    if duplicate_ngay.empty:
        return pd.DataFrame(columns=df.columns) # Return empty DataFrame if no duplicate "Ngày" in "CN" rows


    def merge_tenbs(group):
        """Merges 'TenBS' for 'S' and 'C' Giờ in a group, prioritizing 'C' Giờ row."""
        tenbs_s = group[group["Giờ"] == "S"][name_of_column].to_string(index=False, header=False)
        if len(tenbs_s) > 0:
            tenbs_s = "Ngày: " + process_value_bacsi(tenbs_s)
        else:
            tenbs_s = ""
        tenbs_c = group[group["Giờ"] == "C"][name_of_column].to_string(index=False, header=False)
        if len(tenbs_c) > 0:
            tenbs_c = "Đêm: " + process_value_bacsi(tenbs_c)
        else:
            tenbs_c = ""
        # st.write("tenbs_s", tenbs_s)
        # st.write("tenbs_c", tenbs_c)
        if not tenbs_s: # If no "S", but has "C" (unlikely case based on problem description, but handle it)
            merged_tenbs = tenbs_c
        else:
            merged_tenbs = tenbs_s + "; " + tenbs_c # Join C first then S, if both exist
        if not tenbs_c: # If no "C", but has "S" (unlikely case based on problem description, but handle it)
            merged_tenbs = tenbs_s

        # Prioritize row with "Giờ" as "C" if exists, otherwise take first row (should have "S" in unlikely case)
        row_c = group[group["Giờ"] == "C"]
        if not row_c.empty:
            first_row = row_c.iloc[0].copy() # Take the first "C" row if multiple
            first_row[name_of_column] = merged_tenbs
            first_row["Giờ"] = "C" # Ensure "Giờ" is "C"
            return first_row
        else: # In unlikely case no "C" row (but duplicated day, meaning there must be "S" row)
            first_row = group.iloc[0].copy() # Take the first row (should be "S")
            first_row[name_of_column] = merged_tenbs
            first_row["Giờ"] = "C" # Still return "C" as requested, even though original was "S".  Adjust if different logic needed for this edge case.
            return first_row


    # 3. Group by "Ngày" and apply merge_tenbs function
    merged_rows = duplicate_ngay.groupby("Ngày").apply(merge_tenbs).reset_index(drop=True)

    # 4. Return the merged rows
    return merged_rows


if __name__ == "__main__":
    # Example Usage:
    data = {'Thứ': ['T2', 'CN', 'CN', 'T3', 'CN', 'T4', 'CN'],
            'Ngày': ['01/01/2024', '07/01/2024', '07/01/2024', '08/01/2024', '14/01/2024', '15/01/2024', '14/01/2024'],
            'Giờ': ['S', 'S', 'C', 'S', 'S', 'S', 'C'],
            'TenBS': ['BS.A', 'BS.B', 'BS.C', 'BS.D', 'BS.E', 'BS.F', 'BS.G']}
    df = pd.DataFrame(data)

    result_df = process_dataframe_Merge_Truc_co_SangChieu(df)
    st.table(data)
    st.write(result_df)