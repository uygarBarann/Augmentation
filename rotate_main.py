import numpy as np
from PIL import Image
from rot_utils import *
from adjust import *

#Polygons is in the format [ (id1, [(x1, y1), ..., (xn, yn)]), (id2, [(x1, y1), ..., (xn, yn)]) ]
def rotation(img_path, polygons_orig, output_folder, max_number, min_percentage):
    degrees_cons = [90,180,270,45,135,225,315,30,60,120,150,210,240,300,330]

    degrees = []
    for i in degrees_cons:
        degrees.append(int(np.random.uniform(i-10, i+10)))
    
    image = Image.open(img_path)
    original_width, original_height = image.size

    center = (original_width / 2 , original_height / 2)

    #Converts polygon information to array type
    polygons = convert_normal_to_original(polygons_orig, original_width, original_height)

    max_area_scratch_index = find_biggest_area(polygons)
    base_polygon = polygons[max_area_scratch_index][1]
    
    area = polygon_area(base_polygon)

    min_ratio = min_percentage / 100
    rotate_count = 0 
    rotated_list = []
    for degree in degrees:
        if ((degree % 180) == 0):
            adjusted_base_polygon = adjust_polygons_tmp([(-1, base_polygon)], original_width, original_height)[0][1]
        elif ((degree % 90) == 0):
            adjusted_base_polygon = adjust_polygons_tmp([(-1, base_polygon)], original_height, original_width)[0][1]
        else:
            adjusted_base_polygon = adjust_polygon(base_polygon, original_width, original_height, degree)

        #If polygon is completely outside
        if len(adjusted_base_polygon) == 0:
            continue

        adjusted_base_polygon_area = polygon_area(adjusted_base_polygon)
        
        if adjusted_base_polygon_area/area >= min_ratio:
            rotated_polygons = rotate_polygons(polygons, degree, center)
            rotated_polygons = adjust_polygons_tmp(rotated_polygons, original_width, original_height)

            rotated_polygons = convert_original_to_normal(rotated_polygons, original_width, original_height)
            
            rotated_list.append(rotated_polygons)

            rotated_image = rotate_image(img_path, -degree)
            save_image(output_folder, img_path, rotated_image, rotate_count)
            rotate_count = rotate_count + 1

            if rotate_count == max_number:
                break
    
    return rotated_list, rotate_count