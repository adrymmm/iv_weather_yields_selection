def build_non_linear_feats(X, quantiles =(0.25, 0.5, 0.75)):
    """ Returns polynomial, hinge and absolute value transformations for a
    dataframe X"""
    cols = X.columns
    for col in cols:
        # Polynomials
        X[f'{col}__sq'] = X[col] ** 2
        X[f'{col}__cu'] = X[col] ** 3
        # Absolute value
        X[f"{col}__abs"] = X[col].abs()
    
    new_cols = {}
    
    for col in cols:
        x = X[col]
        # Iterating over quantiles
        for q in quantiles:
            # Cutting at quantile q
            c = x.quantile(q)
            new_cols[f"{col}__hinge_pos_q{int(q*100)}"] = (x - c).clip(lower=0)
            new_cols[f"{col}__hinge_neg_q{int(q*100)}"] = (c - x).clip(lower=0)
    
    X_transformed = pd.concat([X, pd.DataFrame(new_cols, index=X.index)], axis=1)
    return X_transformed
