import time
import math

from interbotix_xs_modules.xs_robot.arm import InterbotixManipulatorXS
import numpy as np
from typing import Any, List, Tuple, Union

def main():
	#testing
	lx = 0.00001
	calculate_mallet_cords(lx)
	print("")
	pass
def deg(rads):
	return rads * 360 / (2 * np.pi)

def rads(degs):
	return degs * (2 * np.pi) / 360

def law_of_cosines(b, c, A_radians): 
	# Used to find distance between our gripper carriages
	# b and c are the length of gripper carriages towards the mallet
	# A is 120 - the angle between grippers (Calculated below in calculate_angle_A)
	# Calculates a using the formula a = sqrt(b^2 + c^2 - 2bc*cos(A)).

	a_squared = (b**2 + c**2) - 2 * b * c * math.cos(A_radians)
	a = math.sqrt(a_squared)  # Take the square root of a_squared to find a
	print("x: ", a)
	return a
	
def law_of_cosines_angle(a, b, c): 
	# Used to find angle between mallets given c is the desired length between
	# a and b are length of mallets
	# Note the length between should be distance from note1 to note2 - .025
	# Calculates angle A in degrees using the Law of Cosines.
		
	cos_A = (b**2 + a**2 - c**2) / (2 * b * a)
	A = math.acos(cos_A)
	print("Angle a: ", deg(A))
	return A	

def line_rad_to_x(x):

	m = ((math.pi / 2) + 1) / 0.05
	b = -1 
	print("rad: ", m*x + b)
	return m * x + b
	
# following functions are finding the x and y of mallets given the origin is the middle
# of gripper cartridge rail
def find_y_mallet(l1, l2, a, b): # given the preset l1 and l2. l2 is length of mallet.
	# l1 is length of carriage base to mallet base
	# a is angle between mallets
	# b is 120 degree minus angle a
	yb = l1 * math.cos(b/2)
	ya = l2 * math.cos(a/2)
	return ya + yb
# left_mallet is whether it is left, false if right mallet
# lx is desired distance between mallets with the 0.025 offset taken out
def find_x_mallet(left_mallet, lx):
	if left_mallet:
		return -1 * ((lx/2) + (0.025 / 2))
	else:
		return (lx/2) + (0.025/2)

def calculate_mallet_cords(lx):
	# lx is distance between notes - 0.025
	l1 = 0.029
	l2 = .17186

	angle_a = law_of_cosines_angle(l2,l2, lx)
	angle_b = rads(120) - angle_a

	x = law_of_cosines(l1,l1,angle_b) # desired length between carriages

	# our limits
	if x > .05:
		x = 0.05
	if x < 0:
		x = 0

	rad_to_use = line_rad_to_x(x)

	# find x and y of mallet cords
 
	# for right mallet
 
	mx = find_x_mallet(False, lx)
	my = find_y_mallet(l1,l2,angle_a, angle_b)

	print("Y cord: ", my)
	print("X coord:, ", mx)

	return mx, my, rad_to_use

class XyloBot():

	def __init__(self):
		self.bot = InterbotixManipulatorXS(
			robot_model='px150',
			group_name='arm',
			gripper_name='gripper'
		)
		self.last_wrist_pos = 0
		
		self.m = {}
		
		notes = ["G1", "A1", "B1", "C1", "D1"]
		for i, note in enumerate(notes):
			self.m[note] = (-0.17 + 0.03*i, 0.45)
			
		notes = ["E1", "F1", "G2", "A2", "B2"]
		for i, note in enumerate(notes):
			self.m[note] = (-0.031 + 0.03*i, 0.45)
			
		notes = ["C2", "D2", "E2", "F2", "G3"]
		for i, note in enumerate(notes):
			self.m[note] = (0.105 + 0.03*i, 0.45)
			
		self.left_mallet = (-0.068, 0.2)
		self.right_mallet = (0.068, 0.2)
		self.mallet_distance = 0
		self.left = True

	def find_ee_pose(
        self,
        x: float = 0,
        y: float = 0,
        z: float = 0
    ) -> Tuple[Union[np.ndarray, Any, List[float]], bool]:
		return self.bot.arm.set_ee_pose_components(x=x, y=y, z=z, pitch=0, execute=False)
	
	def find_ee_loc(self, note_location: Tuple[float, float], mallet_location_ee: Tuple[float, float]):
		
        # Find the length of the mallet and the note
		mallet_length = math.sqrt(mallet_location_ee[0]**2 + mallet_location_ee[1]**2)
		# print("mallet_length", mallet_length)
		note_length = math.sqrt(note_location[0]**2 + note_location[1]**2)
		# print("note_length", note_length)


        # Find the angles of the mallets and notes
		note_angle = math.atan(note_location[0]/note_location[1])
		# print("note_angle", deg(note_angle))
		mallet_angle = np.pi/2 + np.abs(math.atan(mallet_location_ee[1]/mallet_location_ee[0]))
		# print("mallet_angle", deg(mallet_angle))
		bottom_angle = math.asin(math.sin(mallet_angle)*mallet_length/note_length)
		# print("bottom_angle", deg(bottom_angle))

        # Find angle of the arm
		if mallet_location_ee[0]*note_location[0] > 0: # Both are negative or positive
			# print("Using same side")
			arm_angle = (np.abs(note_angle) - bottom_angle)*note_angle/np.abs(note_angle)
		else:
			# print("Using left and right")
			arm_angle = (np.abs(note_angle) + bottom_angle)*note_angle/np.abs(note_angle)
		# print("arm_angle", deg(arm_angle))
		
        # Find final angle in triangle
		last_triangle_angle = np.pi - bottom_angle - mallet_angle
		# print("last_triangle_angle", deg(last_triangle_angle))

        # Find arm length and final ee position
		arm_length = math.sqrt(mallet_length**2 + note_length**2 - 2*mallet_length*note_length*math.cos(np.abs(last_triangle_angle)))
		# print("arm_length", arm_length)
		return (math.sin(arm_angle)*arm_length, math.cos(arm_angle)*arm_length)
	
	def go_to(self,
        x: float = 0,
        y: float = 0,
        z: float = 0):

		thetas, success = self.find_ee_pose(x=x, y=y, z=z)
		if not success:
			print("Couldn't find pose")
			return False
		thetas[3] -= 0.2
		self.last_wrist_pos = thetas[3]
		
		rotation = self.get_wrist_rotation()
		thetas[4] = -rotation if self.left else rotation
		
		return self.bot.arm.set_joint_positions(thetas, moving_time=1.0)
	
	def get_wrist_rotation(self):
		goal_height_difference = 0.025
		radius = self.mallet_distance / 2
		return math.atan(goal_height_difference/radius)
	
	def find_mallet_location(self):
		mallet = self.left_mallet if self.left else self.right_mallet
		rotation = self.get_wrist_rotation()
		print(rotation)
		print(self.mallet_distance)
		x_pos = (self.mallet_distance/2)*math.cos(rotation)
		print(x_pos)
		if self.left:
			return (-x_pos, mallet[1])
		else:
			return (x_pos, mallet[1])
        

	def hit(self):
		self.bot.arm.set_single_joint_position("wrist_angle", self.last_wrist_pos + 0.25, moving_time=1.0)
		self.bot.arm.set_single_joint_position("wrist_angle", self.last_wrist_pos, moving_time=1.0)
	
	def wait(self, secs):
		time.sleep(secs)
		
	def play_song(self, notes):
		for n, left in notes:
			self.left = left
			self.mallet_distance = 0.136
			mallet_location = self.find_mallet_location()
			ee_loc = self.find_ee_loc(self.m[n], mallet_location)
			self.go_to(x=ee_loc[0], y=ee_loc[1], z=0.15)
			self.hit()
			
	def gripper_to_distance(self, angle):
		self.bot.core.robot_set_operating_modes(cmd_type='single', name='gripper', mode='position')
		self.wait(0.5)
		self.bot.core.robot_write_joint_command(joint_name="gripper", command=angle)
		self.wait(0.5)
		self.bot.core.robot_set_operating_modes(cmd_type='single', name='gripper', mode='pwm')

	def go_home(self):
		self.bot.arm.set_joint_positions([rads(90), rads(-105), 1.55, rads(20), 0.0], moving_time=1.0)

	def shutdown(self):
		self.bot.shutdown()

	if __name__ == '__main__':
		main()
