import pandas as pd

def filter_events(df, event_id=None, provider=None, start_time=None, end_time=None):
    """
    Filters the event dataframe based on given parameters.

    Args:
        df (DataFrame): The events dataframe.
        event_id (int, optional): Filter by specific EventID.
        provider (str, optional): Filter by Provider name.
        start_time (str, optional): Start of time range (ISO format).
        end_time (str, optional): End of time range (ISO format).

    Returns:
        DataFrame: Filtered events dataframe.
    """

    filtered_df = df.copy()

    if event_id is not None:
        filtered_df = filtered_df[filtered_df['EventID'] == event_id]

    if provider is not None:
        filtered_df = filtered_df[filtered_df['Provider'].str.lower() == provider.lower()]

    if start_time is not None:
        filtered_df = filtered_df[filtered_df['Timestamp'] >= pd.to_datetime(start_time)]

    if end_time is not None:
        filtered_df = filtered_df[filtered_df['Timestamp'] <= pd.to_datetime(end_time)]

    return filtered_df
