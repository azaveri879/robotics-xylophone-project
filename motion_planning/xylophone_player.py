import random
import librosa
# from utils import freq_to_note
import numpy as np
# import sounddevice as sd
from scipy.io.wavfile import write
import wavio as wv

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

class XylophonePlayer:
    def __init__(self):
        """
        Initialize the Xylophone Player class with default settings for note lists,
        mallet positions, the Q-table for learning, and the current song.
        """
        self.distance_map = {}
        self.notes = []  # List to store the xylophone notes
        self.right_mallet = None  # Current position of the right mallet
        self.left_mallet = None  # Current position of the left mallet
        self.setup_notes()  # Setup the notes and their distances
        self.q_table = {}  # Q-table for learning the optimal actions
        self.current_song = []  # Current song (sequence of notes) to be played
        self.freq = 44100  # Sample rate
        self.duration = 5  # Duration of recording in seconds


    def record_song(self):
        """
        Record a song from the microphone and analyze it directly to get notes.
        """
        # Record audio from the microphone
        audio = sd.rec(int(self.freq * self.duration), samplerate=self.freq, channels=1, dtype='float32')
        sd.wait()  # Wait until recording is finished

        # Normalize audio and ensure it is in floating-point format suitable for librosa
        audio = audio.flatten()  # Flatten the array to 1D
        audio = audio / np.max(np.abs(audio))  # Normalize audio to -1.0 to 1.0

        # Directly convert the recorded audio array to notes
        notes = self.detect_notes_from_array(audio, self.freq)
        return notes

    def detect_notes_from_array(self, audio, sr):
        """
        Detect musical notes from an audio array using pitch tracking.
        """
        pitches, magnitudes = librosa.piptrack(y=audio, sr=sr)
        pitch_times = np.argmax(magnitudes, axis=0)
        pitch_freqs = [pitches[pitch_times[i], i] for i in range(pitches.shape[1])]

        threshold = np.median(magnitudes) * 1.5  # Threshold to consider a pitch significant
        pitch_freqs_filtered = [freq for i, freq in enumerate(pitch_freqs) if magnitudes[pitch_times[i], i] > threshold and freq > 0]

        notes = [freq_to_note(freq) for freq in pitch_freqs_filtered]
        simplified_notes = [notes[0]] if notes else []
        for note in notes[1:]:
            if note != simplified_notes[-1]:
                simplified_notes.append(note)

        return simplified_notes

        
    def setup_notes(self):
        """
        Setup the initial notes on the xylophone and initialize the mallet positions.
        This function defines the distances between all pairs of notes to facilitate quick lookup during play.
        """
        front_notes = ['G1', 'G#1', 'A1', 'A#1', 'B1', 'C1', 'C#1', 'D1', 'D#1', 'E1', 'F1', 'G2', 'G#2', 'A2', 'A#2', 'B2', 'C2', 'C#2', 'D2', 'D#2', 'E2', 'F2', 'F#2', 'G3']
        note_map = {}
        for i in range(len(front_notes)):
            for j in range(len(front_notes)):
                note_map[(front_notes[i], front_notes[j])] = abs(i - j)
        self.distance_map = note_map
        self.notes = front_notes
        self.right_mallet = self.notes[len(front_notes) // 2]  # Initialize the right mallet position
        self.left_mallet = self.notes[(len(front_notes) // 2) - 1]  # Initialize the left mallet position
        print("Initial Mallet Positions -> Left: {}, Right: {}".format(self.left_mallet, self.right_mallet))

    def detect_notes(self, audio_path):
        """
        Detect the musical notes from an audio file using pitch tracking.
        This function simplifies the detected notes to ensure consecutive identical notes are collapsed into one.
        
        Parameters:
        - audio_path: Path to the audio file.
        
        Returns:
        - simplified_notes: List of detected notes, simplified.
        """
        y, sr = librosa.load(audio_path)
        pitches, magnitudes = librosa.piptrack(y=y, sr=sr)
        pitch_times = np.argmax(magnitudes, axis=0)
        pitch_freqs = [pitches[pitch_times[i], i] for i in range(pitches.shape[1])]

        threshold = np.median(magnitudes) * 1.5  # Increase threshold to filter out more noise
        pitch_freqs_filtered = [freq for i, freq in enumerate(pitch_freqs) if magnitudes[pitch_times[i], i] > threshold and freq > 0]
            
        notes = [freq_to_note(freq) for freq in pitch_freqs_filtered]
        simplified_notes = [notes[0]]
        for note in notes[1:]:
            if note != simplified_notes[-1]:
                simplified_notes.append(note)
            
        return simplified_notes

    def set_song(self, song):
        """
        Set the current song for the xylophone player. 
        This function also initializes Q-values for the notes in the new song.
        
        Parameters:
        - song: A list of notes representing the song to be learned/played.
        """
        self.current_song = song
        for note in song:
            if note not in self.q_table:
                self.q_table[note] = {'L': 0, 'R': 0}

    def mallet_decision(self, notes):
        """
        Decide which mallet (left or right) to use for each note in the song based on the current positions of the mallets.
        The decision aims to minimize the total movement distance of the mallets over the song.
        
        Parameters:
        - notes: List of notes to be played.
        
        Returns:
        - decisions: List of tuples (note, left mallet position, right mallet position, chosen mallet).
        """
        if len(notes) == 0:
            return []

        # Initialize mallet positions to the first note (or first two different notes if available)
        # left_mallet = right_mallet = notes[0]
        # i = 0
        # while notes[0] == notes[i] and i < len(notes) - 1:
        #     i += 1
        # if len(notes) > 1:
        #     right_mallet = notes[i]
        front_notes = np.array(["G1", "G#1", "A1", "A#1", "B1", "C1", "C#1", "D1", "D#1", "E1", "F1", "G2", "G#2", "A2", "A#2", "B2", "C2", "C#2", "D2", "D#2", "E2", "F2", "F#2", "G3"])
        min_index = len(front_notes)
        max_index = 0
        for note in notes:
            indices = np.where(front_notes == note)[0]
            print(indices)
            if len(indices) > 0:
                if indices[0] < min_index:
                    min_index = indices[0]
                if indices[-1] > max_index:
                    max_index = indices[-1]
        left_mallet = front_notes[min_index]
        right_mallet = front_notes[max_index]

        decisions = []
        for note in notes:
            # Calculate distances from the current note to both mallet positions
            left_distance = self.distance_map.get((left_mallet, note), float('inf'))
            right_distance = self.distance_map.get((right_mallet, note), float('inf'))

            # Decide which mallet to use based on the distance
            if left_distance <= right_distance:
                left_mallet = note
                mallet_used = 'L'
            else:
                right_mallet = note
                mallet_used = 'R'

            decisions.append((note, left_mallet, right_mallet, mallet_used))

        return decisions
    def learn_to_play(self, episodes=1000):
        """
        Learn to play the current song optimally using Q-learning. Adjust the exploration rate over time to balance exploration and exploitation.
        
        Parameters:
        - episodes: Number of episodes to run the learning process.
        """
        epsilon = 0.9  # Initial exploration rate
        min_epsilon = 0.1  # Minimum exploration rate
        epsilon_decay = 0.995  # Decay rate of exploration per episode

        for episode in range(episodes):
            self.left_mallet, self.right_mallet = self.notes[len(self.notes) // 2 - 1], self.notes[len(self.notes) // 2]
            previous_note = None
            for note in self.current_song:
                if random.random() < epsilon:  # Exploration
                    action = random.choice(['L', 'R'])
                else:  # Exploitation
                    action = 'L' if self.q_table[note]['L'] >= self.q_table[note]['R'] else 'R'
                
                reward = self.calculate_reward(note, action, previous_note)
                self.update_q_table(note, action, reward)
                self.perform_action(note, action)
                previous_note = note

            epsilon = max(min_epsilon, epsilon * epsilon_decay)  # Decrease epsilon as learning progresses
    def choose_action(self, note):
        """
        Choose the best action (left or right mallet) for the given note based on Q-values, using an epsilon-greedy strategy.
        
        Parameters:
        - note: The musical note for which the action is to be decided.
        
        Returns:
        - action: The chosen action ('L' for left mallet or 'R' for right mallet).
        """
        if random.random() < 0.2:  # 20% chance to explore randomly
            return random.choice(['L', 'R'])
        else:  # 80% chance to exploit the best known action
            return 'L' if self.q_table[note]['L'] > self.q_table[note]['R'] else 'R'
    
    def perform_action(self, note, action):
        """
        Perform the chosen action by updating the position of the selected mallet to the current note.
        
        Parameters:
        - note: The musical note to be played.
        - action: The chosen action ('L' for left mallet, 'R' for right mallet).
        """
        if action == 'L':
            self.left_mallet = note
        else:
            self.right_mallet = note

    def calculate_reward(self, note, action, previous_note):
        """
        Calculate the reward for taking a particular action based on the distance moved. 
        This includes a bonus for alternating between mallets, which simulates a more human-like playing technique.
        
        Parameters:
        - note: The current musical note.
        - action: The chosen action ('L' or 'R').
        - previous_note: The previous note played (used for determining alternating bonus).
        
        Returns:
        - reward: The calculated reward (negative for movement, positive for staying).
        """
        movement_cost = 0
        if action == 'L':
            movement_cost = abs(self.notes.index(self.left_mallet) - self.notes.index(note))
            if previous_note and self.right_mallet == previous_note:
                movement_cost -= 5  # Reward for alternating mallets
        else:
            movement_cost = abs(self.notes.index(self.right_mallet) - self.notes.index(note))
            if previous_note and self.left_mallet == previous_note:
                movement_cost -= 5  # Reward for alternating mallets

        return -movement_cost  # Negative because we want to minimize movement cost

    def update_q_table(self, note, action, reward):
        """
        Update the Q-table based on the action taken, the reward received, and the potential future rewards.
        
        Parameters:
        - note: The musical note for which the action was taken.
        - action: The action taken ('L' or 'R').
        - reward: The reward received for taking the action.
        """
        learning_rate = 0.1
        discount_factor = 0.95
        next_best_reward = max(self.q_table[note].values())
        self.q_table[note][action] += learning_rate * (reward + discount_factor * next_best_reward - self.q_table[note][action])

    def get_optimal_play(self):
        optimal_play = []
        left_mallet, right_mallet = self.notes[len(self.notes) // 2 - 1], self.notes[len(self.notes) // 2]
        
        for i in range(len(self.current_song)):
            current_note = self.current_song[i]
            chosen_mallet = 'L' if self.q_table[current_note]['L'] >= self.q_table[current_note]['R'] else 'R'
            
            if chosen_mallet == 'L':
                left_mallet = current_note
            else:
                right_mallet = current_note
            
            # Adjust the non-active mallet's position
            non_active_mallet = 'R' if chosen_mallet == 'L' else 'L'
            non_active_mallet_position = right_mallet if non_active_mallet == 'R' else left_mallet
            active_mallet_position = left_mallet if chosen_mallet == 'L' else right_mallet
            
            if i + 1 < len(self.current_song):
                lookahead_notes = self.current_song[i + 1:i + 4]
                best_position = self.proactive_mallet_positioning(active_mallet_position, non_active_mallet_position, lookahead_notes, non_active_mallet)
                
                if non_active_mallet == 'R':
                    right_mallet = best_position
                else:
                    left_mallet = best_position
            
            # Ensure mallets are not on the same note
            if left_mallet == right_mallet:
                if non_active_mallet == 'R':
                    right_mallet = self.adjust_mallet_position(left_mallet, right_mallet)
                else:
                    left_mallet = self.adjust_mallet_position(right_mallet, left_mallet)
            
            optimal_play.append((current_note, chosen_mallet, left_mallet, right_mallet))
        
        return optimal_play

    def adjust_mallet_position(self, active_mallet, non_active_mallet):
        active_index = self.notes.index(active_mallet)
        non_active_index = self.notes.index(non_active_mallet)
        
        # Check if adjustment is possible within the 8-note range
        if non_active_index > 0 and abs((non_active_index - 1) - active_index) <= 8:
            return self.notes[non_active_index - 1]
        elif non_active_index < len(self.notes) - 1 and abs((non_active_index + 1) - active_index) <= 8:
            return self.notes[non_active_index + 1]
        return non_active_mallet  # Return the original if no adjustment is feasible within constraints

    def proactive_mallet_positioning(self, active_mallet_position, non_active_mallet_position, future_notes, non_active_mallet):
        """
        Determine the best position for the non-active mallet given the upcoming notes, while ensuring the mallets
        do not exceed a separation of 8 notes.
        
        Parameters:
        - active_mallet_position: The current position of the active mallet.
        - non_active_mallet_position: The current position of the mallet being optimized.
        - future_notes: A list of future notes to plan for.
        - non_active_mallet: The mallet ('L' or 'R') that is currently non-active.
        
        Returns:
        - best_position: The optimal future position of the mallet, adhering to physical constraints.
        """
        active_index = self.notes.index(active_mallet_position)
        non_active_index = self.notes.index(non_active_mallet_position)
        min_index = max(1, active_index - 8)
        max_index = min(len(self.notes) - 1, active_index + 8)

        possible_positions = self.notes[min_index:max_index + 1]
        distance_costs = {note: 0 for note in possible_positions}
        for note in possible_positions:
            distance_costs[note] = sum(self.distance_map.get((note, future_note), float('inf')) for future_note in future_notes)

        best_position = min(distance_costs, key=distance_costs.get)

        # Adjust if best position is out of the 8-note range
        best_position_index = self.notes.index(best_position)
        if abs(best_position_index - active_index) > 8:
            best_position = self.notes[active_index + 8 if best_position_index > active_index else active_index - 8]

        return best_position

