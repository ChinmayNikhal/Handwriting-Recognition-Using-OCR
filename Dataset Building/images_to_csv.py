import cv2, csv, os
import numpy as np
from PIL import Image, ImageFilter

def resize_images(base_folder, target_size=(28, 28)):
    """
    Processes images in the given folder by sharpening and resizing.

    Parameters:
        base_folder (str): Path to the main folder containing subfolders of images.
        target_size (tuple): Desired size for the resized images, default is (28, 28).

    Returns:
        None
    """
    if not os.path.exists(base_folder):
        print(f"Folder '{base_folder}' does not exist.")
        return

    for subfolder in os.listdir(base_folder):
        subfolder_path = os.path.join(base_folder, subfolder)

        # Ensure it's a folder and the name corresponds to the ASCII character range
        if os.path.isdir(subfolder_path) and subfolder.isdigit():
            ascii_value = int(subfolder)
            if 65 <= ascii_value <= 90 or 97 <= ascii_value <= 122:
                for file_name in os.listdir(subfolder_path):
                    file_path = os.path.join(subfolder_path, file_name)

                    # Check if it's an image file
                    try:
                        with Image.open(file_path) as img:
                            # Sharpen the image
                            sharpened_img = img.filter(ImageFilter.SHARPEN)

                            # Resize the image
                            resized_img = sharpened_img.resize(target_size)

                            # Save the modified image back to its original location
                            resized_img.save(file_path)

                            print(f"Processed image: {file_path}")
                    except Exception as e:
                        print(f"Could not process file {file_path}: {e}")


def preproc_img(image_path):
    """
    Preprocesses an image by displaying the grayscale, binarized, and resized versions.
    Inverts colors (white to black and black to white) in the final image.

    Parameters:
        image_path (str): Path to the input image.

    Returns:
        numpy.ndarray: The final processed image.
    """
    try:
        # Read the image using OpenCV
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError("Invalid image path or file.")

        # Step 1: Convert to Grayscale
        grayscale_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # cv2.imshow("Grayscale Image", grayscale_image)

        # Step 2: Binarize the image
        _, binarized_image = cv2.threshold(grayscale_image, 128, 255, cv2.THRESH_BINARY)
        # cv2.imshow("Binarized Image", binarized_image)

        # Step 3: Invert colors
        inverted_image = cv2.bitwise_not(binarized_image)
        # cv2.imshow("Inverted Image", inverted_image)

        # Step 4: Resize the image
        resized_image = cv2.resize(inverted_image, (28, 28), interpolation=cv2.INTER_AREA)
        # cv2.imshow("Resized Image", resized_image)

        # Wait for user to close windows
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

        return resized_image
    except Exception as e:
        print(f"Error processing image: {e}")
        return None

def images_to_csv(folder_path, csv_path):
    """
    Processes all images in a folder, applies preprocessing, and saves the results to a CSV file.

    Parameters:
        folder_path (str): Path to the folder containing subfolders of images.
        csv_path (str): Path to save the output CSV file.
    """
    try:
        with open(csv_path, mode='w', newline='') as csv_file:
            writer = csv.writer(csv_file)

            # Iterate through subfolders
            for ascii_value in range(65, 91):  # Uppercase A-Z
                subfolder_path = os.path.join(folder_path, str(ascii_value))
                if not os.path.exists(subfolder_path):
                    continue

                for image_name in os.listdir(subfolder_path):
                    image_path = os.path.join(subfolder_path, image_name)

                    # Preprocess the image
                    processed_image = preproc_img(image_path)
                    if processed_image is not None:
                        # Flatten the image and write to CSV
                        flattened_image = processed_image.flatten()
                        writer.writerow([ascii_value] + flattened_image.tolist())

            for ascii_value in range(97, 123):  # Lowercase a-z
                subfolder_path = os.path.join(folder_path, str(ascii_value))
                if not os.path.exists(subfolder_path):
                    continue

                for image_name in os.listdir(subfolder_path):
                    image_path = os.path.join(subfolder_path, image_name)

                    # Preprocess the image
                    processed_image = preproc_img(image_path)
                    if processed_image is not None:
                        # Flatten the image and write to CSV
                        flattened_image = processed_image.flatten()
                        writer.writerow([ascii_value] + flattened_image.tolist())

        print(f"CSV file saved to {csv_path}")

    except Exception as e:
        print(f"Error writing to CSV: {e}")

# Example usage:
# resize_images("path_to_the_images_main_folder")
images_to_csv("path_to_the_images_main_folder", "output.csv")
