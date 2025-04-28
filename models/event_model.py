import pandas as pd

def normalize_events(events):
    """
    Takes a list of raw events and returns a cleaned DataFrame.
    """
    # Create DataFrame
    df = pd.DataFrame(events)

    # Fix Data Types safely
    if 'EventID' in df.columns:
        df['EventID'] = pd.to_numeric(df['EventID'], errors='coerce').fillna(0).astype(int)

    if 'Timestamp' in df.columns:
        df['Timestamp'] = pd.to_datetime(df['Timestamp'], errors='coerce')
        df['Timestamp'] = df['Timestamp'].fillna(pd.Timestamp('1970-01-01'))

    # Fill missing text fields
    for column in ['Provider', 'User', 'Message']:
        if column in df.columns:
            df[column] = df[column].fillna('Unknown')

    return df
