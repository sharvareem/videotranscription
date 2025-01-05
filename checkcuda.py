from transformers import pipeline
import torch

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
pipe = pipeline(task="automatic-speech-recognition", device=device)
print(pipe.device)
