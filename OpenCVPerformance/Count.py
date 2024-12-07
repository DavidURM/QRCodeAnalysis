import csv
from collections import defaultdict
import os

# Path to the CSV file (relative to the script's location)
CSV_PATH = os.path.join(os.path.dirname(__file__), "QRCodeScanner", "OpenCVPerformance", "scratch_results_OpenCV.csv")

def count_detections_and_avg_time(csv_path):
    # Dictionary to store counts and total time for each scratch level
    detection_counts = defaultdict(int)
    total_times = defaultdict(float)

    # Open the CSV file and read it
    with open(csv_path, mode='r') as file:
        reader = csv.DictReader(file)  # Use DictReader to access columns by name

        # Process each row
        for row in reader:
            scratch_level = int(row["Scratch Level"])  # Extract scratch level
            decode_status = row["Decode Status (Boolean)"] == "True"  # Check decode status
            time_to_decode = float(row["Time to Decode"])  # Extract time to decode

            if decode_status:
                detection_counts[scratch_level] += 1  # Increment count for this scratch level
                total_times[scratch_level] += time_to_decode  # Add time to total for this scratch level

    # Calculate average time per scratch level
    avg_times = {level: total_times[level] / detection_counts[level] if detection_counts[level] > 0 else 0
                 for level in detection_counts}

    return detection_counts, avg_times

def main():
    detection_counts, avg_times = count_detections_and_avg_time(CSV_PATH)

    # Display the results
    print("QR Code Detections per Scratch Level:")
    for scratch_level in sorted(detection_counts.keys()):
        print(f"Scratch Level {scratch_level}: {detection_counts[scratch_level]} detections, Average Time: {avg_times[scratch_level]:.6f} seconds")

if __name__ == "__main__":
    main()
