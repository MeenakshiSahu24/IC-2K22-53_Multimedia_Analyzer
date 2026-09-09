import os

IMAGE_EXTENSIONS = {
    ".jpg", ".jpeg", ".png", ".gif",
    ".bmp", ".tiff", ".webp"
}

AUDIO_EXTENSIONS = {
    ".mp3", ".wav", ".m4a",
    ".aac", ".flac", ".ogg"
}

VIDEO_EXTENSIONS = {
    ".mp4", ".mov", ".avi",
    ".mkv", ".webm", ".flv"
}


def validate_file(file_path):
    if not os.path.exists(file_path):
        return False

    if not os.path.isfile(file_path):
        return False

    return True


def get_file_size(file_path):
    return os.path.getsize(file_path)


def get_file_extension(file_path):
    return os.path.splitext(file_path)[1].lower()


def identify_file_type(file_path):

    extension = get_file_extension(file_path)

    if extension in IMAGE_EXTENSIONS:
        return "IMAGE"

    elif extension in AUDIO_EXTENSIONS:
        return "AUDIO"

    elif extension in VIDEO_EXTENSIONS:
        return "VIDEO"

    else:
        return "UNKNOWN"