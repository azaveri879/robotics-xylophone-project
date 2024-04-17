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

def data():
	d = np.array([[1.5707963267948966, 0.041, 0.076], [1.3137166941154068, 0.046, 0.073], [1.056637061435917, 0.091, 0.068], [0.7995574287564274, 0.137, 0.063], [0.5424777960769378, 0.18, 0.058], [0.28539816339744817, 0.23, 0.05], [0.028318530717958534, 0.26, 0.043], [-0.2287611019615311, 0.029, 0.034], [-0.48584073464102073, 0.31, 0.031], [-0.7429203673205104, 0.32, 0.027], [-1.0, 0.33, 0.025]])
	return d[:, 0], d[:, 1], d[:, 2]

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
		
	cos_C = (b**2 + a**2 - c**2) / (2 * b * a)
	C = math.acos(cos_C)
	print("Angle a: ", deg(C))
	return C

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
def find_x_mallet(lx):
	return (lx/2)
	
def calculate_mallet_cords(lx):
	l1 = 0.029
	l2 = .17186
	gap = 0.05
	
	angles, m_distances, _ = data()
	rad_to_use = np.interp(lx, m_distances, angles)

	angle_a = law_of_cosines_angle(l2,l2, lx - gap)
	angle_b = rads(120) - angle_a
 
	mx = find_x_mallet(lx)
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
			self.m[note] = (-0.17 + 0.03*i, 0.44)
			
		notes = ["E1", "F1", "G2", "A2", "B2"]
		for i, note in enumerate(notes):
			self.m[note] = (-0.031 + 0.03*i, 0.44)
			
		notes = ["C2", "D2", "E2", "F2", "G3"]
		for i, note in enumerate(notes):
			self.m[note] = (0.105 + 0.03*i, 0.44)
			
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
		print(thetas)
		
		return self.bot.arm.set_joint_positions(thetas, moving_time=0.7)
	
	def get_wrist_rotation(self):
		goal_height_difference = 0.01
		radius = self.mallet_distance / 2
		return math.atan(goal_height_difference/radius)
	
	def find_and_set_mallet_location(self, execute=True):
		mx, my, rads = calculate_mallet_cords(self.mallet_distance)
		
		if execute:
			self.set_gripper_angle(rads)
		
        # Adjust for wrist rotation
		rotation = self.get_wrist_rotation()
		x_pos = (mx)*math.cos(rotation)
		
		if self.left:
			return (-x_pos, my)
		else:
			return (x_pos, my)
        

	def hit(self):
		self.bot.arm.set_single_joint_position("wrist_angle", self.last_wrist_pos + 0.27, moving_time=0.7)
		self.bot.arm.set_single_joint_position("wrist_angle", self.last_wrist_pos, moving_time=0.7)
	
	def wait(self, secs):
		time.sleep(secs)
		
	def play_song(self, notes):
		for n1, n2, left in notes:
			self.left = left
			note = n1 if left else n2
			
            # Check if mallet distance changed
			mallet_distance = self.get_distance(n1, n2)
			execute = mallet_distance != self.mallet_distance
			self.mallet_distance = mallet_distance
			
			mallet_location = self.find_and_set_mallet_location(execute=execute)
			
			ee_loc = self.find_ee_loc(self.m[note], mallet_location)
			self.go_to(x=ee_loc[0], y=ee_loc[1], z=0.15)
			self.hit()
			
	def get_distance(self, n1, n2):
		print("Calculated distance", np.abs(self.m[n1][0] - self.m[n2][0]))
		return np.abs(self.m[n1][0] - self.m[n2][0])
			
	def set_gripper_angle(self, angle):
		self.bot.core.robot_set_operating_modes(cmd_type='single', name='gripper', mode='position')
		self.wait(0.2)
		self.bot.core.robot_write_joint_command(joint_name="gripper", command=np.pi/2)
		self.wait(0.4)
		self.bot.core.robot_write_joint_command(joint_name="gripper", command=angle)
		self.wait(0.4)
		self.bot.core.robot_set_operating_modes(cmd_type='single', name='gripper', mode='pwm')

	def go_home(self):
		self.bot.arm.set_joint_positions([rads(90), rads(-105), 1.55, rads(20), 0.0], moving_time=0.7)
		
	def ready(self):
		self.bot.arm.set_joint_positions([ 1.63049627, -0.33121526,  1.18114171, -1.5, -0.1814677 ], moving_time=0.7)

	def shutdown(self):
		self.bot.shutdown()

	if __name__ == '__main__':
		main()
