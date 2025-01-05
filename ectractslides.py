# Install necessary dependencies before running this script
# pip install opencv-python pytesseract tqdm

import os
import cv2
import pytesseract
from tqdm import tqdm

def create_output_folder(video_name, base_folder):
    """
    Create an output folder named after the video.
    """
    folder_path = os.path.join(base_folder, video_name)
    os.makedirs(folder_path, exist_ok=True)
    return folder_path

def extract_frame_diff_percentage(frame1, frame2):
    """
    Calculate the percentage of difference between two frames.
    """
    diff = cv2.absdiff(frame1, frame2)
    gray_diff = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    non_zero_count = cv2.countNonZero(gray_diff)
    total_pixels = gray_diff.size
    return (non_zero_count / total_pixels) * 100

def save_frame_with_text(frame, video_name, timestamp, output_folder):
    """
    Save the frame and its extracted text.
    """
    frame_file_name = f"{video_name}_{timestamp}.jpg"
    frame_file_path = os.path.join(output_folder, frame_file_name)

    # Save the frame as an image
    cv2.imwrite(frame_file_path, frame)

    # Extract text from the frame
    text = pytesseract.image_to_string(frame)

    # Save the text in a corresponding text file
    text_file_name = f"{video_name}_{timestamp}.txt"
    text_file_path = os.path.join(output_folder, text_file_name)
    with open(text_file_path, "w", encoding="utf-8") as text_file:
        text_file.write(text)

    print(f"Saved slide: {frame_file_name} with text.")
    return frame_file_path

def process_video(video_path, output_base_folder, threshold=20.0):
    """
    Process a video to extract slides based on frame changes.
    """
    video_name = os.path.splitext(os.path.basename(video_path))[0]
    output_folder = create_output_folder(video_name, output_base_folder)

    # Open video capture
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Failed to open video: {video_path}")
        return

    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    success, prev_frame = cap.read()

    if not success:
        print(f"Failed to read the first frame of {video_path}")
        return

    prev_frame = cv2.resize(prev_frame, (640, 360))  # Resize to a manageable size
    slide_count = 0

    with tqdm(total=frame_count, desc=f"Processing {video_name}", unit="frame") as pbar:
        while True:
            success, current_frame = cap.read()
            if not success:
                break

            current_frame_resized = cv2.resize(current_frame, (640, 360))
            diff_percentage = extract_frame_diff_percentage(prev_frame, current_frame_resized)

            if diff_percentage > threshold:
                timestamp = cap.get(cv2.CAP_PROP_POS_MSEC) // 1000  # Timestamp in seconds
                timestamp_str = f"{int(timestamp // 60):02d}_{int(timestamp % 60):02d}"

                save_frame_with_text(current_frame, video_name, timestamp_str, output_folder)
                slide_count += 1
                prev_frame = current_frame_resized

            pbar.update(1)

    cap.release()
    print(f"Finished processing {video_name}. Extracted {slide_count} slides.")

if __name__ == "__main__":
    # Path to your video folder
    input_folder = r"C:\Users\Sharvaree\Videos\CQF"
    output_folder = r"C:\Users\Sharvaree\Videos\CQF_Extracted_Slides"

    # Ensure Tesseract OCR is installed and configured
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

    # Process each video in the input folder
    for video_file in os.listdir(input_folder):
        if video_file.endswith(".mkv") or video_file.endswith(".mp4"):
            video_path = os.path.join(input_folder, video_file)
            process_video(video_path, output_folder)
