from PIL import Image

# Point class for contain (x, y) coordination
class Point:
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.position = (x, y)

	def __str__(self):
		return('({}, {})'.format(self.x, self.y))

# return valid pixels in N-8 connection of current point
def n8_connection_points(current_point, max_x, max_y):
	n8_points = []
	for delta_x in range(-1, 2):
		for delta_y in range(-1, 2):
			neighbor_x = current_point.x + delta_x
			neighbor_y = current_point.y + delta_y
			# check if the point is in the image
			x_in_image = (neighbor_x >= 0) and (neighbor_x <= max_x)
			y_in_image = (neighbor_y >= 0) and (neighbor_y <= max_y)
			# check if the point is same as the current point
			not_current_point = (neighbor_x != current_point.x) or (neighbor_y != current_point.y)
			if x_in_image and y_in_image and not_current_point:
				n8_points.append(Point(neighbor_x, neighbor_y))
	return(n8_points)

# region growing
# input:
# 	image = grayscale image object
#	seed_point = Point object of coordinate want to be grew
#	threshold = value used in predicate
# predicate:
#	The different between new pixel' gray value and average gray value of all pixel in region
#	must less than a threshold
# output:
#	2-D list in the same size of input containing the logical value
#	specifying if the pixels in region or not using region growing algorithm
def region_growing(image, seed_point=Point(x=210, y=100), threshold=70):
	col, row = image.size
	region = [[False for i in range(col)] for j in range(row)]	# logical 2-D list for containing pixels in region
	region[seed_point.y][seed_point.x] = True					# add seed point to region
	region_mean = image.getpixel(seed_point.position)[0]		# average gray value of all pixel in region
	pixel_count = 1				# count of all pixel in region
	to_explore = [*n8_connection_points(seed_point, col-1, row-1)]	# list of Points which must be explored
	is_run = True				# run the operation until meet certain conditions
	while is_run:
		new_to_explore = []		# list of Points which must be explored in the next iteration
		pixel_grow_count = 0	# count of pixel grew in this iteration
		# explore the pixels in to_explore list
		for point in to_explore:
			gray_value = image.getpixel(point.position)[0]
			is_in_region = region[point.y][point.x]
			small_than_threshold = abs(gray_value - region_mean) <= threshold
			# if it's not already in region and predicate is correct, add it to the region
			if (not is_in_region) and small_than_threshold:
				region[point.y][point.x] = True		# add point to region
				region_mean = (region_mean*pixel_count+gray_value)/(pixel_count+1)	# re-calculate region mean
				pixel_count += 1					# increase number of pixel in region
				pixel_grow_count += 1				# count the pixel that is added to region
				neighbors = n8_connection_points(point, col-1, row-1)				# calculate its neighbors
				for neighbor in neighbors:	new_to_explore.append(neighbor)			# add its neighbors in explore list
		to_explore = new_to_explore.copy()			# copy the pixels needed to be explored for the next iteration
		if pixel_grow_count == 0: is_run = False	# if there are no new pixel added to the region, stop the algorithm
	return(region)

# color the pixel which is in region
def color_region(image, region, color=(255, 0, 0, 255)):
	col, row = image.size
	pixels = image.load()	# extract pixels value of image
	for x in range(col):
		for y in range(row):
			# if pixel is in region, color it
			if region[y][x] == True:
				pixels[x, y] = color
	return(image)

# mark specific point on the image
def mark_point(image, seed_point):
	col, row = image.size
	pixels = image.load()
	for x in range(col):
		for y in range(row):
			if (x-seed_point.x)**2 + (y-seed_point.y)**2 < 20:
				pixels[x, y] = (255, 0, 0, 255)
	image.show()

im = Image.open('./brain.png')
# finding proper seed point
# mark_point(im, Point(120, 130))
# mark_point(im, Point(350, 200))
region_left = region_growing(im, seed_point=Point(120, 130))
region_right = region_growing(im, seed_point=Point(350, 200))
left_colored_image = color_region(im, region_left)
all_colored_image = color_region(im, region_right)
all_colored_image.show()