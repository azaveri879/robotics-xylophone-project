from robot.XyloBot import XyloBot


def main():
	xylo = XyloBot()

	# print(xylo.bot.arm.get_ee_pose())
	# xylo.go_to(x=0.05, y=0.22647966, z=0.15)
	# xylo.bot.gripper.grasp()
	# xylo.bot.gripper.release()
	# xylo.wait(1)
	# xylo.go_home()
	print(xylo.find_ee_loc((-3, 3), (1, 1)))
	xylo.shutdown()

if __name__ == '__main__':
	main()