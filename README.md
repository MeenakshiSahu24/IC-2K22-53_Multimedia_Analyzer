# Consolidated Multimedia Analyzer

A Python-based multimedia metadata analyzer that automatically identifies whether a given file is an image, audio, or video and extracts its metadata.

## Features

- Automatically detects file type
- Extracts image metadata
- Extracts audio metadata
- Extracts video metadata
- Generates a JSON report
- Validates files before analysis
- Supports multiple multimedia formats

## Supported File Types

### Images
- JPG
- JPEG
- PNG
- GIF
- BMP
- TIFF
- WEBP

### Audio
- MP3
- WAV
- M4A
- AAC
- FLAC
- OGG

### Video
- MP4
- MOV
- AVI
- MKV
- WEBM
- FLV

## Technologies Used

- Python
- Pillow
- FFmpeg / FFprobe
- JSON

## Project Structure

multimedia_analyzer/
│
├── main.py
├── file_utils.py
├── image_analyzer.py
├── audio_analyzer.py
├── video_analyzer.py
├── report_generator.py
│
├── samples/
│
└── reports/
    └── report.json

## How It Works

The user provides a multimedia file.

The application:

1. Validates the file.
2. Identifies the file type using its extension.
3. Selects the appropriate analyzer.
4. Extracts metadata.
5. Generates a JSON report.

## How to Run

Install Pillow:

```bash
pip install Pillow