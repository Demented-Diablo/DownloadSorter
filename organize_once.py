from pathlib import Path
from shutil import move
import csv
import time

DOWNLOADS = Path.home() / "Downloads"
OUT_BASE = DOWNLOADS / "Sorted"
LOG_CSV = DOWNLOADS / "sorted_moves.csv"

CATEGORY_MAP = {
    "PDFs": [".pdf"],
    "Images": [".png", ".jpg", ".jpeg", ".tiff", ".webp", ".gif", ".svg", ".heic"],
    "Videos": [".mp4", ".mkv", ".mov"],
    "Audio": [".mp3", ".wav", ".flac"],
    "Documents": [".docx", ".doc", ".pptx", ".xlsx", ".csv", ".txt", ".rtf", ".md"],
    "Archives": [".zip", ".rar", ".7z", ".tar", ".gz"],
    "Installers": [".exe", ".msi", ".apk", ".jar", ".bat", ".reg"],
    "Code": [".js", ".c", ".java", ".py", ".json", ".xml", ".yml", ".css", ".html", ".pem", ".ini", ".lock", ".key"],
    "GameData": [".pak", ".bin", ".mca", ".dat", ".dat_old", ".asi", ".node", ".dll", ".0", ".1", ".sig", ".asar", ".mcmeta", ".recipe", ".exp", ".iobj", ".ipdb", ".lib", ".filters", ".vcxproj", ".lastbuildstate", ".md5", ".tlog", ".cv"],
    "Misc": []
}

# build reverse lookups
EXT_TO_FOLDER = {}
for folder, exts in CATEGORY_MAP.items():
    for e in exts:
        EXT_TO_FOLDER[e] = folder

def ensure_dirs():
    OUT_BASE.mkdir(exist_ok=True)
    for folder in CATEGORY_MAP.keys():
        (OUT_BASE / folder).mkdir(parents=True, exist_ok=True)

def pick_folder(path: Path) -> Path:
    ext = path.suffix.lower()
    folder = EXT_TO_FOLDER.get(ext, "Misc")
    return OUT_BASE / folder

def log_move(src: Path, dst: Path):
    write_header = not LOG_CSV.exists()
    with LOG_CSV.open("a", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        if write_header:
            w.writerow(["timestamp", "file_name", "from", "to", "size_bytes"])
        w.writerow([time.strftime("%Y-%m-%d %H:%M:%S"), src.name, str(src.parent), str(dst), src.stat().st_size])

def move_one(p: Path):
    if not p.is_file():
        return False
    if OUT_BASE in p.parents:
        return False  # already sorted
    dest_dir = pick_folder(p)
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / p.name
    # handle name collision
    n = 1
    while dest.exists():
        dest = dest_dir / f"{p.stem} ({n}){p.suffix}"
        n += 1
    move(str(p), str(dest))
    log_move(p, dest)
    print(f"Moved: {p.name}  ->  {dest}")
    return True

def main():
    ensure_dirs()
    print(f"Organizing existing files in: {DOWNLOADS}")
    moved = 0
    # only files sitting directly in Downloads, leave subfolders as they are
    for p in DOWNLOADS.iterdir():
        try:
            if move_one(p):
                moved += 1
        except Exception as e:
            print(f"Skip {p.name}: {e}")
    print(f"Done. Files moved: {moved}")
    print(f"Log saved to: {LOG_CSV}")
    print(f"Sorted folders at: {OUT_BASE}")

if __name__ == "__main__":
    main()
