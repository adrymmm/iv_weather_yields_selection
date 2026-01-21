# Generalised demeaning helper function
def demean_2FE(df):
    """ Returns a dataframe with demeaned data, both entity and time"""
    # Copying dataframe
    df_fe = df.copy()
    # Looping over all columns
    for col in df.columns:
        # Grouping by FE type and and create mean vector
        e_mean = df_fe[col].groupby(level='entity_id').transform('mean')
        t_mean = df_fe[col].groupby(level='year').transform('mean')
        total_mean = df_fe[col].mean()
        # Demeaning
        df_fe[col] = df_fe[col] - e_mean - t_mean + total_mean
    return df_fe