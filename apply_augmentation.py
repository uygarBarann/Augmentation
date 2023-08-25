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







def apply_augmentation( 
        rotate_class,
        crop_class,
        crop=False,
        rotate=False,
        color=False,
        rotation_percentage=15,
        num_crop = 1, 
        num_rotate = 1, 
        num_color = 1,
        images_directory = "images",
        labels_directory = "labels",
        cropped_images_directory = "cropped_images",
        cropped_labels_directory = "cropped_labels",
        rotated_images_directory = "rotated_images",
        rotated_labels_directory = "rotated_labels",
        colored_images_directory = "colored_images",
    ):
    
    # Create output directories if they don't exist
    os.makedirs(cropped_images_directory, exist_ok=True)
    os.makedirs(cropped_labels_directory, exist_ok=True)
    os.makedirs(rotated_images_directory, exist_ok=True)
    os.makedirs(rotated_labels_directory, exist_ok=True)
    os.makedirs(colored_images_directory, exist_ok=True)
    
    
    for filename in os.listdir(images_directory):
        
        image_path = os.path.join(images_directory, filename)
        base_name, _ = os.path.splitext(filename)
        label_path = os.path.join(labels_directory, base_name + ".txt")
        
        try:
            polygons,to_rotate , to_crop = extract_polygons(label_path,rotate_class= rotate_class,crop_class= crop_class)
            
            
            if crop:    
                cropped_polygons, numberOfSuccesfullCrops = crop(image_path, to_crop, cropped_images_directory, num_crop)
                for i in range (0,numberOfSuccesfullCrops):
                    cropped_label_path = os.path.join(cropped_labels_directory, base_name +  "_cropped" + str(i) + ".txt")
                    save_label(cropped_polygons[i], cropped_label_path)
            
            if rotate:    
                rotated_polygons, numberOfSuccesfullRotations = rotation(image_path, to_rotate, rotated_images_directory, num_rotate,rotation_percentage)
                for i in range (0,numberOfSuccesfullRotations):
                    rotated_label_path = os.path.join(rotated_labels_directory, base_name +  "_rotated" + str(i) + ".txt")
                    save_label(rotated_polygons[i], rotated_label_path)
            if color:        
                numberOfSuccesfullColors=color(image_path, colored_images_directory, num_color)
            
            
           
            
        except FileNotFoundError:
            print(f"Label file missing for image: {image_path}")
        except Exception as e:
            print(f"An error occurred for image {image_path}: {e}")