"""
Audio Library Organizer & Tagger
----------------------------------
Scans a folder of audio files (mp3, wav, flac), reads their metadata
(artist, title, genre, duration, bitrate), and organizes them into a
clean folder structure: Organized/<Artist>/<Genre>/<Title>.ext

If metadata is missing, files are sorted into an "Unknown" bucket
instead of crashing — real-world audio libraries are messy.

Usage:
    python organizer.py /path/to/messy/music/folder
"""

import os
import shutil
import sys
from mutagen import File as MutagenFile

SUPPORTED_EXTENSIONS = {".mp3", ".wav", ".flac", ".m4a"}


def read_metadata(filepath):
    """Extract artist, title, genre, duration, and bitrate from an audio file."""
    audio = MutagenFile(filepath, easy=True)

    if audio is None:
        return None

    tags = audio.tags or {}
    artist = tags.get("artist", ["Unknown Artist"])[0]
    title = tags.get("title", [os.path.splitext(os.path.basename(filepath))[0]])[0]
    genre = tags.get("genre", ["Unknown Genre"])[0]

    duration = getattr(audio.info, "length", 0)
    bitrate = getattr(audio.info, "bitrate", 0)

    return {
        "artist": sanitize(artist),
        "title": sanitize(title),
        "genre": sanitize(genre),
        "duration": duration,
        "bitrate": bitrate,
    }


def sanitize(name):
    """Remove characters that aren't safe for folder/file names."""
    invalid_chars = '<>:"/\\|?*'
    for ch in invalid_chars:
        name = name.replace(ch, "")
    return name.strip() or "Unknown"


def organize_folder(source_folder, output_folder="Organized"):
    scanned, moved, skipped = 0, 0, 0

    for filename in os.listdir(source_folder):
        ext = os.path.splitext(filename)[1].lower()
        if ext not in SUPPORTED_EXTENSIONS:
            continue

        scanned += 1
        filepath = os.path.join(source_folder, filename)
        meta = read_metadata(filepath)

        if meta is None:
            print(f"  [skip] Could not read metadata: {filename}")
            skipped += 1
            continue

        dest_dir = os.path.join(output_folder, meta["artist"], meta["genre"])
        os.makedirs(dest_dir, exist_ok=True)

        dest_path = os.path.join(dest_dir, f"{meta['title']}{ext}")
        shutil.copy2(filepath, dest_path)
        moved += 1

        mins, secs = divmod(int(meta["duration"]), 60)
        print(f"  [ok] {filename} -> {dest_path}  "
              f"({mins}:{secs:02d}, {meta['bitrate']//1000 if meta['bitrate'] else 0}kbps)")

    print(f"\nScanned {scanned} files | Organized {moved} | Skipped {skipped}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python organizer.py <folder_of_audio_files>")
        sys.exit(1)

    organize_folder(sys.argv[1])
