import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from organizer import (
    organize_folder,
    preview_folder,
    undo_last_organization
)


selected_folder = None

CATEGORY_ICONS = {
    "Documents": "📄",
    "Images": "🖼",
    "Music": "🎵",
    "Videos": "🎬",
    "Code": "💻",
    "Others": "📦"
}

def browse_folder():
    global selected_folder

    folder = filedialog.askdirectory()

    if folder:
        selected_folder = folder
        folder_label.config(text=folder)
        status_label.config(text="Folder selected")

def preview_files():
    if selected_folder is None:
        result_text.delete("1.0", tk.END)
        result_text.insert(
            tk.END,
            "Please select a folder first."
        )

        stats_label.config(text="")

        status_label.config(
            text="Preview unavailable"
        )

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
        icon = CATEGORY_ICONS.get(
            result["category"],
            "📦"
        )    

        result_text.insert(
            tk.END,
            f"{icon}  {result['name']} → {destination}\n"
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
        result_text.delete("1.0", tk.END)
        result_text.insert(
            tk.END,
            "Please select a folder first."
        )

        stats_label.config(text="")

        status_label.config(
            text="Organization unavailable"
        )

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

        undo_button.config(
        state=tk.NORMAL,
        bg=PRIMARY_COLOR,
        fg="white",
        activebackground=PRIMARY_HOVER,
        activeforeground="white",
        cursor="hand2"
    )

        result_text.delete("1.0", tk.END)

        for result in results:
            result_text.insert(tk.END, result + "\n")

        successful_files = sum(
            1 for result in results
            if result.startswith("✓")
        )

        failed_files = sum(
            1 for result in results
            if result.startswith("✗")
        )

        status_label.config(
            text=f"Organization completed! "
                 f"{successful_files} successful, "
                 f"{failed_files} failed"
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

def undo_organization():
    if selected_folder is None:
        result_text.delete("1.0", tk.END)
        result_text.insert(
            tk.END,
            "Please select a folder first."
        )    
        status_label.config(
            text="Undo unavailable"
        )

        return

    confirmed = messagebox.askyesno(
        "Undo Organization",
        "Are you sure you want to undo the last organization?"
    )

    if not confirmed:
        status_label.config(text="Undo cancelled")
        return

    try:
        results = undo_last_organization()

        undo_button.config(
        state=tk.DISABLED,
        bg="#E5E7EB",
        fg="#9CA3AF",
        activebackground="#E5E7EB",
        activeforeground="#9CA3AF",
        cursor="arrow"
    )

        result_text.delete("1.0", tk.END)

        for result in results:
            result_text.insert(
                tk.END,
                result + "\n"
            )

        successful_restores = sum(
            1 for result in results
            if result.startswith("✓")
        )

        failed_restores = sum(
            1 for result in results
            if result.startswith("✗")
        )

        status_label.config(
            text=f"Undo completed! "
                 f"{successful_restores} restored, "
                 f"{failed_restores} failed"
        )

    except Exception as error:
        messagebox.showerror(
            "Undo Error",
            f"An unexpected error occurred:\n\n{error}"
        )

        status_label.config(
            text="Undo failed"
        )

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

# -------------------------------
# GUI Theme
# -------------------------------

BG_COLOR = "#F4F6F8"
CARD_COLOR = "#FFFFFF"
PRIMARY_COLOR = "#2563EB"
PRIMARY_HOVER = "#1D4ED8"
TEXT_COLOR = "#1F2937"
SECONDARY_TEXT = "#6B7280"
BORDER_COLOR = "#D1D5DB"

TITLE_FONT = ("Segoe UI", 24, "bold")
SUBTITLE_FONT = ("Segoe UI", 10)
HEADING_FONT = ("Segoe UI", 11, "bold")
NORMAL_FONT = ("Segoe UI", 10)
BUTTON_FONT = ("Segoe UI", 10, "bold")


# -------------------------------
# Window
# -------------------------------

window.title("File Organizer")

window_width = 1000
window_height = 650

screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x = (screen_width - window_width) // 2
y = (screen_height - window_height) // 2 - 90

window.geometry(
    f"{window_width}x{window_height}+{x}+{y}"
)

window.minsize(900, 750)
window.configure(bg=BG_COLOR)


# -------------------------------
# Title
# -------------------------------

title_label = tk.Label(
    window,
    text="File Organizer",
    font=TITLE_FONT,
    bg=BG_COLOR,
    fg=TEXT_COLOR
)

title_label.pack(pady=(15, 5))


subtitle_label = tk.Label(
    window,
    text="Organize your files quickly and effortlessly",
    font=SUBTITLE_FONT,
    bg=BG_COLOR,
    fg=SECONDARY_TEXT
)

subtitle_label.pack(pady=(0, 20))


# -------------------------------
# Folder Card
# -------------------------------

folder_frame = tk.Frame(
    window,
    bg=CARD_COLOR,
    highlightbackground=BORDER_COLOR,
    highlightthickness=1
)

folder_frame.pack(
    fill="x",
    padx=80,
    pady=5
)


folder_title = tk.Label(
    folder_frame,
    text="SELECTED FOLDER",
    font=HEADING_FONT,
    bg=CARD_COLOR,
    fg=TEXT_COLOR
)

folder_title.pack(pady=(15, 8))


folder_content = tk.Frame(
    folder_frame,
    bg=CARD_COLOR
)

folder_content.pack(
    fill="x",
    padx=20,
    pady=(0, 15)
)


folder_label = tk.Label(
    folder_content,
    text="No folder selected",
    wraplength=650,
    anchor="w",
    font=NORMAL_FONT,
    bg=CARD_COLOR,
    fg=SECONDARY_TEXT
)

folder_label.pack(
    side=tk.LEFT,
    fill="x",
    expand=True,
    padx=(0, 15)
)


browse_button = tk.Button(
    folder_content,
    text="Browse",
    command=browse_folder,
    font=BUTTON_FONT,
    bg=PRIMARY_COLOR,
    fg="white",
    activebackground=PRIMARY_HOVER,
    activeforeground="white",
    relief="flat",
    padx=25,
    pady=8,
    cursor="hand2"
)

browse_button.pack(side=tk.RIGHT)


# -------------------------------
# Organization Mode
# -------------------------------

mode_frame = tk.Frame(
    window,
    bg=BG_COLOR
)

mode_frame.pack(pady=3)


mode_title = tk.Label(
    mode_frame,
    text="ORGANIZATION MODE",
    font=HEADING_FONT,
    bg=BG_COLOR,
    fg=TEXT_COLOR
)

mode_title.pack(pady=(0, 5))


radio_frame = tk.Frame(
    mode_frame,
    bg=BG_COLOR
)

radio_frame.pack()


category_radio = tk.Radiobutton(
    radio_frame,
    text="By Category",
    variable=organization_mode,
    value="category",
    command=preview_files,
    font=NORMAL_FONT,
    bg=BG_COLOR,
    fg=TEXT_COLOR,
    activebackground=BG_COLOR,
    activeforeground=TEXT_COLOR
)

category_radio.pack(
    side=tk.LEFT,
    padx=15
)


extension_radio = tk.Radiobutton(
    radio_frame,
    text="By Extension",
    variable=organization_mode,
    value="extension",
    command=preview_files,
    font=NORMAL_FONT,
    bg=BG_COLOR,
    fg=TEXT_COLOR,
    activebackground=BG_COLOR,
    activeforeground=TEXT_COLOR
)

extension_radio.pack(
    side=tk.LEFT,
    padx=15
)


# -------------------------------
# Action Buttons
# -------------------------------

actions_frame = tk.Frame(
    window,
    bg=BG_COLOR
)

actions_frame.pack(pady=5)


preview_button = tk.Button(
    actions_frame,
    text="Preview",
    command=preview_files,
    font=NORMAL_FONT,
    bg="#E8EEF7",
    fg=PRIMARY_COLOR,
    activebackground="#D8E4F5",
    activeforeground=PRIMARY_COLOR,
    relief="solid",
    bd=1,
    padx=25,
    pady=9,
    cursor="hand2"
)

preview_button.pack(
    side=tk.LEFT,
    padx=6
)


organize_button = tk.Button(
    actions_frame,
    text="Organize Files",
    command=organize_files,
    font=BUTTON_FONT,
    bg=PRIMARY_COLOR,
    fg="white",
    activebackground=PRIMARY_HOVER,
    activeforeground="white",
    relief="flat",
    padx=25,
    pady=9,
    cursor="hand2"
)

organize_button.pack(
    side=tk.LEFT,
    padx=6
)

undo_button = tk.Button(
    actions_frame,
    text="Undo",
    command=undo_organization,
    font=NORMAL_FONT,
    bg="#E5E7EB",
    fg="#9CA3AF",
    activebackground="#E5E7EB",
    activeforeground="#9CA3AF",
    disabledforeground="#9CA3AF",
    relief="solid",
    bd=1,
    padx=25,
    pady=9,
    cursor="arrow",
    state=tk.DISABLED
)

undo_button.pack(
    side=tk.LEFT,
    padx=6
)

clear_button = tk.Button(
    actions_frame,
    text="Clear",
    command=clear_selection,
    font=NORMAL_FONT,
    bg=CARD_COLOR,
    fg=TEXT_COLOR,
    activebackground="#E5E7EB",
    activeforeground=TEXT_COLOR,
    relief="solid",
    bd=1,
    padx=25,
    pady=9,
    cursor="hand2"
)

clear_button.pack(
    side=tk.LEFT,
    padx=6
)


# -------------------------------
# Results
# -------------------------------

results_label = tk.Label(
    window,
    text="RESULTS",
    font=HEADING_FONT,
    bg=BG_COLOR,
    fg=TEXT_COLOR
)

results_label.pack(pady=(3, 3))


results_frame = tk.Frame(
    window,
    bg=CARD_COLOR,
    highlightbackground=BORDER_COLOR,
    highlightthickness=1
)

results_frame.pack(
    fill="both",
    expand=True,
    padx=80,
    pady=5
)

result_text = tk.Text(
    results_frame,
    height=9,
    width=80,
    font=("Consolas", 10),
    bg="#FFFFFF",
    fg=TEXT_COLOR,
    insertbackground=TEXT_COLOR,
    relief="solid",
    bd=1,
    padx=12,
    pady=10,
    wrap="none"
)

result_text.pack(
    side=tk.LEFT,
    fill="both",
    expand=True
)


results_scrollbar = tk.Scrollbar(
    results_frame,
    command=result_text.yview,
    relief="flat"
)

results_scrollbar.pack(
    side=tk.RIGHT,
    fill=tk.Y
)


result_text.config(
    yscrollcommand=results_scrollbar.set
)


# -------------------------------
# Statistics
# -------------------------------

# Statistics

statistics_frame = tk.Frame(
    window,
    bg=CARD_COLOR,
    bd=1,
    relief="solid"
)

statistics_frame.pack(
    pady=4,
    padx=100,
    fill="x"
)

statistics_title = tk.Label(
    statistics_frame,
    text="STATISTICS",
    font=("Arial", 11, "bold"),
    bg=CARD_COLOR,
    fg=TEXT_COLOR
)

statistics_title.pack(pady=(5, 2))

stats_label = tk.Label(
    statistics_frame,
    text="No preview available",
    font=("Arial", 10),
    bg=CARD_COLOR,
    fg=SECONDARY_TEXT
)

stats_label.pack(pady=(3, 10))


# Progress section

progress_frame = tk.Frame(
    window,
    bg=BG_COLOR
)

progress_frame.pack(
    pady=5
)

progress_title = tk.Label(
    progress_frame,
    text="PROGRESS",
    font=("Arial", 11, "bold"),
    bg=BG_COLOR,
    fg=TEXT_COLOR
)

progress_title.pack(pady=(0, 5))

progress_bar = ttk.Progressbar(
    progress_frame,
    orient="horizontal",
    length=500,
    mode="determinate"
)

progress_bar.pack()


# -------------------------------
# Status
# -------------------------------

status_label = tk.Label(
    window,
    text="Status: Ready",
    font=NORMAL_FONT,
    bg=BG_COLOR,
    fg=SECONDARY_TEXT
)

status_label.pack(pady=(2, 15))


window.mainloop()