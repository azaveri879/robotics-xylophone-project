from XyloBot import XyloBot
import numpy as np

def main():
	notes = ["G", "A", "B", "C", "D"]
	m = {}
	for i, note in enumerate(notes):
		m[note] = (0.028 + 0.03*i, 0.45)
		
	left_mallet = (-0.02, 0.2)
	right_mallet = (0.02, 0.2)

	xylo = XyloBot()
	# pos = xylo.find_ee_loc(m["C"], right_mallet)
	# xylo.go_to(x=pos[0], y=pos[1], z=0.15, left=True)
	# xylo.hit()
	# xylo.hit()
	# # xylo.wait(3)
	# pos = xylo.find_ee_loc(m["G"], left_mallet)
	# xylo.go_to(x=pos[0], y=pos[1], z=0.15)
	# xylo.hit()
	# xylo.hit()
	# # xylo.wait(3)
	# pos = xylo.find_ee_loc(m["A"], left_mallet)
	# xylo.go_to(x=pos[0], y=pos[1], z=0.15)
	# xylo.hit()
	# xylo.hit()
	# pos = xylo.find_ee_loc(m["G"], left_mallet)
	# xylo.go_to(x=pos[0], y=pos[1], z=0.15)
	# xylo.hit()
	xylo.gripper_to_distance(np.pi/4)
	xylo.wait(1)
	# xylo.play_song([("G1", True), ("A1", True), ("B1", True), ("C1", True), ("D1", True), ("E1", True), ("F1", True), ("G2", True), ("A2", True), ("B2", True), ("C2", True), ("D2", True), ("E2", True), ("F2", True), ("G3", True)])
	xylo.play_song([("C1", True), ("D1", True), ("E1", False)])
	xylo.go_home()
	# xylo.gripper_to_distance(0.0)
	# xylo.wait(1)
	# xylo.gripper_to_distance(np.pi/2)
	xylo.shutdown()

if __name__ == '__main__':
	main()