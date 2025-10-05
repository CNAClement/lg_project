import os
import cv2

def pre_traitement_image(image_path):
    if os.path.exists(image_path):
        print(f"image trouvée : {image_path}")
        img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE) # gris pour atténuer le bruit
        img = cv2.resize(img, (64,64))  
        x_crop = img.flatten().reshape(1, -1)
        return x_crop
    else:
        raise FileNotFoundError(f"L'image {image_path} n'existe pas.")