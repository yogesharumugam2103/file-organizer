import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from organizer import organize_folder, preview_folder


selected_folder = None


def browse_folder():
    global selected_folder

    folder = filedialog.askdirectory()

    if folder:
        selected_folder = folder
        folder_label.config(text=folder)
        status_label.config(text="Folder selected")

def preview_files():
    if selected_folder is None:
        status_label.config(text="Please select a folder first")
        return

    results = preview_folder(selected_folder)

    if results is None:
        result_text.delete("1.0", tk.END)
        result_text.insert(tk.END, "Invalid folder.")

        stats_label.config(text="")
        status_label.config(text="Preview failed")
        return

    if not results:
        result_text.delete("1.0", tk.END)
        result_text.insert(
            tk.END,
            "No files found in this folder."
        )

        stats_label.config(text="")
        status_label.config(text="Preview: No files found")
        return

    # Get the currently selected mode
    mode = organization_mode.get()

    result_text.delete("1.0", tk.END)

    counts = {}

    for result in results:

        if mode == "extension":
            destination = result["extension"]

            if not destination:
                destination = "No Extension"

        else:
            destination = result["category"]

        # Display the actual destination
        result_text.insert(
            tk.END,
            f"{result['name']} → {destination}\n"
        )

        # Count according to the selected mode
        if destination not in counts:
            counts[destination] = 0

        counts[destination] += 1

    total_files = len(results)

    stats_text = f"Total files: {total_files} | " + " | ".join(
        f"{name}: {count}"
        for name, count in counts.items()
    )

    stats_label.config(text=stats_text)

    status_label.config(
        text=f"Preview ({'By Extension' if mode == 'extension' else 'By Category'}): "
             f"{total_files} file(s) found"
    )

def organize_files():
    if selected_folder is None:
        status_label.config(text="Please select a folder first")
        return

    confirmed = messagebox.askyesno(
        "Confirm Organization",
        "Are you sure you want to organize the files?"
    )

    if not confirmed:
        status_label.config(text="Organization cancelled")
        return

    preview_button.config(state=tk.DISABLED)
    organize_button.config(state=tk.DISABLED)
    clear_button.config(state=tk.DISABLED)

    progress_bar["value"] = 0
    progress_bar["maximum"] = 100

    def update_progress(processed, total):
        if total > 0:
            percentage = (processed / total) * 100
            progress_bar["value"] = percentage

            status_label.config(
                text=f"Organizing... {processed}/{total} files"
            )

            window.update_idletasks()

    try:
        results = organize_folder(
            selected_folder,
            progress_callback=update_progress,
            mode=organization_mode.get()
        )

        result_text.delete("1.0", tk.END)

        for result in results:
            result_text.insert(tk.END, result + "\n")

        status_label.config(
            text=f"Organization completed! {len(results)} result(s)"
        )

    except Exception as error:
        messagebox.showerror(
            "Organization Error",
            f"An unexpected error occurred:\n\n{error}"
        )

        status_label.config(
            text="Organization failed"
        )

    finally:
        preview_button.config(state=tk.NORMAL)
        organize_button.config(state=tk.NORMAL)
        clear_button.config(state=tk.NORMAL)

def clear_selection():
    global selected_folder

    selected_folder = None

    folder_label.config(text="No folder selected")
    result_text.delete("1.0", tk.END)
    stats_label.config(text="")
    status_label.config(text="Status: Ready")

window = tk.Tk()
organization_mode = tk.StringVar(
    master=window,
    value="category"
)

window.title("File Organizer")
window.geometry("1000x600")


# Title
title_label = tk.Label(
    window,
    text="File Organizer",
    font=("Arial", 20, "bold")
)

title_label.pack(pady=20)


# Folder section
folder_frame = tk.Frame(window)
folder_frame.pack(pady=10)

folder_title = tk.Label(
    folder_frame,
    text="Selected Folder",
    font=("Arial", 12, "bold")
)

folder_title.pack()

browse_button = tk.Button(
    folder_frame,
    text="Browse",
    command=browse_folder
)

browse_button.pack()

folder_label = tk.Label(
    folder_frame,
    text="No folder selected",
    wraplength=700,
    font=("Arial", 10)
)

folder_label.pack(pady=15)


# Action buttons section
actions_frame = tk.Frame(window)
actions_frame.pack(pady=10)

mode_frame = tk.Frame(window)
mode_frame.pack(pady=5)

mode_title = tk.Label(
    mode_frame,
    text="Organization Mode",
    font=("Arial", 11, "bold")
)

mode_title.pack()

category_radio = tk.Radiobutton(
    mode_frame,
    text="By Category",
    variable=organization_mode,
    value="category",
    command=preview_files
)

category_radio.pack(side=tk.LEFT, padx=10)

extension_radio = tk.Radiobutton(
    mode_frame,
    text="By Extension",
    variable=organization_mode,
    value="extension",
    command=preview_files
)

extension_radio.pack(side=tk.LEFT, padx=10)

preview_button = tk.Button(
    actions_frame,
    text="Preview",
    command=preview_files
)

preview_button.pack(side=tk.LEFT, padx=5)

organize_button = tk.Button(
    actions_frame,
    text="Organize Files",
    command=organize_files
)

organize_button.pack(side=tk.LEFT, padx=5)

clear_button = tk.Button(
    actions_frame,
    text="Clear",
    command=clear_selection
)

clear_button.pack(side=tk.LEFT, padx=5)


# Results section
results_label = tk.Label(
    window,
    text="Results",
    font=("Arial", 12, "bold")
)

results_label.pack()

results_frame = tk.Frame(window)
results_frame.pack(pady=10)

result_text = tk.Text(
    results_frame,
    height=10,
    width=80
)

result_text.pack(side=tk.LEFT)

results_scrollbar = tk.Scrollbar(
    results_frame,
    command=result_text.yview
)

results_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

result_text.config(
    yscrollcommand=results_scrollbar.set
)

# Statistics
statistics_title = tk.Label(
    window,
    text="Statistics",
    font=("Arial", 12, "bold")
)

statistics_title.pack(pady=5)

stats_label = tk.Label(
    window,
    text=""
)

stats_label.pack(pady=5)

progress_bar = ttk.Progressbar(
    window,
    orient="horizontal",
    length=400,
    mode="determinate"
)

progress_bar.pack(pady=10)

# Status
status_label = tk.Label(
    window,
    text="Status: Ready"
)

status_label.pack(pady=10)


window.mainloop()