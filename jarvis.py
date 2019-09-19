import cv2
import numpy as np 
import random


image_height = 200
image_width  = 200
padding = 20

image = np.zeros((image_height,image_width,3))


def draw_points(im, points):

	img = im.copy()

	for i in range(len(points)):

		img[points[i][1], points[i][0]] = 255

	return img



def orientation_length(p,q,r):

	p = np.asarray(p, dtype='int32')
	q = np.asarray(q, dtype='int32')
	r = np.asarray(r, dtype='int32')

	vector_1 = q - p
	vector_2 = r - p

	length_1 = np.linalg.norm(vector_1)
	length_2 = np.linalg.norm(vector_2)

	cross_product = np.cross(vector_1,vector_2)

	return (cross_product, length_1, length_2)


def draw_temp_line(im, points1, points2, permanent=255):

	img = im.copy()

	cv2.line(img, (points1[0], points1[1]),
				  (points2[0], points2[1]), (255,255,permanent), 1)

	return img


def jarvis_march(points, animation=False):

	leftmost_point = min(points, key = lambda x:x[0])

	leftmost_point_index = points.index(leftmost_point)

	p = leftmost_point_index

	hull_list = []
	hull_list.append(points[p])

	num_of_points = len(points)

	if animation:

		img = draw_points(image, points)

	img_index = 0
	while True:

		q = (p + 1) % num_of_points

		for r in range(num_of_points):

			if animation:

				img_temp = draw_temp_line(img, points[p], points[q])
				img_temp = draw_temp_line(img_temp, points[p], points[r], 0)
				cv2.imshow('img_temp', img_temp)
				cv2.waitKey(50)
				cv2.imwrite('images/'+str(img_index)+'.jpg', img_temp)
				img_index += 1

			if r == p:
				continue

			orientation, length_1, length_2 = orientation_length(points[p], points[q], points[r])

			if orientation > 0 or (orientation == 0 and length_2 > length_1):

				q = r 

		if animation:
			img = draw_temp_line(img, points[p], points[q])
		
		p = q

		if p == leftmost_point_index:
			break

		hull_list.append(points[q])

	return hull_list


def gen_points(num):

	points = []

	for i in range(num):

		points.append([random.randint(padding,image_height-padding), random.randint(padding,image_width-padding)])

	return points




def draw_lines(im, points):

	img = im.copy()

	for i in range(len(points)):

		next_index = (i+1)%len(points)

		cv2.line(img, (points[i][0], points[i][1]),
					 (points[next_index][0], points[next_index][1]),
					 (255,255,255),1)

	return img



points = gen_points(10)
hull_list = jarvis_march(points, True)


