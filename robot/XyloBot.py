import time
import math

from interbotix_xs_modules.xs_robot.arm import InterbotixManipulatorXS
import numpy as np
from typing import Any, List, Tuple, Union

def deg(rads):
	return rads * 360 / (2 * np.pi)

def rads(degs):
	return degs * (2 * np.pi) / 360

class XyloBot():

	def __init__(self):
		self.bot = InterbotixManipulatorXS(
			robot_model='px150',
			group_name='arm',
			gripper_name='gripper'
		)
		self.last_wrist_pos = 0
		
		self.m = {}
		notes = ["G", "A", "B", "C", "D", "E", "F"]
		for i, note in enumerate(notes):
			self.m[note] = (0.028 + 0.032*i, 0.45)
			
		self.left_mallet = (-0.02, 0.2)
		self.right_mallet = (0.02, 0.2)

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
        z: float = 0, left: bool = True):

		thetas, success = self.find_ee_pose(x=x, y=y, z=z)
		if not success:
			print("Couldn't find pose")
			return False
		thetas[3] -= 0.2
		self.last_wrist_pos = thetas[3]
		
		thetas[4] = -0.22 if left else 0.22
		
		return self.bot.arm.set_joint_positions(thetas, moving_time=1.0)

	def hit(self):
		self.bot.arm.set_single_joint_position("wrist_angle", self.last_wrist_pos + 0.25, moving_time=1.0)
		self.bot.arm.set_single_joint_position("wrist_angle", self.last_wrist_pos, moving_time=1.0)
	
	def wait(self, secs):
		time.sleep(secs)
		
	def play_song(self, notes):
		for n, left in notes:
			mallet = self.left_mallet if left else self.right_mallet
			pos = self.find_ee_loc(self.m[n], mallet)
			self.go_to(x=pos[0], y=pos[1], z=0.15, left=left)
			self.hit()

	def go_home(self):
		self.bot.arm.set_joint_positions([rads(90), rads(-105), 1.55, rads(20), 0.0], moving_time=1.0)

	def shutdown(self):
		self.bot.shutdown()