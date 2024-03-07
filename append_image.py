import cv2
import numpy as np

def append_images(image1_path, image2_path, output_path):
    # Read images
    image1 = cv2.imread(image1_path)
    image2 = cv2.imread(image2_path)

    # Check if images are loaded successfully
    if image1 is None or image2 is None:
        print("Error: Could not read images.")
        return

    # Append images vertically
    appended_image = np.vstack((image1, image2))

    # Save the result
    cv2.imwrite(output_path, appended_image)

    print(f"Images appended successfully. Result saved at: {output_path}")

if __name__ == "__main__":
# Replace 'image1.jpg', 'image2.jpg', and 'output.jpg' with your file paths
    image1_path = 'page_1.png'
    image2_path = 'page_2.png'
    output_path = 'output.png'

    append_images(image1_path, image2_path, output_path)
