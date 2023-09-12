import numpy as np
from rot_utils import *

#Takes two line segments and finds the intersection
#A and B are ((x1, y1), (x2, y2))
def find_intersection(A, B):
    x1, y1, x2, y2 = A[0][0], A[0][1], A[1][0], A[1][1]
    x3, y3, x4, y4 = B[0][0], B[0][1], B[1][0], B[1][1]

    det = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)

    intersection_x = ((x1 * y2 - y1 * x2) * (x3 - x4) - (x1 - x2) * (x3 * y4 - y3 * x4)) / det
    intersection_y = ((x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) * (x3 * y4 - y3 * x4)) / det

    return np.array([intersection_x, intersection_y]).astype("int32")


def adjust_polygon_tmp(polygon, edge, w, h):
        new_polygon = []
        leng = len(polygon)

        #Traverses the polygon taking two points every time
        for i in range(leng):
            point_pair = [polygon[i], polygon[(i + 1) % leng]]

            #This part is hard-coded, we need to modify this part
            #Checks if points are inside the borders corresponding to given edge input
            if edge == "top":
                first_inside = 0 <= point_pair[0][1]
                second_inside = 0 <= point_pair[1][1]
            elif edge == "right":
                first_inside = point_pair[0][0] <= w
                second_inside = point_pair[1][0] <= w
            elif edge == "bottom":
                first_inside = point_pair[0][1] <= h
                second_inside = point_pair[1][1] <= h
            else:
                first_inside = 0 <= point_pair[0][0]
                second_inside = 0 <= point_pair[1][0]

            #If they are both inside, we don't need to modify anything, we add the second point to the new polygon
            if first_inside and second_inside:
                new_polygon.append(point_pair[1])
            
            #One of them is inside and the other is not
            #We find the intersection point and add it to the new polygon
            #If second one is inside, we also add the second point to the new polygon
            elif first_inside or second_inside:
                if edge == "top":
                    new_point = find_intersection(point_pair, ((0, 0), (w, 0)))
                elif edge == "right":
                    new_point = find_intersection(point_pair, ((w, 0), (w, h)))
                elif edge == "bottom":
                    new_point = find_intersection(point_pair, ((0, h), (w, h)))
                elif edge == "left":
                    new_point = find_intersection(point_pair, ((0, 0), (0, h)))
                
                new_polygon.append(new_point)

                if second_inside:
                    new_polygon.append(point_pair[1])

        #If the rotated polygon is totally out of the image borders, return empty list to check in adjusted_polygons function
        if len(new_polygon) == 0:
            return []

        return np.array(new_polygon)

#Controls each polygon if they are inside the borders according to each edge and adjust the polygon to be inside the border appropriately
def adjust_polygons_tmp(polygons, w, h):
    new_polygons = []

    for label, polygon in polygons:
        adjusted_polygon = adjust_polygon_tmp(polygon, "top", w, h)
        adjusted_polygon = adjust_polygon_tmp(adjusted_polygon, "right", w, h)
        adjusted_polygon = adjust_polygon_tmp(adjusted_polygon, "bottom", w, h)
        adjusted_polygon = adjust_polygon_tmp(adjusted_polygon, "left", w, h)

        #If the rotated polygon is totally out of the image borders
        if adjusted_polygon is None:
            continue

        new_polygons.append((label, adjusted_polygon))

    return new_polygons

def line_equation(x, y, a, b, c):
    return (a * x + b * y + c)

def calculate_coefficients(x1, y1, x2, y2):
    # Calculate the slope
    if (x2-x1 == 0):
        slope = 0
    else:
        slope = (y2 - y1) / (x2 - x1)
    
    # Calculate coefficients a, b, and c
    a = -slope
    b = 1
    c = slope * x1 - y1
    
    return a, b, c

def find_inside_polygon(polygon, center, endpoint1, endpoint2):
    center_x, center_y = center
    x1, y1 = endpoint1
    x2, y2 = endpoint2
    a, b, c = calculate_coefficients(x1, y1, x2, y2)
    center_result = line_equation(center_x, center_y, a, b, c)
    new_polygon = []
    
    length = len(polygon)
    for i in range(length):
        point_pair = [polygon[i], polygon[(i + 1) % length]]
        if (center_result <= 0):
            first_inside = 0 >= line_equation(point_pair[0][0], point_pair[0][1], a, b, c)
            second_inside = 0 >= line_equation(point_pair[1][0], point_pair[1][1], a, b, c)
        else:
            first_inside = 0 <= line_equation(point_pair[0][0], point_pair[0][1], a, b, c)
            second_inside = 0 <= line_equation(point_pair[1][0], point_pair[1][1], a, b, c)

        if first_inside and second_inside:
            new_polygon.append(point_pair[1])
        elif first_inside or second_inside:
            intersection_point = find_intersection(point_pair, (endpoint1, endpoint2))

            new_polygon.append(intersection_point)

            if second_inside:
                new_polygon.append(point_pair[1])

    return new_polygon

def adjust_polygon(polygon, w, h, degree):
    center = (w/2, h/2)

    corners = np.array([[0, 0], (w, 0), (w, h), (0, h)])

    rotated_image_coords = rotate_polygon(corners, -np.radians(degree), center)

    adjusted_polygon = find_inside_polygon(polygon, center, rotated_image_coords[0],rotated_image_coords[1])
    adjusted_polygon = find_inside_polygon(adjusted_polygon, center, rotated_image_coords[1],rotated_image_coords[2])
    adjusted_polygon = find_inside_polygon(adjusted_polygon, center, rotated_image_coords[2],rotated_image_coords[3])
    adjusted_polygon = find_inside_polygon(adjusted_polygon, center, rotated_image_coords[3],rotated_image_coords[0])

    return  adjusted_polygon