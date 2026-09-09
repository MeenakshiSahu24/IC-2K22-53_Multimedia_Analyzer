import sys
import os
from PIL import Image, ExifTags

def format_file_size(size_bytes):
    """Format file size in human-readable units."""
    if size_bytes < 1024:
        return f"{size_bytes} Bytes"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.2f} KB"
    else:
        return f"{size_bytes / (1024 * 1024):.2f} MB"

def analyze_image(image_path):

    if not os.path.isfile(image_path):
        return {
            "error": f"File '{image_path}' not found."
        }

    file_name = os.path.basename(image_path)
    file_size = format_file_size(os.path.getsize(image_path))

    try:
        with Image.open(image_path) as img:

            width, height = img.size
            file_format = img.format if img.format else "Unknown"
            color_mode = img.mode

            # Resolution / DPI
            dpi = img.info.get("dpi")

            if dpi:
                resolution = f"{int(dpi[0])} x {int(dpi[1])} DPI"
            else:
                resolution = "N/A"

            # EXIF metadata
            exif_data = {}

            raw_exif = img.getexif() if hasattr(img, "getexif") else None

            if raw_exif:
                for tag_id, value in raw_exif.items():

                    tag_name = ExifTags.TAGS.get(
                        tag_id,
                        str(tag_id)
                    )

                    exif_data[tag_name] = value

            # Common EXIF information
            make = exif_data.get("Make", "")
            model = exif_data.get("Model", "")

            camera = (
                f"{make} {model}".strip()
                if (make or model)
                else "N/A"
            )

            date_taken = (
                exif_data.get("DateTimeOriginal")
                or exif_data.get("DateTime")
                or "N/A"
            )

            orientation = exif_data.get(
                "Orientation",
                "N/A"
            )

            # Remove binary EXIF values
            additional_exif = {}

            for tag, value in exif_data.items():

                if tag not in {
                    "Make",
                    "Model",
                    "DateTimeOriginal",
                    "DateTime",
                    "Orientation"
                }:

                    if not isinstance(
                        value,
                        (bytes, bytearray)
                    ):
                        additional_exif[tag] = str(value)

            # RETURN metadata instead of printing it
            return {
                "file_type": "IMAGE",
                "file_name": file_name,
                "file_size": file_size,
                "file_format": file_format,
                "width": width,
                "height": height,
                "resolution": resolution,
                "color_mode": color_mode,
                "exif": {
                    "camera": camera,
                    "date_taken": str(date_taken),
                    "orientation": str(orientation),
                    "additional": additional_exif
                }
            }

    except Exception as e:

        return {
            "error": f"Error reading image '{image_path}': {e}"
        }
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python image_analyzer.py <path_to_image>")
    else:
        analyze_image(sys.argv[1])