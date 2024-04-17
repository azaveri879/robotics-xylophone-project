
from motion_planning.xylophone_player import XylophonePlayer
from robot.XyloBot import XyloBot


class XyloController:

    def __init__(self):
        self.bot = XyloBot()
        self.converter = XylophonePlayer()

    def note_list_to_play(self, note_list, use_learning = False):
        decision = self.converter.mallet_decision(note_list)

        notes = []
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