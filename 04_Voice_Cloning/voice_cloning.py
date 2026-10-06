import os
import requests


def speech_to_text(api_key, audio_file_path, output_text_path):
    """
    Convert an audio file into text using ElevenLabs Scribe
    (Speech-to-Text API).
    """

    print("\n[1/2] Uploading audio file to ElevenLabs...")

    # ElevenLabs Speech-to-Text API
    stt_url = "https://api.elevenlabs.io/v1/speech-to-text"

    headers = {
        "xi-api-key": api_key
    }

    # Scribe model
    data = {
        "model_id": "scribe_v2"
    }

    # Open audio file
    with open(audio_file_path, "rb") as f:
        files = {
            "file": (
                os.path.basename(audio_file_path),
                f,
                "audio/mpeg"
            )
        }

        response = requests.post(
            stt_url,
            headers=headers,
            data=data,
            files=files
        )

    # Check response
    if response.status_code != 200:
        print("\nError converting speech to text.")
        print(f"Status Code: {response.status_code}")
        print(f"Details: {response.text}")
        return

    # Get transcription
    result = response.json()
    transcription = result.get("text", "")

    print("\n[2/2] Speech-to-text conversion completed!")

    print("\nTranscribed Text:")
    print("-" * 50)
    print(transcription)
    print("-" * 50)

    # Save transcription to a text file
    with open(output_text_path, "w", encoding="utf-8") as f:
        f.write(transcription)

    print(f"\nText saved successfully to:")
    print(output_text_path)


def main():

    print("=" * 55)
    print("ELEVENLABS SPEECH-TO-TEXT (SCRIBE)")
    print("=" * 55)

    # Get API Key
    api_key = input("\nEnter your ElevenLabs API Key: ").strip()

    if not api_key:
        print("API Key is required! Exiting...")
        return

    # Folder containing this Python script
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Audio input file
    audio_file = os.path.join(
        script_dir,
        "sample_audio.mp3"
    )

    # Output text file
    output_file = os.path.join(
        script_dir,
        "transcription.txt"
    )

    # Check audio file
    if not os.path.exists(audio_file):
        print(f"\nError: Audio file not found!")
        print(f"Please place '{os.path.basename(audio_file)}'")
        print("in the same folder as this Python file.")
        return

    # Start transcription
    speech_to_text(
        api_key,
        audio_file,
        output_file
    )


if __name__ == "__main__":
    main()