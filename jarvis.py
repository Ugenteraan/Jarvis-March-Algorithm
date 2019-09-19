import cv2
import numpy as np 
import random
import cfg

args = cfg.args


image_height = args.height
image_width  = args.width
padding = args.padding

image = np.zeros((image_height,image_width,3))


def draw_points(im, points):
	'''
	To draw the generated points on the image
	'''

	#make a copy so the original image is not altered
	img = im.copy()

	for i in range(len(points)):
		#access by row, column
		img[points[i][1], points[i][0]] = 255

	return img



def orientation_length(p,q,r):
	'''
	To determine the orientation of the vectors and the length of the vectors. Vectors are (q-p) and (r-p)
	'''

	#convert lists into np arrays
	p = np.asarray(p, dtype='int32')
	q = np.asarray(q, dtype='int32')
	r = np.asarray(r, dtype='int32')

	vector_1 = q - p
	vector_2 = r - p

	#calculate the length of the vectors
	length_1 = np.linalg.norm(vector_1)
	length_2 = np.linalg.norm(vector_2)

	cross_product = np.cross(vector_1,vector_2)

	return (cross_product, length_1, length_2)


def draw_temp_line(im, points1, points2, red_colour=255):
	'''
	To draw the temporary lines during the visualization process
	'''

	img = im.copy()

	#plot the lines
	cv2.line(img, (points1[0], points1[1]),
				  (points2[0], points2[1]), (255,255,red_colour), 1)

	return img


def jarvis_march(points, animation=False):
	'''
	To generate the convex polygon using Jarvis March algorithm
	'''

	#get the leftmost point based on the x values
	leftmost_point = min(points, key = lambda x:x[0])

	#index of that leftmost point
	leftmost_point_index = points.index(leftmost_point)

	p = leftmost_point_index

	hull_list = []
	#append the leftmost point as it is surely one of the points in the convex polygon
	hull_list.append(points[p])

	num_of_points = len(points)

	#plot the points on the image
	if animation:

		img = draw_points(image, points)

	while True:

		#initialize a point to start the comparing process
		q = (p + 1) % num_of_points

		#iterate through all points
		for r in range(num_of_points):

			#skip the current loop if r == p
			if r == p:
				continue

			#draw the temporary lines during the process
			if animation:

				img_temp = draw_temp_line(img, points[p], points[q])
				img_temp = draw_temp_line(img_temp, points[p], points[r], 0)
				cv2.imshow('img_temp', img_temp)
				cv2.waitKey(50)


			orientation, length_1, length_2 = orientation_length(points[p], points[q], points[r])

			#if orientation is more than 0, that means it is an anticlockwise rotation
			#if orientation is 0, the vectors are colinear, hence we choose the largest length vector
			if orientation > 0 or (orientation == 0 and length_2 > length_1):

				q = r 

		if animation:
			img = draw_temp_line(img, points[p], points[q])
		
		#declare a new p
		p = q

		#break the loop if the starting point has been reached
		if p == leftmost_point_index:
			break

		hull_list.append(points[q])

	return hull_list


def gen_points(num):
	'''
	Randomly generate num points
	'''

	points = []

	for i in range(num):
		#generate within the range of the padded values
		points.append([random.randint(padding,image_height-padding), random.randint(padding,image_width-padding)])

	return points




def draw_lines(im, points):
	'''	
	draw the lines on the image as per the hull_list generated from the algo.
	'''

	img = im.copy()

	for i in range(len(points)):

		#the next_index cannot be more than the number of points
		next_index = (i+1)%len(points)

		cv2.line(img, (points[i][0], points[i][1]),
					 (points[next_index][0], points[next_index][1]),
					 (255,255,255),1)

	return img




if __name__ == '__main__':

	points = gen_points(args.num_of_points)
	hull_list = jarvis_march(points, args.visualize)

	if args.save:
		#save the final image
		img = draw_lines(image, hull_list)
		cv2.imwrite('result.jpg', img)