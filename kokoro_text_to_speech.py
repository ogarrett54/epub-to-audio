from kokoro import KPipeline
import soundfile as sf
import torch
from tqdm import tqdm

BOOK_PATH = "book.txt"
OUTPUT_DIR = "output_wav/"

print("Setting up pipeline...")
pipeline = KPipeline(lang_code='a')

print("Reading book...")
with open(BOOK_PATH, 'r', encoding="utf-8") as f:
    text = f.read()

print("Setting up generator...")
generator = pipeline(
    text,
    voice='am_michael',
    speed=1,
    split_pattern=r'\n+'
)

for i, (gs, ps, audio) in tqdm(enumerate(generator), desc="Generating Audio"):
    sf.write(f'{OUTPUT_DIR}{i}.wav', audio, 24000)