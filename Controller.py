
from motion_planning.xylophone_player import XylophonePlayer
from robot.XyloBot import XyloBot
import numpy as np


class XyloController:

    def __init__(self):
        self.bot = XyloBot()
        self.converter = XylophonePlayer()

    def random_song(self, length = 5):
        possible_notes = np.array(["G1", "A1", "B1", "C1", "D1", "E1", "F1", "G2", "A2", "B2", "C2", "D2", "E2", "F2", "G3"])

        song = np.random.choice(possible_notes, length, replace=True)
        print("Notes chosen:", song)
        self.note_list_to_play(song)


    def note_list_to_play(self, note_list, use_learning = False):
        decision = self.converter.mallet_decision(note_list)
        notes = []
        if use_learning:
            self.converter.set_song(note_list)
            self.converter.learn_to_play(episodes=1000)
            decisions = self.converter.get_optimal_play()

            for decision in decisions:
                note, action, left_pos, right_pos = decision
                notes.append((left_pos, right_pos, action == "L"))

        else:
            for n, n1, n2, mallet in decision:
                notes.append((n1, n2, mallet == "L"))


        self.bot.ready()
        self.bot.wait(3)
        self.bot.play_song(notes)
        self.bot.go_home()
        self.bot.shutdown()

    def twinkle_twinkle(self):
        self.note_list_to_play(["C1", "C1", "G2", "G2", "A2", "A2", "G2"])

    def marry_had_a_little_lamb(self):
        self.note_list_to_play(["E1", "D1", "C1", "D1", "E1", "E1", "E1"])