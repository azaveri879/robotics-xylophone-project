import numpy as np

"""
    Function to map a frequency to a musical note.
    Input:
    - Frequency
    Output:
    - Musical note
"""
def freq_to_note(freq):
    """
    Convert frequency to musical note.
    """
    if freq <= 0:
        return "No Note"
    NOTES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    A4 = 440
    C0 = A4 * pow(2, -4.75)
    h = round(12 * np.log2(freq / C0))
    octave = h // 12
    index = h % 12
    if index < 0 or index >= len(NOTES):
        return "Invalid Note"
    return NOTES[index] + str(octave)
