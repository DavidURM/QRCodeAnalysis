import os
import csv
import time
from pyzxing import BarCodeReader


def decode_qr_codes(folder_path, level, csv_writer):
    # Initialize the barcode reader
    reader = BarCodeReader()
    # Counter for successfully decoded QR codes
    image_number = 0

    # Iterate over all files in the folder
    for file_name in os.listdir(folder_path):
        # Construct full file path
        file_path = os.path.join(folder_path, file_name)
        if file_name.lower().endswith('.png'):
            image_number += 1
            start_time = time.time()  # Start timing
            results = reader.decode(file_path)
            end_time = time.time()  # End timing
            decode_time = end_time - start_time

            # Determine decode status
            decode_status = False
            if results:  # Check if there are results
                for result in results:
                    if result.get('parsed', None):
                        decode_status = True
                        break

            # Write result to CSV
            csv_writer.writerow([level, image_number, decode_time, decode_status])
            print(f"Processed: {file_name}, Level: {level}, Status: {decode_status}")


def main():
    # Define the base directory relative to the script location
    BASE_DIR = os.path.dirname(__file__)
    base_folder_path = os.path.join(BASE_DIR, "QRCodeScanner", "ScratchQR")
    output_csv_path = os.path.join(BASE_DIR, "QRCodeScanner", "pyzxingPerformance", "pyzxing_results_csv.csv")

    # Open CSV file for writing
    os.makedirs(os.path.dirname(output_csv_path), exist_ok=True)  # Ensure the output directory exists
    with open(output_csv_path, mode='w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        # Write header
        csv_writer.writerow(['Scratch Level', 'Image Number', 'Time to Decode', 'Decode Status (Boolean)'])

        # Process each Scratch Level folder
        for level in range(1, 6):
            folder_path = os.path.join(base_folder_path, f"ScratchLevel{level}")
            print(f"Processing Scratch Level {level}...")
            decode_qr_codes(folder_path, level, csv_writer)

    print(f"Results written to {output_csv_path}")


if __name__ == "__main__":
    main()
