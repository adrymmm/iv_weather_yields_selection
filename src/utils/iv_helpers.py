def feat_name(feat):
    """ Returns the linear non-transformed name """
    return feat.split("__")[0]

def feat_transformation(feat):
    """ Returns the kind of transformation of the column """
    if '__hinge' in feat: return "hinge"
    if feat.endswith('__cu'): return "cubic"
    if feat.endswith('__abs'): return "abs"
    if feat.endswith('__sq'): return 'square'
    return 'linear'

def hinge_quartile_search(feat):
    """ Returns the quartile of the hinge column"""
    search = re.search(r'q(\d+)', feat)
    return int(search.group(1)) if search else None


def drop_month_family(cols, base):
    return [c for c in cols if not c.startswith(base)]

def controls_temp(m):
    base = f"Z_temp_m{m}"
    other_temp = drop_month_family(temp_months, base)

    near = []
    for k in [m-1, m, m+1]:
        basep = f"Z_prcp_m{k}"
        near += [c for c in prcp_months if c.startswith(basep)]
    return other_temp + near

def controls_prcp(m):
    base = f"Z_prcp_m{m}"
    other_prcp = drop_month_family(prcp_months, base)

    near = []
    for k in [m-1, m, m+1]:
        baset = f"Z_temp_m{k}"
        near += [c for c in temp_months if c.startswith(baset)]
    return other_prcp + near

def excl_test(df, y, endog, Z, controls=None, fe_entity='entity_id', fe_time='year'):
    if controls is None:
        controls = []
    if isinstance(controls, str):
        controls = [controls]

    base_month = Z.split("__")[0]
    controls = [c for c in controls if not c.startswith(base_month)]

    fe_part = f'C({fe_entity}) + C({fe_time})'
    base = f"{y}~ 1 + {fe_part} + [{endog} ~ {Z}]"
    stress = base + (" + " + " + ".join(controls) if len(controls) else "")

    cols_needed = [y, endog, Z, fe_entity, fe_time] + controls
    df_use = df.dropna(subset=cols_needed).copy()

    res_base = IV2SLS.from_formula(
    base,
    data=df_use,
    ).fit(cov_type="clustered", clusters=df_use[fe_entity])

    res_stress = IV2SLS.from_formula(
    stress,
    data=df_use,
    ).fit(cov_type="clustered", clusters=df_use[fe_entity])

    comparison = {
    "baseline_beta": res_base.params[endog],
    "baseline_se": res_base.std_errors[endog],
    "stress_beta": res_stress.params[endog],
    "stress_se": res_stress.std_errors[endog],
    }
    print(f"\nExclusion restriction stress test for {Z}")
    print("-" * 38)
    print(f"Baseline:  β = {comparison['baseline_beta']:.3f} "
          f"(SE = {comparison['baseline_se']:.3f})")
    print(f"Stress:    β = {comparison['stress_beta']:.3f} "
          f"(SE = {comparison['stress_se']:.3f})\n")
