import os
from tqdm import tqdm
from pydub import AudioSegment

INPUT_PATH = "output_wav/"
OUTPUT_PATH = "book.wav"

def combine_wav_files(folder_path, start_num, end_num, silence_ms):
    """
    Finds, sorts, and combines a numerical range of .wav files from a specified folder.
    """
    def get_numeric_part(filename):
        """Helper function to extract the number from a filename for sorting."""
        return int(os.path.splitext(filename)[0])

    # Find, filter, and sort the wav files numerically
    all_files = [f for f in os.listdir(folder_path) if f.endswith('.wav')]

    files_in_range = []
    for f in all_files:
        # A simple try/except to handle non-numeric filenames gracefully
        try:
            num = get_numeric_part(f)
            if start_num <= num <= end_num:
                files_in_range.append(f)
        except ValueError:
            continue # Skip files that don't have a numeric name

    wav_files = sorted(files_in_range, key=get_numeric_part)

    if not wav_files:
        print(f"No matching .wav files found in '{folder_path}' for the range {start_num}-{end_num}.")
        return

    # Create the silent segment
    silence = AudioSegment.silent(duration=silence_ms)

    # Combine the audio files
    first_file_path = os.path.join(folder_path, wav_files[0])
    combined_audio = AudioSegment.from_wav(first_file_path)

    for filename in tqdm(wav_files[1:], desc="Combining Audio"):
        file_path = os.path.join(folder_path, filename)
        next_audio = AudioSegment.from_wav(file_path)
        combined_audio += silence + next_audio

    # Export the final combined audio
    output_filename = OUTPUT_PATH
    combined_audio.export(output_filename, format="wav")
    print(f"Successfully created '{output_filename}'.")


folder_path = INPUT_PATH if INPUT_PATH else '.'

start_num_input = 76
end_num_input = 3521
silence_ms_input = 500

combine_wav_files(folder_path, start_num_input, end_num_input, silence_ms_input)