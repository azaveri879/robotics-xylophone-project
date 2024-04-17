from xylophone_player import XylophonePlayer


if __name__ == "__main__":
    
    xylophone_player = XylophonePlayer()
    # #notes= xylophone.record_song()
    # #audio_path = '/Users/aakash/robotics-xylophone-project/motion_planning/recorded_audio.wav'
    audio_path = '/Users/aakash/robotics-xylophone-project/xylophone-melody_76bpm_C#_major.wav'
    notes = xylophone_player.detect_notes(audio_path)
    # print(notes)

    # #decisions = xylophone.mallet_decision(notes)
    # #print(decisions)
    
    # xylophone.set_song(['C#2', 'E2', 'F#2', 'F#2', 'G#2', 'F#2', 'E2', 'F#2', 'B2', 'E2', 'F#2'])
    # xylophone.learn_to_play(episodes=1000)

    # optimal_play = xylophone.get_optimal_play()

    # print("Optimal mallet usage for each note:")
    # for note, action in optimal_play:
    #     print(f"Note: {note}, Use: {'Left Mallet' if action == 'L' else 'Right Mallet'}")
    
    # print(xylophone.q_table)

    xylophone_player.set_song(notes)
    xylophone_player.learn_to_play(episodes=1000)
    print("Optimal mallet usage for each note:")
    optimal_play = xylophone_player.get_optimal_play()
    for note, action, left_pos, right_pos in optimal_play:
        print(f"Note: {note}, Use: {'Left Mallet' if action == 'L' else 'Right Mallet'}, Left Pos: {left_pos}, Right Pos: {right_pos}")

   
    