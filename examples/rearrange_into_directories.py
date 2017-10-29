import os 
import shutil

meta_dir = '/home/ratneshm/projects/motion_planning_datasets'
import cv2
import os
from pprint import pprint

# ref: http://norvig.com/python-iaq.html
class Planning_environment:
    "A structure that can have any fields defined."
    def __init__(self, **entries): self.__dict__.update(entries)

class Planning_dataset():
	"""docstring for Planning_dataset"""
	def __init__(self):
		# path to Mohak n Sanjiban's dataset. todo make arg
		self.meta_dir = '/home/ratneshm/projects/motion_planning_datasets'

		# list of immediate subdirectories, which categorize the various types
		env_types = [subdir for subdir in os.listdir(self.meta_dir) 
							if os.path.isdir(os.path.join(self.meta_dir, subdir))]
		# remove the .git folder from the list
		env_types = [subdir for subdir in env_types
							if not subdir=='.git']


		self.environments = []

		for env_type in env_types:
			train_dir = os.path.join(self.meta_dir, env_type, 'train')
			test_dir = os.path.join(self.meta_dir, env_type, 'test')
			validation_dir = os.path.join(self.meta_dir, env_type, 'validation')
			current_env_struct = Planning_environment(name=env_type, 
								train_dir=train_dir,
								test_dir=test_dir,
								validation_dir=validation_dir)

			self.environments.append(current_env_struct)

def image_to_folder(folder):
	files = os.listdir(folder)
	for orig_file in files:
		subdir_name = orig_file.split('.')[0]
		os.makedirs(os.path.join(folder, subdir_name))
		os.rename(os.path.join(folder, orig_file), os.path.join(folder, subdir_name, 'map.png'))  

def main():
	dataset = Planning_dataset()
	envs = dataset.environments
	for env in envs:
		print env.name
		image_to_folder(env.train_dir)
		image_to_folder(env.test_dir)
		image_to_folder(env.validation_dir)
		# pprint([env.name, env.train_dir, env.test_dir, env.validation_dir])


if __name__ == '__main__':
	main()
