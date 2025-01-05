# videotranscription
https://sharvareem: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@github.com/sharvareem/videotranscription.git

git clone https://<your-username>:<PAT>@github.com/username/repo.git


Here are the steps to use **insanely-fast-whisper** for transcription in Python:

---

### **1. Install the Library**
Install the `insanely-fast-whisper` library from PyPI:

```bash
pip install insanely-fast-whisper
```

---

### **2. Import the Library**
In your Python script, import the necessary modules:

```python
from insanely_fast_whisper import WhisperModel
```

---

### **3. Load the Whisper Model**
Load the model with appropriate parameters. The available model sizes are `tiny`, `base`, `small`, `medium`, and `large`.

```python
# Load the Whisper model
model = WhisperModel("base", device="cuda")  # Use "cuda" for GPU, "cpu" for CPU
```

- Replace `"base"` with the model size of your choice.
- Use `"cuda"` if you have a compatible GPU; otherwise, use `"cpu"`.

---

### **4. Transcribe Audio**
Transcribe an audio file using the `transcribe` method.

```python
# Transcribe audio
audio_path = "path_to_audio_file.wav"
segments, info = model.transcribe(audio_path, beam_size=5)

# Print transcription results
print(f"Language detected: {info.language}")
print("Transcription:")
for segment in segments:
    print(f"[{segment.start:.2f} - {segment.end:.2f}] {segment.text}")
```

- **Parameters:**
  - `audio_path`: Path to your audio file (e.g., `.wav`, `.mp3`).
  - `beam_size`: Beam size for decoding (higher values improve accuracy but take longer).

---

### **5. Batch Processing (Optional)**
If you need to process multiple audio files, loop through a list:

```python
audio_files = ["file1.wav", "file2.wav", "file3.wav"]

for audio_file in audio_files:
    segments, info = model.transcribe(audio_file)
    print(f"Transcription for {audio_file}:")
    for segment in segments:
        print(f"[{segment.start:.2f} - {segment.end:.2f}] {segment.text}")
```

---

### **6. Save Transcriptions to File**
Save the results to a text file:

```python
output_path = "transcription.txt"

with open(output_path, "w") as f:
    for segment in segments:
        f.write(f"[{segment.start:.2f} - {segment.end:.2f}] {segment.text}\n")
```

---

### **7. Additional Configuration**
You can customize the transcription further by adjusting these parameters:
- **`language`**: Specify a target language (e.g., `"en"` for English).
- **`temperature`**: Adjust decoding temperature for diversity.
- **`vad_filter`**: Enable voice activity detection (default: `True`).

Example:

```python
segments, info = model.transcribe(
    audio_path,
    language="en",        # Force English transcription
    temperature=0.5,      # Adjust decoding diversity
    vad_filter=True       # Enable voice activity detection
)
```

---

### **8. Ensure CUDA Support**
If using GPU acceleration:
- Install PyTorch with CUDA support:
  ```bash
  pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
  ```
- Verify CUDA availability:
  ```python
  import torch
  print(torch.cuda.is_available())  # Should return True
  ```

---

With these steps, you can efficiently transcribe audio using `insanely-fast-whisper` in Python! Let me know if you encounter any issues.