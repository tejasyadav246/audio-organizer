# Audio Library Organizer & Tagger

A Python script that scans a messy folder of audio files (the kind every producer has — half-named exports, drafts, random downloads) and organizes them into a clean `Artist/Genre/Title.ext` folder structure, reading the real metadata instead of relying on filenames.

## How it works

1. Scans a folder for `.mp3`, `.wav`, `.flac`, `.m4a` files.
2. Reads embedded metadata (artist, title, genre, duration, bitrate) using `mutagen`.
3. Falls back to sensible defaults ("Unknown Artist", filename as title) when tags are missing, instead of crashing.
4. Copies each file into a new organized folder tree and prints a summary.

## Usage

```bash
pip install mutagen
python organizer.py /path/to/messy/music/folder
```

Example output:
```
[ok] track01.mp3 -> Organized/Tejas Yadav/Hindi Pop/Tere Naino Se.mp3  (0:03, 25kbps)
[ok] xyz_final_v3.mp3 -> Organized/Unknown Artist Demo/Ambient RnB/half-healed (draft).mp3  (0:02, 28kbps)

Scanned 2 files | Organized 2 | Skipped 0
```

## Why I built this

Managing exports, stems, and drafts across projects gets messy fast. This automates the sorting I'd otherwise do by hand, and reads actual ID3/metadata tags rather than trusting filenames — which are usually a mess like `xyz_final_v3.mp3`.

## Possible extensions
- Move instead of copy, with a `--dry-run` safety flag
- Auto-tag untagged files using filename heuristics or an audio fingerprinting API
- Detect and flag duplicate tracks
