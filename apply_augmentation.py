import os

def extract_polygons(label_path,rotate_class,crop_class):
    # Process the files using image_path and label_path
    polygons = []
    to_rotate=[]
    to_crop=[]
    with open(label_path, 'r') as label_file:
        for line in label_file:
            line = line.strip()
            parts = line.split()

            # Parse the first number as 'class'
            class_value = int(parts[0])

            # Parse remaining parts into a list of tuples
            polygon = [(float(parts[i]), float(parts[i + 1])) for i in range(1, len(parts), 2)]

            if class_value in rotate_class:
                to_rotate.append((class_value, polygon))
            if class_value in crop_class:
                to_crop.append((class_value, polygon))

            print(f"Class: {class_value}")
            print(f"Tuples: {polygon}")

            polygons.append((class_value, polygon))
    print("\n\n")
    return polygons,to_rotate,to_crop


def save_label(updated_polygons, output_label_path):
    # Save the updated polygons as label file
    with open(output_label_path, 'w') as label_file:
        for class_value, polygon in updated_polygons:
            polygon_line = f"{class_value} " + " ".join([f"{coord:.6f}" for vertex in polygon for coord in vertex])
            label_file.write(polygon_line + "\n")

