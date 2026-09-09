import json
import os
import sys
import subprocess


def format_file_size(size_bytes):
    """Convert bytes into a readable file size."""
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 ** 2:
        return f"{size_bytes / 1024:.2f} KB"
    elif size_bytes < 1024 ** 3:
        return f"{size_bytes / (1024 ** 2):.2f} MB"
    else:
        return f"{size_bytes / (1024 ** 3):.2f} GB"


def format_duration(seconds):
    """Convert seconds into HH:MM:SS format."""
    try:
        seconds = float(seconds)
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)

        return f"{hours:02d}:{minutes:02d}:{secs:02d}"
    except (ValueError, TypeError):
        return "N/A"


def analyze_audio(file_path):
    """Extract audio metadata using FFprobe and return it as a dictionary."""

    if not os.path.exists(file_path):
        return {
            "error": "File does not exist."
        }

    try:
        command = [
            "ffprobe",
            "-v", "quiet",
            "-print_format", "json",
            "-show_format",
            "-show_streams",
            file_path
        ]

        result = subprocess.run(
            command,
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            return {
                "error": "Unable to analyze the audio file.",
                "details": result.stderr
            }

        data = json.loads(result.stdout)

        # File information
        file_name = os.path.basename(file_path)
        file_size = os.path.getsize(file_path)

        # Format information
        format_data = data.get("format", {})

        container = format_data.get(
            "format_name",
            "N/A"
        )

        duration = format_duration(
            format_data.get("duration")
        )

        # Find audio stream
        audio_stream = None

        for stream in data.get("streams", []):

            if stream.get("codec_type") == "audio":
                audio_stream = stream
                break

        if audio_stream is None:
            return {
                "error": "No audio stream found."
            }

        # Audio information
        codec = audio_stream.get(
            "codec_name",
            "N/A"
        )

        channels = audio_stream.get(
            "channels",
            "N/A"
        )

        sample_rate = audio_stream.get(
            "sample_rate",
            "N/A"
        )

        if sample_rate != "N/A":
            sample_rate = f"{sample_rate} Hz"

        bit_rate = audio_stream.get("bit_rate")

        if bit_rate:
            bit_rate = f"{float(bit_rate) / 1000:.2f} kbps"
        else:
            bit_rate = "N/A"

        codec_long_name = audio_stream.get(
            "codec_long_name",
            "N/A"
        )

        # Additional metadata
        tags = audio_stream.get("tags", {})
        format_tags = format_data.get("tags", {})

        additional_metadata = {}

        if tags:
            additional_metadata["stream_tags"] = tags

        if format_tags:
            additional_metadata["format_tags"] = format_tags

        # RETURN metadata
        return {
            "file_type": "AUDIO",
            "file_name": file_name,
            "file_size": format_file_size(file_size),
            "container": container,
            "duration": duration,
            "audio": {
                "codec": codec,
                "channels": channels,
                "sampling_rate": sample_rate,
                "bit_rate": bit_rate
            },
            "metadata": {
                "codec_name": codec_long_name,
                "additional": additional_metadata
            }
        }

    except FileNotFoundError:

        return {
            "error": "FFprobe was not found. "
                     "Make sure FFmpeg/FFprobe is installed "
                     "and added to PATH."
        }

    except json.JSONDecodeError:

        return {
            "error": "Could not read FFprobe output."
        }

    except Exception as e:

        return {
            "error": f"Error: {e}"
        }


# Main program
if __name__ == "__main__":

    if len(sys.argv) < 2:
        print("Usage:")
        print("python audio_analyzer.py <audio_file>")
        sys.exit(1)

    audio_file = sys.argv[1]

    analyze_audio(audio_file)