import cv2
import numpy as np
import os
from glob import glob
from tqdm import tqdm

# Define base directory relative to the script's location
BASE_DIR = os.path.dirname(__file__)

# Directories
SOURCE_DIR = os.path.join(BASE_DIR, "QRCodeScanner", "benign")
SCRATCH_DIRS = [
    os.path.join(BASE_DIR, "QRCodeScanner", "ScratchQR", "ScratchLevel1"),
    os.path.join(BASE_DIR, "QRCodeScanner", "ScratchQR", "ScratchLevel2"),
    os.path.join(BASE_DIR, "QRCodeScanner", "ScratchQR", "ScratchLevel3"),
    os.path.join(BASE_DIR, "QRCodeScanner", "ScratchQR", "ScratchLevel4"),
    os.path.join(BASE_DIR, "QRCodeScanner", "ScratchQR", "ScratchLevel5"),
]

# Create target directories if they don't exist
for dir_path in SCRATCH_DIRS:
    os.makedirs(dir_path, exist_ok=True)

# Function to add wear and tear (scratches)
def add_scratch(image, scratch_level):
    """
    Add scratches to an image.

    :param image: Input image (numpy array)
    :param scratch_level: Intensity of scratches (number of scratches)
    :return: Image with scratches
    """
    scratched_image = image.copy()
    rows, cols, _ = scratched_image.shape

    # Add scratch_level number of random lines
    for _ in range(scratch_level):
        # Randomize line properties
        x1, y1 = np.random.randint(0, cols), np.random.randint(0, rows)
        x2, y2 = np.random.randint(0, cols), np.random.randint(0, rows)
        thickness = max(1, scratch_level // 10)  # Adjust thickness to correlate with scratch level
        color = (0, 0, 0)  # Black lines for scratches

        # Draw the line on the image
        cv2.line(scratched_image, (x1, y1), (x2, y2), color, thickness)

    return scratched_image


# Main processing loop
def process_images():
    # Read all benign images
    benign_images = glob(os.path.join(SOURCE_DIR, "*.png"))

    # Scratch levels for testing
    scratch_levels = [5, 10, 20, 30, 40]  # Correct order of scratches

    for scratch_idx, (scratch_dir, scratch_level) in enumerate(zip(SCRATCH_DIRS, scratch_levels), start=1):
        print(f"Processing Scratch Level {scratch_idx} (scratches={scratch_level})...")
        image_count = 0

        # Loop to create 10,000 images with scratches for this level
        for _ in tqdm(range(10000), desc=f"Generating images for Scratch Level {scratch_idx}"):
            # Pick a random source image
            image_path = np.random.choice(benign_images)
            image = cv2.imread(image_path)

            if image is None:
                continue  # Skip unreadable files

            # Add scratches to the image
            scratched_image = add_scratch(image, scratch_level)

            # Save the scratched image
            filename = f"scratched_{image_count}_level{scratch_idx}.png"
            cv2.imwrite(os.path.join(scratch_dir, filename), scratched_image)

            image_count += 1


if __name__ == "__main__":
    process_images()
