import os
import sys
import json
import subprocess


def format_file_size(size_bytes):
    """Convert bytes into KB, MB or GB."""

    if size_bytes < 1024:
        return f"{size_bytes} Bytes"

    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.2f} KB"

    elif size_bytes < 1024 * 1024 * 1024:
        return f"{size_bytes / (1024 * 1024):.2f} MB"

    else:
        return f"{size_bytes / (1024 * 1024 * 1024):.2f} GB"


def format_duration(seconds):
    """Convert seconds into HH:MM:SS format."""

    try:
        seconds = float(seconds)

        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        seconds = int(seconds % 60)

        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

    except:
        return "Not Available"


def analyze_video(video_path):
    """Extract video metadata using FFprobe and return it as a dictionary."""

    if not os.path.isfile(video_path):
        return {"error": f"File not found - {video_path}"}

    try:
        command = [
            "ffprobe",
            "-v", "quiet",
            "-print_format", "json",
            "-show_format",
            "-show_streams",
            video_path
        ]

        result = subprocess.run(
            command,
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            return {
                "error": "Unable to analyze the video.",
                "details": result.stderr
            }

        data = json.loads(result.stdout)

        file_name = os.path.basename(video_path)
        file_size = os.path.getsize(video_path)

        format_data = data.get("format", {})

        container = format_data.get(
            "format_name",
            "Not Available"
        )

        format_long_name = format_data.get(
            "format_long_name",
            "Not Available"
        )

        duration = format_duration(
            format_data.get("duration")
        )

        # Find video and audio streams
        video_stream = None
        audio_stream = None

        for stream in data.get("streams", []):
            if stream.get("codec_type") == "video":
                video_stream = stream

            elif stream.get("codec_type") == "audio":
                audio_stream = stream

        # ---------------- VIDEO INFORMATION ----------------

        if video_stream:

            width = video_stream.get(
                "width",
                "Not Available"
            )

            height = video_stream.get(
                "height",
                "Not Available"
            )

            resolution = f"{width} x {height}"

            frame_rate = video_stream.get(
                "r_frame_rate",
                "Not Available"
            )

            if "/" in str(frame_rate):
                numerator, denominator = frame_rate.split("/")

                try:
                    frame_rate = (
                        f"{float(numerator) / float(denominator):.2f} FPS"
                    )
                except:
                    pass

            codec = video_stream.get(
                "codec_name",
                "Not Available"
            )

            bit_rate = video_stream.get(
                "bit_rate",
                "Not Available"
            )

            if bit_rate != "Not Available":

                try:
                    bit_rate = (
                        f"{int(bit_rate) / 1000:.2f} kbps"
                    )
                except:
                    pass

        else:

            resolution = "Not Available"
            frame_rate = "Not Available"
            codec = "Not Available"
            bit_rate = "Not Available"

        # ---------------- AUDIO INFORMATION ----------------

        if audio_stream:

            audio_codec = audio_stream.get(
                "codec_name",
                "Not Available"
            )

            channels = audio_stream.get(
                "channels",
                "Not Available"
            )

            sample_rate = audio_stream.get(
                "sample_rate",
                "Not Available"
            )

            if sample_rate != "Not Available":
                sample_rate = f"{sample_rate} Hz"

            audio_bit_rate = audio_stream.get(
                "bit_rate",
                "Not Available"
            )

            if audio_bit_rate != "Not Available":

                try:
                    audio_bit_rate = (
                        f"{int(audio_bit_rate) / 1000:.2f} kbps"
                    )
                except:
                    pass

        else:

            audio_codec = "Not Available"
            channels = "Not Available"
            sample_rate = "Not Available"
            audio_bit_rate = "Not Available"

        # ---------------- ADDITIONAL METADATA ----------------

        metadata = format_data.get("tags", {})

        return {
            "file_type": "VIDEO",
            "file_name": file_name,
            "file_size": format_file_size(file_size),
            "container": container,
            "duration": duration,

            "video": {
                "resolution": resolution,
                "frame_rate": frame_rate,
                "bit_rate": bit_rate,
                "codec": codec
            },

            "audio": {
                "codec": audio_codec,
                "channels": channels,
                "sampling_rate": sample_rate,
                "bit_rate": audio_bit_rate
            },

            "metadata": {
                "format": format_long_name,
                "additional": metadata
            }
        }

    except FileNotFoundError:

        return {
            "error": (
                "FFprobe was not found. "
                "Make sure FFmpeg/FFprobe is installed "
                "and added to PATH."
            )
        }

    except json.JSONDecodeError:

        return {
            "error": "Could not read FFprobe output."
        }

    except Exception as error:

        return {
            "error": f"Error analyzing video: {error}"
        }

def main():

    if len(sys.argv) != 2:

        print("Usage:")
        print("python video_analyzer.py <video_path>")

        return

    video_path = sys.argv[1]

    analyze_video(video_path)


if __name__ == "__main__":
    main()