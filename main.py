import sys

from file_utils import validate_file, identify_file_type
from image_analyzer import analyze_image
from audio_analyzer import analyze_audio
from video_analyzer import analyze_video
from report_generator import generate_report


def main():

    if len(sys.argv) != 2:
        print("Usage:")
        print("python main.py <file_path>")
        return

    file_path = sys.argv[1]

    # Validate file
    if not validate_file(file_path):
        print("Error: File does not exist or is not a valid file.")
        return

    # Identify file type
    file_type = identify_file_type(file_path)

    print(f"File Type Detected: {file_type}")

    if file_type == "IMAGE":
        metadata = analyze_image(file_path)

    elif file_type == "AUDIO":
        metadata = analyze_audio(file_path)

    elif file_type == "VIDEO":
        metadata = analyze_video(file_path)

    else:
        print("Error: Unsupported file type.")
        return

    # Check for analyzer error
    if "error" in metadata:
        print("Error:", metadata["error"])
        return

    # Generate report
    generate_report(metadata)


if __name__ == "__main__":
    main()