import os
import subprocess
import logging
from tqdm import tqdm
import shutil

# Configure logging
logging.basicConfig(
    filename="process_log.log",
    filemode="a",
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger()

def set_cuda_device(device_id="0"):
    """
    Set the CUDA_VISIBLE_DEVICES environment variable.
    """
    os.environ["CUDA_VISIBLE_DEVICES"] = device_id
    logger.info(f"Set CUDA_VISIBLE_DEVICES to {device_id}")
    print(f"Set CUDA_VISIBLE_DEVICES to {device_id}")

def check_cuda():
    """
    Check if CUDA is available.
    :return: True if CUDA is available, otherwise False.
    """
    try:
        import torch
        if torch.cuda.is_available():
            logger.info(f"CUDA device found: {torch.cuda.get_device_name(0)}")
            print(f"CUDA device found: {torch.cuda.get_device_name(0)}")
            return True
        else:
            logger.error("CUDA device not available.")
            print("CUDA device not available.")
            return False
    except Exception as e:
        logger.error(f"Error checking CUDA availability: {e}")
        print(f"Error checking CUDA availability: {e}")
        return False

def extract_audio(input_file, output_file, progress_bar):
    """
    Extract audio from an MKV file using ffmpeg.
    """
    if os.path.exists(output_file):
        logger.info(f"Audio already extracted: {output_file}")
        print(f"Audio already extracted: {output_file}")
        progress_bar.update(1)  # Mark extraction as done
        return output_file

    try:
        print(f"Extracting audio from: {input_file} to {output_file}")
        logger.info(f"Extracting audio from: {input_file} to {output_file}")
        command = [
            "ffmpeg",
            "-i", input_file,
            "-vn",
            "-acodec", "pcm_s16le",
            "-ar", "44100",
            "-ac", "2",
            output_file
        ]
        subprocess.run(command, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        logger.info(f"Audio extracted to: {output_file}")
        print(f"Audio extracted to: {output_file}")
        progress_bar.update(1)  # Mark extraction as done
        return output_file
    except subprocess.CalledProcessError as e:
        logger.error(f"Error extracting audio from {input_file}: {e}")
        print(f"Error extracting audio from {input_file}: {e}")
        return None

def transcribe_audio_with_cli(audio_path, output_file_path, language="en", batch_size=2, progress_bar=None):
    """
    Transcribe an audio file using insanely-fast-whisper CLI and rename the output file.
    """
    if os.path.exists(output_file_path):
        logger.info(f"Transcription already exists: {output_file_path}")
        print(f"Transcription already exists: {output_file_path}")
        if progress_bar:
            progress_bar.update(1)  # Mark transcription as done
        return

    try:
        print(f"Transcribing audio file: {audio_path}")
        logger.info(f"Transcribing audio file: {audio_path}")
        command = [
            "insanely-fast-whisper",
            "--file-name", audio_path,
            "--language", language,
            "--batch-size", str(batch_size),
        ]
        logger.info(f"Running command: {' '.join(command)}")
        subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        logger.info(f"Transcription completed for: {audio_path}")
        print(f"Transcription completed for: {audio_path}")

        # Rename the default output file (output.json) to match the desired file name
        default_output_path = "output.json"
        if os.path.exists(default_output_path):
            shutil.move(default_output_path, output_file_path)
            logger.info(f"Renamed {default_output_path} to {output_file_path}")
            print(f"Renamed {default_output_path} to {output_file_path}")
        else:
            logger.error(f"Default output file {default_output_path} not found.")
            print(f"Default output file {default_output_path} not found.")
        if progress_bar:
            progress_bar.update(1)  # Mark transcription as done
    except subprocess.CalledProcessError as e:
        logger.error(f"Error during transcription for {audio_path}: {e.stderr.decode('utf-8')}")
        print(f"Error during transcription for {audio_path}: {e.stderr.decode('utf-8')}")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        print(f"Unexpected error: {e}")

def process_folder(folder_path, output_folder, language="en", batch_size=2):
    """
    Process all MKV files in a folder, extract audio, transcribe, and save results.
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    files = [f for f in os.listdir(folder_path) if f.endswith(".mkv")]
    if not files:
        logger.warning("No MKV files found in the folder.")
        print("No MKV files found in the folder.")
        return

    for file_name in files:
        input_file = os.path.join(folder_path, file_name)
        base_name = os.path.splitext(file_name)[0]
        audio_file = os.path.join(output_folder, f"{base_name}.wav")
        transcription_file = os.path.join(output_folder, f"{base_name}.json")

        logger.info(f"Processing file: {file_name}")
        print(f"Processing file: {file_name}")

        # Create a progress bar for each file
        with tqdm(total=2, desc=f"Processing {file_name}", unit="task") as file_progress:
            # Extract audio
            extracted_audio = extract_audio(input_file, audio_file, progress_bar=file_progress)
            if extracted_audio:
                # Transcribe audio
                transcribe_audio_with_cli(
                    audio_path=extracted_audio,
                    output_file_path=transcription_file,
                    language=language,
                    batch_size=batch_size,
                    progress_bar=file_progress
                )
            else:
                logger.error(f"Failed to process file: {file_name}")
                print(f"Failed to process file: {file_name}")

# Main function
if __name__ == "__main__":
    set_cuda_device("0")

    if not check_cuda():
        print("CUDA device not available. Exiting.")
        exit(1)

    input_folder = r"C:\Users\Sharvaree\Videos\CQF"  # Replace with your folder path
    output_folder = r"C:\Users\Sharvaree\Videos\CQF_Output"  # Folder for outputs

    process_folder(input_folder, output_folder, language="en", batch_size=2)
