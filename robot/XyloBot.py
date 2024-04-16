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

	def find_ee_pose(
        self,
        x: float = 0,
        y: float = 0,
        z: float = 0
    ) -> Tuple[Union[np.ndarray, Any, List[float]], bool]:
		return self.bot.arm.set_ee_pose_components(x=x, y=y, z=z, pitch=-0.2, execute=False)
	
	def find_ee_loc(self, note_location: Tuple[float, float], mallet_location_ee: Tuple[float, float]):
		mallet_length = math.sqrt(mallet_location_ee[0]**2 + mallet_location_ee[1]**2)
		print("lm", mallet_length)
		note_length = math.sqrt(note_location[0]**2 + note_location[1]**2)
		print("ln", note_length)


		note_angle = math.atan(note_location[1]/note_location[0])
		print("theta_1", deg(note_angle))
		mallet_angle = np.pi/2 + np.abs(math.atan(mallet_location_ee[1]/mallet_location_ee[0]))
		print("theta_2", deg(mallet_angle))
		bottom_angle = math.asin(math.sin(mallet_angle)*mallet_length/note_length)
		print("theta_4", deg(bottom_angle))

		if mallet_location_ee[0]*note_location[0] > 0: # Both are negative or positive
			arm_angle = (np.abs(note_angle) - bottom_angle)*note_angle/np.abs(note_angle)
		else:
			arm_angle = (np.abs(note_angle) + bottom_angle)*note_angle/np.abs(note_angle)

		print("theta_3", deg(arm_angle))

		arm_length = math.sqrt(mallet_length**2 + note_length**2 - 2*mallet_length*note_length*math.cos(np.abs(arm_angle)))
		print("la", arm_length)
		return (math.sin(arm_angle)*arm_length, math.cos(arm_angle)*arm_length)
	
	def go_to(self,
        x: float = 0,
        y: float = 0,
        z: float = 0):

		thetas, success = self.find_ee_pose(x=x, y=y, z=z)
		if not success:
			print("Couldn't find pose")
			return False
		return self.bot.arm.set_joint_positions(thetas, moving_time=3.0)
	
	def wait(self, secs):
		time.sleep(secs)

	def go_home(self):
		self.bot.arm.set_joint_positions([rads(90), rads(-105), 1.55, rads(20), 0.0], moving_time=3.0)

	def shutdown(self):
		self.bot.shutdown()