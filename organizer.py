from pathlib import Path
import shutil

from categories import categories

def get_unique_path(path):
    if not path.exists():
        return path

    counter = 1

    while True:
        new_name = f"{path.stem}_{counter}{path.suffix}"
        new_path = path.parent / new_name

        if not new_path.exists():
            return new_path

        counter += 1

def preview_folder(folder):
    folder = Path(folder)

    if not folder.exists() or not folder.is_dir():
        return None

    results = []

    for item in folder.iterdir():
        if item.is_file():
            extension = item.suffix.lower()
            category = categories.get(extension, "Others")

            results.append({
                "name": item.name,
                "category": category,
                "extension": item.suffix.lower()
            })

    return results

def organize_folder(
    folder,
    progress_callback=None,
    mode="category"
):
    folder = Path(folder)

    if not folder.exists():
        return ["Error: Folder does not exist."]
    
    results = []

    category_folders = set(categories.values())
    category_folders.add("Others")

    files = [
        item for item in folder.iterdir()
        if item.is_file()
    ]

    total_files = len(files)
    processed_files = 0

    for item in files:
        if item.is_dir() and item.name in category_folders:
            continue

        if item.is_file():
            extension = item.suffix.lower()
            category = categories.get(extension, "Others")

            if mode == "extension":
                if extension:
                    destination = folder / extension
                else:
                    destination = folder / "No Extension"
            
            else:
                destination = folder / category

            destination.mkdir(exist_ok=True)

            destination_file = destination / item.name
            destination_file = get_unique_path(destination_file)

        try:
            shutil.move(item, destination_file)

            results.append(
                f"{item.name} → {category}"
            )

            processed_files += 1

            if progress_callback:
                progress_callback(
                    processed_files,
                    total_files
                )

        except Exception as error:
            results.append(
                f"Could not move {item.name}: {error}"
            )

    return results