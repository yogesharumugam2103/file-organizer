from pathlib import Path
import shutil

from categories import categories

last_organization = []

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

def undo_last_organization():
    global last_organization

    if not last_organization:
        return ["Nothing to undo."]

    moves_to_undo = last_organization.copy()
    results = []

    for move in reversed(moves_to_undo):
        original_path = move["original"]
        destination_path = move["destination"]

        try:
            if destination_path.exists():
                original_path.parent.mkdir(
                    parents=True,
                    exist_ok=True
                )

                restored_path = get_unique_path(original_path)

                shutil.move(
                    destination_path,
                    restored_path
                )

                results.append(
                    f"Restored: {destination_path.name}"
                )

            else:
                results.append(
                    f"Could not restore: {destination_path.name}"
                )

        except Exception as error:
            results.append(
                f"Could not restore {destination_path.name}: {error}"
            )

    # Clear history ONLY after the undo operation has been attempted
    last_organization = []

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

    global last_organization
    last_organization = []

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
            original_path = item

            shutil.move(item, destination_file)

            last_organization.append(
                {
                    "original": original_path,
                    "destination": destination_file
                }
            )    

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