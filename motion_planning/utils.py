import numpy as np

"""
    Function to map a frequency to a musical note.
    Input:
    - Frequency
    Output:
    - Musical note
"""
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
