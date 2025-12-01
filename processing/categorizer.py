from model.classifier import hybrid_classify

def categorize_df(df):
    df["category"] = df["merchant_clean"].apply(hybrid_classify)
    return df
