import cv2
import os
import time
import pandas as pd

# Define the base directory relative to the script location
BASE_DIR = os.path.dirname(__file__)

# Input directories and output CSV file (relative paths)
input_paths = [
    os.path.join(BASE_DIR, "QRCodeScanner", "ScratchQR", "ScratchLevel1"),
    os.path.join(BASE_DIR, "QRCodeScanner", "ScratchQR", "ScratchLevel2"),
    os.path.join(BASE_DIR, "QRCodeScanner", "ScratchQR", "ScratchLevel3"),
    os.path.join(BASE_DIR, "QRCodeScanner", "ScratchQR", "ScratchLevel4"),
    os.path.join(BASE_DIR, "QRCodeScanner", "ScratchQR", "ScratchLevel5"),
]
output_csv = os.path.join(BASE_DIR, "QRCodeScanner", "OpenCVPerformance", "Scratch", "scratch_results_OpenCV.csv")

# Initialize an empty list to hold the results
results = []

# Iterate through the input directories
for level, path in enumerate(input_paths, start=1):
    print(f"Processing Scratch Level {level}...")
    image_files = sorted(os.listdir(path))

    # Process each image in the directory
    for idx, image_file in enumerate(image_files):
        image_path = os.path.join(path, image_file)

        # Read the image
        image = cv2.imread(image_path)
        if image is None:
            print(f"Failed to load {image_path}")
            continue

        # Decode the QR code
        start_time = time.time()
        detector = cv2.QRCodeDetector()
        try:
            data, points, _ = detector.detectAndDecode(image)
            decode_status = bool(data)  # Determine if decoding was successful
        except cv2.error as e:
            # Handle OpenCV error gracefully
            print(f"Error decoding {image_path}: {e}")
            data, points, decode_status = None, None, False

        decode_time = time.time() - start_time

        # Append the result
        results.append({
            "Scratch Level": level,
            "Image Number": idx + 1,
            "Time to Decode": decode_time,
            "Decode Status": decode_status,
        })

        # Print progress every 1000 images
        if (idx + 1) % 1000 == 0:
            print(f"Processed {idx + 1}/{len(image_files)} images for Level {level}")

# Save results to CSV
df = pd.DataFrame(results)
os.makedirs(os.path.dirname(output_csv), exist_ok=True)  # Ensure the output directory exists
df.to_csv(output_csv, index=False)
print(f"Results saved to {output_csv}")
