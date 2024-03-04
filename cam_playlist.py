import essentia.standard as es
import os
import logging
from logging.handlers import RotatingFileHandler 
from random import shuffle  

# Full Camelot Wheel Dictionary
camelot_wheel = {
    '1A': ['12A', '1B'],
    '2A': ['1A', '3A', '2B'],
    '3A': ['2A', '4A', '3B'],
    '4A': ['3A', '5A', '4B'],
    '5A': ['4A', '6A', '5B'],
    '6A': ['5A', '7A', '6B'],
    '7A': ['6A', '8A', '7B'],
    '8A': ['7A', '9A', '8B'],
    '9A': ['8A', '10A', '9B'],
    '10A': ['9A', '11A', '10B'],
    '11A': ['10A', '12A', '11B'],
    '12A': ['11A', '1A', '12B'],
    '1B': ['12B', '2B'],
    '2B': ['1B', '3B', '2A'],
    '3B': ['2B', '4B', '3A'],
    '4B': ['3B', '5B', '4A'],
    '5B': ['4B', '6B', '5A'],
    '6B': ['5B', '7B', '6A'],
    '7B': ['6B', '8B', '7A'],
    '8B': ['7B', '9B', '8A'],
    '9B': ['8B', '10B', '9A'],
    '10B': ['9B', '11B', '10A'],
    '11B': ['10B', '12B', '11A'],
    '12B': ['11B', '1B', '12A']
}

def get_compatible_keys(key):
    """Returns a list of harmonically compatible keys based on the Camelot Wheel."""
    return camelot_wheel.get(key, [])

def is_compatible(key1, key2):
    """Checks if two keys are harmonically compatible according to the Camelot Wheel."""
    return key2 in get_compatible_keys(key1)

def translate_key_to_camelot(key):
    """Attempts to translate a standard key notation (e.g., C major) to Camelot notation (e.g., 8B).

    This is a simplified approach and may not work for all key signatures.
    """
    key_parts = key.split(' ')
    root_note = key_parts[0]
    mode = key_parts[1].lower()

    # Convert root note to Camelot Wheel format (A-B, 1-12)
    camelot_root = (ord(root_note.upper()) - ord('A')) % 12 + 1

    # Adjust for major/minor (Major = add 0, Minor = add 3)
    camelot_key = f"{camelot_root}{'B' if mode == 'major' else 'A'}"

    return camelot_key

def analyze_song(filename):
    """Analyzes a song file with Essentia and attempts to translate key to Camelot."""

    try:
        loader = es.MonoLoader(filename=filename)
        audio = loader()

        # RhythmExtractor for BPM
        rhythm_extractor = es.RhythmExtractor2013()
        bpm, _, _, _ = rhythm_extractor(audio)

        # Key Extractor 
        key_extractor = es.KeyExtractor()
        key, scale = key_extractor(audio)

        # Translate key to Camelot format (if not already)
        camelot_key = translate_key_to_camelot(key) if not key.startswith(' ') else key

        return {
            'filename': filename,
            'bpm': bpm,
            'key': camelot_key  
        }

    except essentia.standard.Error as e:
        logger.error(f"Error analyzing file '{filename}': {e}")
        return None  

    except Exception as e:  
        logger.warning(f"Unexpected issue with '{filename}': {e}")
        return None

def generate_playlist(music_directory, starting_key, mood='energetic'): 
    """Generates a playlist of musically compatible songs.

    Args:
        music_directory: The path to the directory containing your music files.
        starting_key: The initial Camelot key to base the playlist on.
        mood: Placeholder for future mood detection (not currently implemented).
    """
    song_data = []
    for file in os.listdir(music_directory):
        if file.endswith('.mp3'):  
            filepath = os.path.join(music_directory, file)
            analysis_result = analyze_song(filepath)
            if analysis_result is not None:  
                song_data.append(analysis_result)  

    # Simple sorting with some randomization for now
    compatible_songs = [song for song in song_data if is_compatible(song['key'], starting_key)]
    shuffle(compatible_songs) 

    playlist = [song['filename'] for song in compatible_songs]
    return playlist

# Enhanced Logging Configuration
log_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler = RotatingFileHandler('playlist_generator.log', maxBytes=10485760, backupCount=5)  
file_handler.setFormatter(log_formatter)
console_handler = logging.StreamHandler()
console_handler.setFormatter(log_formatter)
logger = logging.getLogger() 
logger.setLevel(logging.DEBUG)  
logger.addHandler(file_handler)
logger.addHandler(console_handler)

# Example Usage
starting_key = '5B' 
my_playlist = generate_playlist('music_library', starting_key)

# Print the generated playlist
print("Playlist:")
for song in my_playlist:
  print(song) 
