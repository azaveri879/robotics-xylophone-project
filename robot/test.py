from XyloBot import XyloBot

def main():
	notes = ["G", "A", "B", "C", "D"]
	m = {}
	for i, note in enumerate(notes):
		m[note] = (0.028 + 0.03*i, 0.45)
		
	left_mallet = (-0.02, 0.2)
	right_mallet = (0.02, 0.2)

	xylo = XyloBot()
	xylo.bot.gripper.release()
	# pos = xylo.find_ee_loc(m["C"], right_mallet)
	# xylo.go_to(x=pos[0], y=pos[1], z=0.15, left=False)
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
	xylo.play_song([("C", False), ("C", False), ("G", True), ("G", True), ("A", False), ("A", False), ("G", True), ("F", True)])
	xylo.go_home()
	xylo.shutdown()

if __name__ == '__main__':
	main()