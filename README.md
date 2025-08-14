# DownloadSorter
# DownloadSorter

A simple Python automation that keeps your Downloads folder organized in real-time **or** in one click.

## Features
- **Real-time sorting** — watches your Downloads folder and automatically moves files into category folders (PDFs, Images, Videos, etc.).
- **One-time organizer** — run once to instantly sort all current files without keeping the watcher running.
- **Desktop notifications** — get a toast notification telling you where your file went.
- **Logging** — every move is saved in a CSV log for quick lookup.
- **Collision handling** — avoids overwriting files by appending `(1)`, `(2)`, etc.

## Categories
| Category      | Extensions |
|---------------|------------|
| PDFs          | .pdf |
| Images        | .png, .jpg, .jpeg, .tiff, .webp, .gif, .svg, .heic |
| Videos        | .mp4, .mkv, .mov |
| Audio         | .mp3, .wav, .flac |
| Documents     | .docx, .doc, .pptx, .xlsx, .csv, .txt, .rtf, .md |
| Archives      | .zip, .rar, .7z, .tar, .gz |
| Installers    | .exe, .msi, .apk, .jar, .bat, .reg |
| Code          | .js, .c, .java, .py, .json, .xml, .yml, .css, .html, .pem, .ini, .lock, .key |
| Game Data     | .pak, .bin, .mca, .dat, .dat_old, .asi, .node, .dll, .0, .1, .sig, .asar, .mcmeta, .recipe, .exp, .iobj, .ipdb, .lib, .filters, .vcxproj, .lastbuildstate, .md5, .tlog, .cv |
| Misc          | Everything else |

## 🛠 Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/Demented-Diablo/DownloadSorter
   cd DownloadSorter

2. Install required packages:
    pip install watchdog win10toast


3. Choose how you want to use it:

    Real-time Watcher:

        python downloads_sorter.py
        Leave it running in the background while you download files.

    One-time Organizer:

        python organize_once.py
        Runs once and sorts everything currently in your Downloads.

4. Log File

    All moves are recorded in:

    Downloads/Sorted/_logs/sorted_moves.csv
