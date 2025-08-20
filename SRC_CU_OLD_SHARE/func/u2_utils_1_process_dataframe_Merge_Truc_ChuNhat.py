import pandas as pd
import streamlit as st
import pandas as pd

def merge_dataframes_tenBS_NgayDem(all_CLS_data, getAndMergeCN, merge_cols=["Thứ", "Ngày", "Giờ"]):
    """
    Merges two pandas DataFrames based on specified columns and updates 
    overlapping columns in the first DataFrame with values from the second.

    Args:
        all_CLS_data (pd.DataFrame): The primary DataFrame to be updated.
        getAndMergeCN (pd.DataFrame): The DataFrame containing the new values.
        merge_cols (list): A list of column names to use for merging.
                           Defaults to ["Thứ", "Ngày", "Giờ"].

    Returns:
        pd.DataFrame: A new DataFrame with the merged data.  Returns the original
                     `all_CLS_data` if `getAndMergeCN` is empty.  Returns the 
                     original `all_CLS_data` if `merge_cols` are not present in both 
                     dataframes.
    """

    # Check if the secondary dataframe is empty.  If so, return the original dataframe
    if getAndMergeCN.empty:
        print("Warning: getAndMergeCN is empty. Returning original all_CLS_data.")
        return all_CLS_data
    
    # Check if the merge columns are present in both dataframes. If not, warn and return
    if not all(col in all_CLS_data.columns for col in merge_cols) or not all(col in getAndMergeCN.columns for col in merge_cols):
        print("Warning: Not all merge columns are present in both dataframes. Returning original all_CLS_data.")
        return all_CLS_data

    # Identify overlapping columns (excluding merge columns)
    overlapping_cols = list(set(all_CLS_data.columns) & set(getAndMergeCN.columns) - set(merge_cols))

    # Create a copy to avoid modifying the original DataFrame in place
    merged_df = all_CLS_data.copy()

    # Merge the dataframes based on the specified columns
    merged = pd.merge(merged_df, getAndMergeCN, on=merge_cols, how='left', suffixes=('_left', '_right'))

    # Update the overlapping columns in merged_df with values from getAndMergeCN
    for col in overlapping_cols:
        merged[col] = merged[f'{col}_right'].fillna(merged[f'{col}_left'])
        merged_df[col] = merged[col]

    # Remove the temporary columns created by the merge
    cols_to_drop = [col for col in merged.columns if col.endswith('_left') or col.endswith('_right')]
    merged = merged.drop(columns=cols_to_drop)
    merged_df = merged.copy()

    return merged_df


if __name__ == "__main__":

    # Example usage (assuming you have DataFrames named all_CLS_data and getAndMergeCN):
    # Sample DataFrames (replace with your actual data)
    data1 = {'Thứ': [1, 2, 3, 1, 2], 
            'Ngày': [10, 11, 12, 10, 11],
            'Giờ': [8, 9, 10, 11, 12],
            'Value1': ['A', 'B', 'C', 'D', 'E'],
            'Value2': [1, 2, 3, 4, 5]}
    all_CLS_data = pd.DataFrame(data1)

    data2 = {'Thứ': [1, 2, 1],
            'Ngày': [10, 11, 10],
            'Giờ': [8, 9, 11],
            'Value1': ['X', 'Y', 'Z'],
            'Value2': [10, 20, 30]}
    getAndMergeCN = pd.DataFrame(data2)

    merged_df = merge_dataframes_tenBS_NgayDem(all_CLS_data, getAndMergeCN)
    print(merged_df)


    # Example with empty getAndMergeCN
    empty_df = pd.DataFrame()
    merged_df_empty = merge_dataframes_tenBS_NgayDem(all_CLS_data, empty_df)
    print("\nMerged with empty DataFrame:")
    print(merged_df_empty)

    # Example with missing merge columns
    data3 = {'Day': [1, 2, 3], 'Value1': ['P', 'Q', 'R']}  # 'Day' instead of 'Ngày'
    missing_merge_cols_df = pd.DataFrame(data3)
    merged_df_missing_cols = merge_dataframes_tenBS_NgayDem(all_CLS_data, missing_merge_cols_df)
    print("\nMerged with missing columns:")
    print(merged_df_missing_cols)