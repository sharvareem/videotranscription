# Install necessary dependencies
# pip install openai

import os
import openai
from datetime import datetime

# Set your OpenAI API key
openai.api_key = "your_openai_api_key"

# Directories for input and output
audio_text_folder = r"C:\Users\Sharvaree\Videos\CQF_Extracted_Slides"
output_script_folder = r"C:\Users\Sharvaree\Videos\CQF_Script"

# Create output folder if it doesn't exist
os.makedirs(output_script_folder, exist_ok=True)

def read_text_files(folder_path):
    """
    Read all text files in a folder and combine their content.
    """
    combined_text = ""
    for file_name in os.listdir(folder_path):
        if file_name.endswith(".txt"):
            file_path = os.path.join(folder_path, file_name)
            with open(file_path, "r", encoding="utf-8") as file:
                combined_text += file.read() + "\n\n"
    return combined_text

def generate_slide_content(prompt, model="gpt-4", max_tokens=1000):
    """
    Generate slide content using OpenAI API.
    """
    try:
        response = openai.Completion.create(
            engine=model,
            prompt=prompt,
            max_tokens=max_tokens,
            temperature=0.7
        )
        return response["choices"][0]["text"].strip()
    except Exception as e:
        print(f"Error generating content: {e}")
        return None

def create_script(audio_text, output_folder, topic="CQF Primer"):
    """
    Create a structured script with slides and narratives based on input text.
    """
    slides = []
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = os.path.join(output_folder, f"{topic}_Script_{timestamp}.txt")

    # Generate slide prompts
    prompt_intro = f"""
    The following content is an introduction to {topic}. 
    Create an engaging opening slide narrative including the importance of {topic}, current market trends, and relevant real-world use cases.
    """
    prompt_slides = f"""
    Based on the following content:
    {audio_text}
    Create a structured set of slides with the following structure:
    1. Slide Title
    2. Slide Content (bullet points)
    3. Slide Narrative (detailed explanation)
    Include current market news, relevant research references, and real-world use cases where applicable.
    """

    # Generate introduction slide
    intro_slide = generate_slide_content(prompt_intro)
    slides.append("Introduction Slide:\n" + intro_slide + "\n")

    # Generate slides based on audio content
    structured_slides = generate_slide_content(prompt_slides)
    slides.append("Slides Content:\n" + structured_slides + "\n")

    # Save slides to file
    with open(output_file, "w", encoding="utf-8") as file:
        for slide in slides:
            file.write(slide + "\n")

    print(f"Script created: {output_file}")
    return output_file

if __name__ == "__main__":
    # Read text from extracted slides
    print("Reading text from extracted slides...")
    audio_text = read_text_files(audio_text_folder)

    # Create a structured script for the new video
    print("Generating video script...")
    create_script(audio_text, output_script_folder)
