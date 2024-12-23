import sys
import os

# Add the parent directory to sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from function.flabelme2mask import lme2mask

input_folder =  "./init-test/labelme/"
output_folder = "./default_data/dataset_masks/dataset_0000/"

if __name__ == '__main__':
    lme2mask(input_folder, output_folder)