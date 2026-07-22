# 🎵 Audio Library Organizer & Tagger

A lightweight Python utility that scans unorganized directories of audio exports, stems, and drafts, sorting them into a structured `Artist/Genre/Title.ext` folder hierarchy by parsing real embedded ID3/metadata tags rather than unreliable filenames.

---

## ✨ Features

* **Multi-Format Support:** Reads tags from `.mp3`, `.wav`, `.flac`, `.m4a`, `.ogg`, and `.aiff` files using `mutagen`.
* **Graceful Metadata Fallbacks:** Missing artist or genre tags are safely assigned sensible defaults (`Unknown Artist`, filename as title) to prevent crashes.
* **Safety Dry-Run Mode:** Supports a `--dry-run` flag to preview organizational changes without modifying any files.
* **Bitrate & Duration Reporting:** Logs audio technical metrics (duration and bitrate in kbps) for processed tracks.
* **Non-Destructive Operating Modes:** Copy files by default, with an optional `--move` flag for directory migrations.

---

## 🚀 Quickstart

1. **Install Dependencies:**
   ```bash
   pip install mutagen
