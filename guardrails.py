def age_filter(df, age):
    allowed_rows = []

    for _, row in df.iterrows():
        cert = str(row.get("Certificate", "")).upper()

        if age < 13:
            if cert in ["G", "PG"]:
                allowed_rows.append(row)

        elif age < 18:
            if cert in ["PG", "PG-13"]:
                allowed_rows.append(row)

        else:
            allowed_rows.append(row)

    return df.loc[[r.name for r in allowed_rows]]