# File Organizer

A simple desktop file organizer built with Python and Tkinter.

File Organizer helps users preview and organize files in a selected folder based on **file category** or **file extension**. It also provides statistics, progress tracking, duplicate-file handling, and an undo option for the last organization.


## Features

- 📁 Select a folder using a graphical interface
- 👀 Preview files before organizing
- 🗂️ Organize files by category
- 🔤 Organize files by file extension
- 📊 Display file count and category statistics
- 📈 Show organization progress with a progress bar
- 🔄 Undo the last organization
- 🔢 Automatically handle duplicate filenames
- ⚠️ Confirmation before organizing or undoing
- 🛡️ Error handling for invalid folders and file operations
- 🧹 Clear the current folder selection and results
- 🖥️ Simple desktop GUI built with Tkinter


## Technologies Used

- **Python**
- **Tkinter** — Graphical User Interface
- **Pathlib** — File and directory handling
- **Shutil** — Moving files
- **Git & GitHub** — Version control and project hosting

## Project Structure

```text
file-organizer/
│
├── main.py          # Tkinter GUI and application logic
├── organizer.py     # File preview, organization, and undo logic
├── categories.py    # File extension categories
├── .gitignore       # Files and folders ignored by Git
└── README.md        # Project documentation
```

## How to Run

### 1. Clone the repository

```bash
git clone https://github.com/yogesharumugam2103/file-organizer.git
```

### 2. Open the project folder

```bash
cd file-organizer
```

### 3. Run the application

```bash
python main.py
```

## Requirements

- Python 3.x
- No external Python packages are required.
- Tkinter is used for the graphical interface.


## How It Works

1. Select a folder using the **Browse** button.
2. Preview the files in the selected folder.
3. Choose an organization mode:
   - **By Category** — groups files such as Documents, Images, Code, etc.
   - **By Extension** — groups files based on their file extensions such as `.pdf`, `.jpg`, `.py`, etc.
4. Click **Organize Files** to move the files into the appropriate folders.
5. Use **Undo** to restore the files from the most recent organization.
6. Duplicate filenames are automatically renamed to prevent existing files from being overwritten.


## Future Improvements

- Filename keyword-based organization
- Custom user-defined categories
- Additional organization rules
- Improved customization options
