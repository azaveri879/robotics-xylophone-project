import random
import librosa
from utils import freq_to_note
import numpy as np

class XylophonePlayer:
    """Initialize a XylophonePlayer object with empty notes and a Q-table for learning."""
    def __init__(self):
        self.notes = []  # List to store the xylophone notes
        self.setup_notes()  # Setup the notes and their distances
        self.q_table = {}  # Q-table for learning the optimal actions
        self.current_song = []  # Current song (sequence of notes) to be played

    def setup_notes(self):
        """
        Setup the xylophone notes and the distance between each pair of notes.
        This information is used for decision-making in the mallet_decision function.
        """
        front_notes = ['G1', 'A1', 'B1', 'C1', 'D1', 'E1', 'F1', 'G2', 'A2', 'B2', 'C2', 'D2', 'E2', 'F2', 'G3']
        note_map = {}
        for i in range(len(front_notes)):
            for j in range(len(front_notes)):
                note_map[(front_notes[i], front_notes[j])] = abs(i - j)
        self.distance_map = note_map  # Map of note pairs to distances

    def mallet_decision(self, notes):
        """
        Decide which mallet (left or right) to use for each key in the song.
        The decision is based on minimizing the distance the mallets need to move.
        
        Input: 
        - notes: List of notes to be played.
        Output: 
        - decisions: List of tuples indicating the mallet decisions for each note.
        """
        if not notes:
            return []

        # Initialize mallet positions to the first note (or first two different notes if available)
        left_mallet = right_mallet = notes[0]
        if len(notes) > 1 and notes[0] != notes[1]:
            right_mallet = notes[1]

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

            decisions.append((left_mallet, right_mallet, mallet_used))

        return decisions

    def detect_notes(self, audio_path):
        """
        Detect the musical notes from an audio file using pitch tracking.
        This function simplifies the detected notes to ensure consecutive identical notes are collapsed into one.
        
        Input: 
        - audio_path: Path to the audio file.
        Output: 
        - simplified_notes: List of detected notes, simplified.
        """
        y, sr = librosa.load(audio_path)
        pitches, magnitudes = librosa.piptrack(y=y, sr=sr)
        pitch_times = np.argmax(magnitudes, axis=0)
        pitch_freqs = [pitches[pitch_times[i], i] for i in range(pitches.shape[1])]

        pitch_freqs_filtered = [freq if magnitudes[pitch_times[i], i] > np.median(magnitudes) else 0 for i, freq in enumerate(pitch_freqs)]
        notes = [freq_to_note(freq) for freq in pitch_freqs_filtered]

        simplified_notes = [notes[0]]
        for note in notes[1:]:
            if note != simplified_notes[-1]:
                simplified_notes.append(note)
        
        return simplified_notes
    
    def learn_to_play(self, episodes=100, learning_rate=0.1, discount_rate=0.95, exploration_rate=1.0, exploration_decay=0.99, min_exploration_rate=0.01):
        """
        Learn to play the xylophone using a reinforcement learning algorithm.
        This function iterates over episodes, deciding actions based on the current policy and updating the policy based on the received reward.
        
        Input: 
        - episodes: Number of episodes to run the learning algorithm.
        """
        # Initialize Q-table for each note in the current song
        for note in self.current_song:
            self.q_table[note] = {'L': 0, 'R': 0}
        
        for episode in range(episodes):
            state, done = self.get_initial_state()

            while not done:
                # Exploration-exploitation decision
                if random.uniform(0, 1) < exploration_rate:
                    action = random.choice(['L', 'R'])
                else:
                    action = max(self.q_table[state], key=self.q_table[state].get)

                new_state, reward, done = self.take_action(state, action)
                if new_state:
                    self.q_table[state][action] = self.q_table[state][action] + learning_rate * (reward + discount_rate * max(self.q_table[new_state].values()) - self.q_table[state][action])
                state = new_state

            # Decay exploration rate
            exploration_rate = max(min_exploration_rate, exploration_rate * exploration_decay)

    def get_initial_state(self):
        """
        Determine the initial state for an episode of learning. 
        The initial state is the first note of the current song.
        
        Output:
        - The first note of the current song and a flag indicating if the song is empty (done).
        """
        if self.current_song:
            return self.current_song[0], False
        return None, True

    def take_action(self, state, action):
        """
        Simulate taking an action (using a mallet to strike a note) based on the current state.
        This function updates the state, calculates the reward, and checks if the song is finished.
        
        Input: 
        - state: The current state (note).
        - action: The action to take ('L' or 'R' mallet).
        
        Output:
        - The new state, the received reward, and a flag indicating if the episode is done.
        """
        if not self.current_song:
            return None, 0, True

        current_index = self.current_song.index(state)
        next_index = current_index + 1

        if next_index < len(self.current_song):
            new_state = self.current_song[next_index]
            done = False
        else:
            new_state = None
            done = True

        # Simplified reward logic based on action efficiency
        # Reward for choosing the mallet that is closer to the note
        left_distance = self.distance_map.get((state, state), float('inf'))
        right_distance = self.distance_map.get((state, state), float('inf'))

        if action == 'L':
            reward = 1 if left_distance <= right_distance else -1
        else:
            reward = 1 if right_distance <= left_distance else -1

        return new_state, reward, done

    def set_song(self, song):
        """
        Set the current song for the xylophone player. 
        This function also initializes Q-values for the notes in the new song.
        
        Input: 
        - song: A list of notes representing the song to be learned/played.
        """
        self.current_song = song
        for note in song:
            if note not in self.q_table:
                self.q_table[note] = {'L': 0, 'R': 0}

    def get_optimal_play(self):
        """
        Determine the optimal sequence of mallet usage for playing the current song,
        based on the learned Q-values.
        
        Output:
        - optimal_actions: A list of tuples, where each tuple contains the note and the optimal
          mallet ('L' or 'R') to use for that note, according to the learned policy.
        """
        optimal_actions = []
        for note in self.current_song:
            # Determine the best action for this note based on the highest Q-value
            if note in self.q_table:
                best_action = max(self.q_table[note], key=self.q_table[note].get)
                optimal_actions.append((note, best_action))
            else:
                # If the note wasn't encountered during learning, default to a heuristic or random choice
                optimal_actions.append((note, random.choice(['L', 'R'])))
        
        return optimal_actions