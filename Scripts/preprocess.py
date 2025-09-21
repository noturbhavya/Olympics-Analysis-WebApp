import pandas as pd

def preprocess(df, region_df):
    # Filter only Summer season and create a copy to avoid SettingWithCopyWarning
    df = df[df['Season'] == 'Summer'].copy()
    
    # Merge region data
    df = df.merge(region_df, on='NOC', how='left')
    
    # Drop duplicates
    df.drop_duplicates(inplace=True)
    
    # One-hot encode Medal column (Gold, Silver, Bronze)
    df = pd.concat([df, pd.get_dummies(df['Medal'])], axis=1)
    
    return df
