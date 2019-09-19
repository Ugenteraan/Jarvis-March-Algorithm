import argparse
import sys


defaults = {	
	'num_of_points' : 30,
	'visualize'     : False,
	'save'          : False,
	'img_height'    : 200,
	'img_width'     : 200,
	'padding'       : 30
}

parser = argparse.ArgumentParser()

parser.add_argument('--num_of_points', default=defaults['num_of_points'], type=int, help="Define the number of points to be generated.")
parser.add_argument('--visualize', action='store_true', default=defaults['visualize'], help="If you want to visualize the working of the algorithm")
parser.add_argument('--save', action='store_true', default=defaults['save'], help='If you want to save the end result as an image.')
parser.add_argument('--height', default=defaults['img_height'], type=int, help='Define the image height')
parser.add_argument('--width', default=defaults['img_width'], type=int, help='Define the image width.')
parser.add_argument('--padding', default=defaults['padding'], type=int, 
				help='Define the padding size. Padding is used to make sure the points generated are not too close to the image boundary.')


args = parser.parse_args()

assert args.num_of_points > 3, "Number of points must be more than 3 !"
assert args.height >= 20, "Image height must be at least 20!"
assert args.width >= 20, "Image width must be at least 20!"
assert args.padding*2 <= args.width or args.padding*2 <= args.height, "Padding size cannot exceed half of the width nor height of the image!"

