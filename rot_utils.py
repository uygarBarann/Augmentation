import os
import numpy as np
from PIL import Image

#Shoelace formula to calculate the polygon area 
def polygon_area(polygon):
    n = len(polygon)
    area = 0
    for i in range(n):
        j = (i + 1) % n
        area += polygon[i][0] * polygon[j][1]
        area -= polygon[j][0] * polygon[i][1]

    #If vertices is not in the counterclockwise order area will be negative, so take abs of it
    return abs(area) / 2.0


#Finds the polygon with the biggest area inside the list of polygons
def find_biggest_area(polygons):
    index_count = -1
    max_index = -1
    max_area = -1
    for label, polygon in polygons:
        index_count = index_count + 1
        np_points = np.array(polygon)
        curr_area = polygon_area(np_points)
        
        if curr_area > max_area:
            max_area = curr_area
            max_index = index_count
    return max_index


#Saves the image to the output folder
def save_image(output_folder, image_path, rotated_image, count):
    full_filename = os.path.basename(image_path)
    image_name = os.path.splitext(full_filename)[0]
    save = os.path.join(output_folder, image_name + "_rotated" + str(count)+ ".jpg")
    rotated_image.save(save)


#Converts a list of normalized polygons to "unnormalized" polygons
def convert_normal_to_original(polygons, original_width, original_height):
    unnormalized_polygons = []
    for label, polygon in polygons:
        polygon_tmp = np.array(polygon)
        unnormalized_x = polygon_tmp[:, 0] * original_width
        unnormalized_y = polygon_tmp[:, 1] * original_height

        unnormalized_polygon = np.stack((unnormalized_x, unnormalized_y), axis=-1)
        unnormalized_polygons.append((label, unnormalized_polygon))

    return unnormalized_polygons


#Converts a list of "unnormalized" polygons to normalized polygons
def convert_original_to_normal(polygons, original_width, original_height):
    normalized_polygons = []
    for label, polygon in polygons:
        normalized_x = polygon[:, 0] / original_width
        normalized_y = polygon[:, 1] / original_height
        
        normalized_polygon = np.stack((normalized_x, normalized_y), axis=-1)
        normalized_polygons.append((label, normalized_polygon))

    return normalized_polygons


#Rotates the image by given degrees counterclockwise :p
def rotate_image(image_path, degrees):
    img = Image.open(image_path)
    return img.rotate(degrees, expand=False)


#Rotates the polygon by given angle around the center point counterclockwise 
def rotate_polygon(polygon, radian, center):
    ox, oy = center

    polygon_x = polygon[:, 0]
    polygon_y = polygon[:, 1]

    rotated_x = ox + (polygon_x - ox) * np.cos(radian) - (polygon_y - oy) * np.sin(radian)
    rotated_y = oy + (polygon_x - ox) * np.sin(radian) + (polygon_y - oy) * np.cos(radian)

    rotated_polygon = np.stack((rotated_x, rotated_y), axis=-1)

    return rotated_polygon


#Rotates the polygons by given angle around the center point counterclockwise
def rotate_polygons(polygons, degrees, center):
    radians = np.radians(degrees)

    rotated_polygons = []
    for label, polygon in polygons:
        rotated_polygon = rotate_polygon(polygon, radians, center)

        rotated_polygons.append((label, rotated_polygon))

    return rotated_polygons