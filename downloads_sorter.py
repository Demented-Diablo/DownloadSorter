import time
import csv
from pathlib import Path
from shutil import move
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from win10toast import ToastNotifier

DOWNLOADS = Path.home() / "Downloads"
OUT_BASE = DOWNLOADS / "Sorted"
LOG_DIR = OUT_BASE / "_logs"
LOG_CSV = LOG_DIR / "sorted_moves.csv"

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

TEMP_EXTS = {".crdownload", ".tmp", ".part"}

EXT_TO_FOLDER = {e: folder for folder, exts in CATEGORY_MAP.items() for e in exts}
toaster = ToastNotifier()

def ensure_dirs():
    OUT_BASE.mkdir(exist_ok=True)
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    for folder in CATEGORY_MAP.keys():
        (OUT_BASE / folder).mkdir(parents=True, exist_ok=True)

def pick_folder(path: Path) -> Path:
    return OUT_BASE / EXT_TO_FOLDER.get(path.suffix.lower(), "Misc")

def is_ignored(p: Path) -> bool:
    # ignore anything already sorted, and the log files
    if OUT_BASE in p.parents:
        return True
    try:
        if p.resolve() == LOG_CSV.resolve():
            return True
    except FileNotFoundError:
        pass
    return False

def wait_until_stable(p: Path, tries=60, delay=0.2):
    for _ in range(tries):
        if not p.exists():
            time.sleep(delay)
            continue
        if p.suffix.lower() in TEMP_EXTS:
            time.sleep(delay)
            continue
        try:
            s1 = p.stat().st_size
            time.sleep(delay)
            s2 = p.stat().st_size
            if s1 == s2 and s1 > 0:
                return True
        except FileNotFoundError:
            pass
    return False

def log_move(src: Path, dst: Path):
    write_header = not LOG_CSV.exists()
    with LOG_CSV.open("a", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        if write_header:
            w.writerow(["timestamp","file_name","from","to","size_bytes"])
        w.writerow([time.strftime("%Y-%m-%d %H:%M:%S"), dst.name, str(src.parent), str(dst), dst.stat().st_size])

def move_file(p: Path):
    if not p.exists() or is_ignored(p) or p.suffix.lower() in TEMP_EXTS:
        return
    if not wait_until_stable(p):
        print(f"Skip not stable: {p.name}")
        return
    dest_dir = pick_folder(p)
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / p.name
    n = 1
    while dest.exists():
        dest = dest_dir / f"{p.stem} ({n}){p.suffix}"
        n += 1
    src_before = p
    move(str(p), str(dest))
    log_move(src_before, dest)
    print(f"MOVED  {src_before.name}  ->  {dest}")
    try:
        toaster.show_toast("Downloads sorted", f"{dest.name} → {dest_dir.name}", duration=3, threaded=True)
    except Exception:
        pass  # some Windows setups throw a toast callback warning, safe to ignore

class SortHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            move_file(Path(event.src_path))
    def on_modified(self, event):
        if not event.is_directory:
            move_file(Path(event.src_path))
    def on_moved(self, event):
        if not event.is_directory:
            move_file(Path(event.dest_path))

def main():
    ensure_dirs()
    print(f"Watching: {DOWNLOADS}")
    print(f"Log file: {LOG_CSV}")
    observer = Observer()
    handler = SortHandler()
    observer.schedule(handler, str(DOWNLOADS), recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1)
    finally:
        observer.stop()
        observer.join()

if __name__ == "__main__":
    main()
