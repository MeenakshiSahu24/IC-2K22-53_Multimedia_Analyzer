import sys
import os
from importlib.util import spec_from_file_location, module_from_spec

from file_utils import validate_file, identify_file_type
from report_generator import generate_report


def load_function(folder, filename, function_name):

    file_path = os.path.join(
        os.path.dirname(__file__),
        folder,
        filename
    )

    spec = spec_from_file_location(function_name, file_path)
    module = module_from_spec(spec)
    spec.loader.exec_module(module)

    return getattr(module, function_name)


# Load analyzer functions from their folders
analyze_image = load_function(
    "01_Image_Analyzer",
    "image_analyzer.py",
    "analyze_image"
)

analyze_audio = load_function(
    "03_Audio_Analyzer",
    "audio_analyzer.py",
    "analyze_audio"
)

analyze_video = load_function(
    "02_Video_Analyzer",
    "video_analyzer.py",
    "analyze_video"
)


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