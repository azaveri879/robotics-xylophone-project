from xylophone_player import XylophonePlayer


if __name__ == "__main__":
    
    xylophone = XylophonePlayer()

    audio_path = '/Users/aakash/robotics-xylophone-project/xylophone-melody_76bpm_C#_major.wav'
    notes = xylophone.detect_notes(audio_path)
    print(notes)

    decisions = xylophone.mallet_decision(notes)
    #print(decisions)

    xylophone.set_song(['G1','G2','G3'])
    xylophone.learn_to_play(episodes=500)

    optimal_play = xylophone.get_optimal_play()

    print("Optimal mallet usage for each note:")
    for note, action in optimal_play:
        print(f"Note: {note}, Use: {'Left Mallet' if action == 'L' else 'Right Mallet'}")
    