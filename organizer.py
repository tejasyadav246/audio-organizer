import os
import sys
import shutil
import argparse
from pathlib import Path
from mutagen import File
from mutagen.id3 import ID3NoHeaderError


def format_duration(seconds):
    """Converts seconds to M:SS string format."""
    if not seconds:
        return "0:00"
    mins = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{mins}:{secs:02d}"


def get_metadata(file_path):
    """
    Reads embedded metadata from .mp3, .wav, .flac, .m4a, etc.
    Falls back gracefully to sensible defaults if tags are missing.
    """
    artist = "Unknown Artist"
    title = file_path.stem
    genre = "Uncategorized"
    duration_str = "0:00"
    bitrate_kbps = 0

    try:
        audio = File(file_path, easy=True)
        
        if audio is not None:
            # Extract basic tags if available
            if "artist" in audio and audio["artist"]:
                artist = audio["artist"][0].strip()
            elif "performer" in audio and audio["performer"]:
                artist = audio["performer"][0].strip()

            if "title" in audio and audio["title"]:
                title = audio["title"][0].strip()

            if "genre" in audio and audio["genre"]:
                genre = audio["genre"][0].strip()

            # Extract technical audio properties
            if hasattr(audio, "info") and audio.info:
                if hasattr(audio.info, "length"):
                    duration_str = format_duration(audio.info.length)
                if hasattr(audio.info, "bitrate") and audio.info.bitrate:
                    bitrate_kbps = int(audio.info.bitrate / 1000)

    except (ID3NoHeaderError, Exception):
        # Fail-safe: Keep default values if metadata reading fails
        pass

    # Sanitize strings to avoid invalid folder/file path characters
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        artist = artist.replace(char, "")
        genre = genre.replace(char, "")
        title = title.replace(char, "")

    return artist, title, genre, duration_str, bitrate_kbps


def organize_library(source_dir, output_dir, move_files=False, dry_run=False):
    """
    Scans source directory for audio files and organizes them into
    an Organized/Artist/Genre/Title.ext directory tree.
    """
    source_path = Path(source_dir)
    output_path = Path(output_dir)

    if not source_path.exists():
        print(f"Error: Source directory '{source_dir}' does not exist.")
        sys.exit(1)

    supported_extensions = {".mp3", ".wav", ".flac", ".m4a", ".ogg", ".aiff"}
    
    scanned_count = 0
    organized_count = 0
    skipped_count = 0

    print(f"\nScanning: {source_path.resolve()}")
    if dry_run:
        print("--- RUNNING IN DRY-RUN MODE (No files will be moved/copied) ---\n")
    else:
        print("-----------------------------------------------------------\n")

    for root, _, files in os.walk(source_path):
        for file in files:
            file_path = Path(root) / file
            
            # Skip files if they are already inside the destination directory
            if output_path.resolve() in file_path.resolve().parents:
                continue

            if file_path.suffix.lower() in supported_extensions:
                scanned_count += 1
                artist, title, genre, duration, bitrate = get_metadata(file_path)

                # Construct new folder hierarchy: Output/Artist/Genre/Title.ext
                dest_dir = output_path / artist / genre
                dest_file = dest_dir / f"{title}{file_path.suffix.lower()}"

                action_str = "move" if move_files else "copy"
                rel_dest = dest_file.relative_to(output_path.parent) if output_path.parent in dest_file.parents else dest_file

                try:
                    if not dry_run:
                        dest_dir.mkdir(parents=True, exist_ok=True)
                        if move_files:
                            shutil.move(str(file_path), str(dest_file))
                        else:
                            shutil.copy2(str(file_path), str(dest_file))

                    print(f"[ok] {file_path.name} -> {rel_dest}  ({duration}, {bitrate}kbps)")
                    organized_count += 1

                except Exception as e:
                    print(f"[ERROR] Failed to {action_str} {file_path.name}: {e}")
                    skipped_count += 1

    print(f"\nScanned {scanned_count} files | Organized {organized_count} | Skipped {skipped_count}\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Organize messy audio files into a clean Artist/Genre directory structure using embedded ID3 metadata."
    )
    parser.add_argument("source", type=str, help="Path to messy source audio directory")
    parser.add_argument(
        "--output", "-o", type=str, default="Organized", help="Destination directory name (Default: 'Organized')"
    )
    parser.add_argument(
        "--move", "-m", action="store_true", help="Move files instead of copying them"
    )
    parser.add_argument(
        "--dry-run", "-d", action="store_true", help="Simulate the organization process without modifying files"
    )

    args = parser.parse_args()
    organize_library(args.source, args.output, move_files=args.move, dry_run=args.dry_run)
