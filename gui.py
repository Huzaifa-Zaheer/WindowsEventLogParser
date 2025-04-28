import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from tabulate import tabulate
import pandas as pd

from parsers.parser import parse_events
from models.event_model import normalize_events
from filters.filter import filter_events

event_df = None
filtered_df = None

# GUI Functions
def select_file():
    global event_df

    filepath = filedialog.askopenfilename(title="Select EVTX File", filetypes=[("EVTX files", "*.evtx")])
    if filepath:
        events = parse_events(filepath)
        event_df = normalize_events(events)
        output_text.delete('1.0', tk.END)
        output_text.insert(tk.END, f"Total Events Parsed: {len(event_df)}\n")
        output_text.insert(tk.END, tabulate(event_df.head(), headers='keys', tablefmt='pretty'))


def apply_filters():
    global filtered_df
    if event_df is None:
        messagebox.showerror("Error", "Please load an EVTX file first!")
        return

    event_id = event_id_entry.get()
    event_id = int(event_id) if event_id else None

    provider = provider_entry.get() or None
    start_time = start_time_entry.get() or None
    end_time = end_time_entry.get() or None

    filtered_df = filter_events(event_df, event_id, provider, start_time, end_time)

    output_text.delete('1.0', tk.END)
    output_text.insert(tk.END, f"Total Events After Filtering: {len(filtered_df)}\n")
    output_text.insert(tk.END, tabulate(filtered_df.head(), headers='keys', tablefmt='pretty'))


def export_file():
    if filtered_df is None:
        messagebox.showerror("Error", "Please apply filters first!")
        return

    format_choice = simpledialog.askstring("Export", "Enter export format (csv/json):").lower()
    filename = simpledialog.askstring("Export", "Enter filename (without extension):")

    if not filename:
        filename = "filtered_events"

    try:
        if format_choice == 'csv':
            filtered_df.to_csv(f"{filename}.csv", index=False)
            messagebox.showinfo("Success", f"Filtered events exported to {filename}.csv")
        elif format_choice == 'json':
            filtered_df.to_json(f"{filename}.json", orient='records', lines=True)
            messagebox.showinfo("Success", f"Filtered events exported to {filename}.json")
        else:
            messagebox.showerror("Error", "Invalid format. Please enter 'csv' or 'json'.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to export: {str(e)}")

# Setup GUI window
root = tk.Tk()
root.title("Windows Event Log Parser")
root.geometry("800x600")

# File selection button
select_button = tk.Button(root, text="Select EVTX File", command=select_file)
select_button.pack(pady=10)

# Filter options frame
filter_frame = tk.Frame(root)
filter_frame.pack(pady=5)

tk.Label(filter_frame, text="Event ID:").grid(row=0, column=0)
event_id_entry = tk.Entry(filter_frame)
event_id_entry.grid(row=0, column=1)

tk.Label(filter_frame, text="Provider:").grid(row=0, column=2)
provider_entry = tk.Entry(filter_frame)
provider_entry.grid(row=0, column=3)

tk.Label(filter_frame, text="Start Time (YYYY-MM-DD):").grid(row=1, column=0)
start_time_entry = tk.Entry(filter_frame)
start_time_entry.grid(row=1, column=1)

tk.Label(filter_frame, text="End Time (YYYY-MM-DD):").grid(row=1, column=2)
end_time_entry = tk.Entry(filter_frame)
end_time_entry.grid(row=1, column=3)

# Apply filter button
filter_button = tk.Button(root, text="Apply Filters", command=apply_filters)
filter_button.pack(pady=5)

# Export button
export_button = tk.Button(root, text="Export Filtered Events", command=export_file)
export_button.pack(pady=5)

# Text area for output
output_text = tk.Text(root, height=25, width=100)
output_text.pack(pady=10)

root.mainloop()
