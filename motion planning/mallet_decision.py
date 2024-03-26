import librosa
import numpy as np

"""
Function to decide which mallet to use for each key in the song.
Input: 
- List of notes
- Map of pairs of keys to distance
Output:
- List of pairs of keys where the first key is for left mallet and the second key is for right mallet
"""
def mallet_decision(notes, distance_map):
     # If there are no notes, return an empty list
    if not notes:
        return []

    # Initialize mallet positions to the first note (or the first two different notes if available)
    left_mallet = right_mallet = notes[0] # These should be different notes
    if len(notes) > 1 and notes[0] != notes[1]:
        right_mallet = notes[1]

    decisions = []

    for note in notes:
        # If the note is the same as one of the mallets, prefer that mallet
        if note == left_mallet or note == right_mallet:
            decisions.append((left_mallet, right_mallet))
            continue

        # Calculate distances from the current note to the left and right mallet positions
        left_distance = distance_map.get((left_mallet, note), float('inf'))
        right_distance = distance_map.get((right_mallet, note), float('inf'))

        # Decide which mallet to use based on the distance and future considerations
        if left_distance <= right_distance:
            left_mallet = note
        else:
            right_mallet = note

        decisions.append((left_mallet, right_mallet))

    # (left_note, right_note)
    return decisions

def freq_to_note(freq):
    """Map a frequency to a musical note."""
    A4 = 440
    C0 = A4*np.power(2, -4.75)
    if freq == 0: return None  # Silence or unvoiced
    h = round(12*np.log2(freq/C0))
    octave = h // 12
    n = h % 12
    note = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B'][n] + str(octave)
    return note

def detect_notes(audio_path):
    y, sr = librosa.load(audio_path)
    pitches, magnitudes = librosa.piptrack(y=y, sr=sr)
    # Taking the maximum magnitude pitch for each time frame
    pitch_times = np.argmax(magnitudes, axis=0)
    pitch_freqs = [pitches[pitch_times[i], i] for i in range(pitches.shape[1])]
    
    # Filtering out low amplitudes
    pitch_freqs_filtered = [freq if magnitudes[pitch_times[i], i] > np.median(magnitudes) else 0 for i, freq in enumerate(pitch_freqs)]
    
    notes = [freq_to_note(freq) for freq in pitch_freqs_filtered]

    # Simplify: Collapsing consecutive identical notes
    simplified_notes = [notes[0]]
    for note in notes[1:]:
        if note != simplified_notes[-1]:
            simplified_notes.append(note)
    
    # Note durations/timing is simplified in this example
    # More sophisticated analysis would be required for accurate timing
    return simplified_notes

