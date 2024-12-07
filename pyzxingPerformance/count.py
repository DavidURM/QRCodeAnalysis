import csv
from collections import defaultdict
import os

# Define the base directory relative to the script's location
BASE_DIR = os.path.dirname(__file__)
file_path = os.path.join(BASE_DIR, "QRCodeScanner", "pyzxingPerformance", "pyzxing_results_csv.csv")

# Dictionaries to store the counts and total times for each scratch level
scratch_level_counts = defaultdict(int)
total_decode_times = defaultdict(float)

try:
    # Open the CSV file and process it
    with open(file_path, mode='r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            scratch_level = int(row['Scratch Level'])
            decode_status = row['Decode Status (Boolean)'].strip().lower() == 'true'
            time_to_decode = float(row['Time to Decode'])  # Extract time to decode

            # Increment count and add time if decode status is True
            if decode_status:
                scratch_level_counts[scratch_level] += 1
                total_decode_times[scratch_level] += time_to_decode

    # Calculate average decode time per scratch level
    avg_decode_times = {
        level: total_decode_times[level] / scratch_level_counts[level] if scratch_level_counts[level] > 0 else 0
        for level in scratch_level_counts
    }

    # Print the results
    print("Successfully Decoded Counts per Scratch Level:")
    for level in sorted(scratch_level_counts.keys()):
        print(f"Scratch Level {level}: {scratch_level_counts[level]} codes successfully decoded, Average Time: {avg_decode_times[level]:.6f} seconds")

except Exception as e:
    print(f"An error occurred: {e}")
