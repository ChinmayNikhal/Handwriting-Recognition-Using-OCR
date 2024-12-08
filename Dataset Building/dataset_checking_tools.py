import os, csv, cv2
from PIL import Image
import pandas as pd
import numpy as np


def check_image_dimensions(folder_path, required_width=28, required_height=28):
    """
    Checks if all images in a folder and its subfolders are of the required dimensions.

    Args:
        folder_path (str): Path to the folder to check.
        required_width (int): Required width of the images in pixels.
        required_height (int): Required height of the images in pixels.

    Returns:
        list: List of file paths for images that do not match the required dimensions.
    """
    invalid_images = []

    for root, _, files in os.walk(folder_path):
        for file in files:
            print(root[(len(folder_path)+1):])
            file_path = os.path.join(root, file)
            try:
                with Image.open(file_path) as img:
                    if img.size != (required_width, required_height):
                        invalid_images.append(file_path)
            except (IOError, OSError):
                print(f"Skipping non-image file: {file_path}")

    return invalid_images

# if __name__ == "__main__":
#     folder = input("Enter the folder path to check: ").strip()

#     if not os.path.isdir(folder):
#         print(f"Invalid folder path: {folder}")
#     else:
#         invalid_images = check_image_dimensions(folder)

#         if invalid_images:
#             print("The following images do not match the required dimensions (28x28):")
#             for img in invalid_images:
#                 print(img)
#         else:
#             print("All images have the required dimensions (28x28).")

def view_image_from_csv(csv_file, row_index, image_size=(28, 28)):
    """
    Displays an image from the CSV file by reconstructing it from the flattened array.

    Parameters:
        csv_file (str): Path to the CSV file.
        row_index (int): Row index of the image in the CSV file (0-based).
        image_size (tuple): Size of the image (width, height), default is (28, 28).

    Returns:
        None
    """
    try:
        with open(csv_file, mode='r') as file:
            reader = csv.reader(file)
            rows = list(reader)

            if row_index < 0 or row_index >= len(rows):
                print(f"Row index {row_index} is out of range.")
                return

            row = rows[row_index]
            ascii_value = row[0]
            flattened_array = list(map(int, row[1:]))

            # Reconstruct the image
            image = np.array(flattened_array, dtype=np.uint8).reshape(image_size)

            print(f"Displaying image for ASCII value: {ascii_value}")

            # Use OpenCV to display the image
            cv2.imshow(f"ASCII {ascii_value}", image)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
    except Exception as e:
        print(f"Could not read or display image from CSV: {e}")

def sort_the_csv_file(csv_file):
    pass
    csvData = pd.read_csv(csv_file)
    print("Before sorting...\n", csvData[:4])

    csvData.sort_values(csvData.columns[0], axis=0, inplace=True)

    print("After sorting...\n", csvData[:4])
    csvData.to_csv("mehhh.csv")

# Example usage:

# sort_the_csv_file("output.csv")
# view_image_from_csv("output.csv", 0)
view_image_from_csv("output.csv", 63501)
