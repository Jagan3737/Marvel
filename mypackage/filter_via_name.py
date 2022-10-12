def filter_character_data_via_name(df, column, value):
    filtered_data_df = df[df[column].str.contains(value, case=False, na=False)]
    return filtered_data_df