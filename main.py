from parsers.parser import parse_events
from models.event_model import normalize_events
from filters.filter import filter_events
from tabulate import tabulate
from analytics.analytics import events_per_provider, most_frequent_event_ids, events_over_time


def main():
    print("Welcome to Windows Event Log Parser!")

    evtx_file = "data/sample.evtx"
    events = parse_events(evtx_file)

    print(f"Total Events Parsed: {len(events)}")

    # Normalize and create DataFrame
    event_df = normalize_events(events)

    print("\nFirst 5 normalized events:")
    print(tabulate(event_df.head(), headers='keys', tablefmt='fancy_grid'))

    # Ask user if they want to apply filters
    choice = input("\nDo you want to apply filters? (yes/no): ").strip().lower()

    if choice == 'yes':
        event_id = input("Enter Event ID to filter (or press Enter to skip): ")
        event_id = int(event_id) if event_id else None

        provider = input("Enter Provider name to filter (or press Enter to skip): ")
        provider = provider if provider else None

        start_time = input("Enter Start Time (YYYY-MM-DD format) (or press Enter to skip): ")
        start_time = start_time if start_time else None

        end_time = input("Enter End Time (YYYY-MM-DD format) (or press Enter to skip): ")
        end_time = end_time if end_time else None

        filtered_df = filter_events(event_df, event_id, provider, start_time, end_time)

        print(f"\nTotal Events After Filtering: {len(filtered_df)}")
        print(tabulate(filtered_df.head(), headers='keys', tablefmt='fancy_grid'))

    else:
        print("\nSkipping filtering.")
        filtered_df = event_df  # If no filtering, export full data

    export = input("\nDo you want to export the events? (yes/no): ").strip().lower()
    if export == 'yes':
        format_choice = input("Choose format (csv/json): ").strip().lower()
        filename = input("Enter filename (without extension) (or press Enter for default 'filtered_events'): ").strip()

        # Default filename if none entered
        if not filename:
            filename = "filtered_events"

        if format_choice == 'csv':
            output_file = f"{filename}.csv"
            filtered_df.to_csv(output_file, index=False)
            print(f"\n✅ Filtered events exported successfully to {output_file}")
        elif format_choice == 'json':
            output_file = f"{filename}.json"
            filtered_df.to_json(output_file, orient='records', lines=True)
            print(f"\n✅ Filtered events exported successfully to {output_file}")
        else:
            print("❌ Invalid format selected. Export cancelled.")

    analytics_choice = input("\nDo you want to see analytics? (yes/no): ").strip().lower()
    if analytics_choice == 'yes':
        events_per_provider(filtered_df)
        most_frequent_event_ids(filtered_df)
        events_over_time(filtered_df)
    else:
        print("Skipping analytics.")


if __name__ == "__main__":
    main()
