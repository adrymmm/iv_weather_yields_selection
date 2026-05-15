from sklearn.utils.validation import check_is_fitted

def demean_2FE(df, max_iter=200, tol=1e-6):
    """ Returns a dataframe with demeaned data, both entity and time"""
    df_fe = df.astype(float).copy()
    for _ in range(max_iter):
        prev = df_fe.copy()
        for col in df_fe.columns:
            df_fe[col] -= df_fe[col].groupby(level='entity_id').transform('mean')
            df_fe[col] -= df_fe[col].groupby(level='year').transform('mean')
        if (df_fe - prev).abs().max().max() < tol:
            break
    return df_fe