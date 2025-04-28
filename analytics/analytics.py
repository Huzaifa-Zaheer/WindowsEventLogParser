import pandas as pd
from tabulate import tabulate

def events_per_provider(df):
    provider_counts = df['Provider'].value_counts()
    print("\n=== Events Per Provider ===")
    print(tabulate(provider_counts.reset_index(), headers=['Provider', 'Event Count'], tablefmt="grid"))

def most_frequent_event_ids(df):
    eventid_counts = df['EventID'].value_counts()
    print("\n=== Most Frequent Event IDs ===")
    print(tabulate(eventid_counts.reset_index(), headers=['EventID', 'Count'], tablefmt="grid"))

def events_over_time(df):
    df['Date'] = pd.to_datetime(df['Timestamp']).dt.date
    date_counts = df['Date'].value_counts().sort_index()
    print("\n=== Events Over Time (Daily) ===")
    print(tabulate(date_counts.reset_index(), headers=['Date', 'Event Count'], tablefmt="grid"))
