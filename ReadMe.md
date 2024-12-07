# QR Code DatA Loss Analysis

This project evaluates and compares the performance of OpenCV and Pyzxing in decoding QR codes under different levels of scratches. Statistical analysis tools are employed to highlight the differences between the two libraries in terms of decoding speed and accuracy.

---

## Prerequisites

1. **Dataset**: Ensure that the `benign` dataset of QR codes exists in the `QRCodeScanner/benign` directory relative to the project directory. These images serve as the base for generating scratched QR codes.
2. **Dependencies**:
   - Python 3.x
   - Required Python libraries:
     ```bash
     pip install opencv-python numpy pyzxing pandas scipy tqdm
     ```

---

## Running the Project

### 1. Generate Scratched QR Codes
Run the script to add scratches to the benign dataset. This generates QR codes with 5 levels of scratches (5, 10, 20, 30, 40 lines).

```bash
python add_scratches_to_qr.py
This script:

Reads QR codes from the QRCodeScanner/benign directory.
Creates scratched QR codes in QRCodeScanner/ScratchQR/ScratchLevel{1-5} directories.
2. Evaluate Performance with OpenCV
Run the OpenCV evaluation script to measure decoding time and success rate for each scratch level:

bash
Copy code
python OpenCVScratch.py
This script:

Processes QR codes in the QRCodeScanner/ScratchQR directory.
Outputs the results to QRCodeScanner/OpenCVPerformance/scratch_results_OpenCV.csv.
3. Evaluate Performance with Pyzxing
Run the Pyzxing evaluation script to measure decoding time and success rate for each scratch level:

bash
Copy code
python pyzxing_performance.py
This script:

Processes QR codes in the QRCodeScanner/ScratchQR directory.
Outputs the results to QRCodeScanner/pyzxingPerformance/pyzxing_results_csv.csv.
4. Analyze Results
Count Average Decoding Time and Successful Decodes
Run the count.py script to compute the average decoding time and number of successful decodes at each scratch level for both OpenCV and Pyzxing:

bash
Copy code
python count.py
This script processes the CSV files generated in the previous steps and outputs the average statistics for each scratch level.

Reproduce Statistical Analysis
Run the Stats.py script to perform statistical tests (t-test and Chi-square) on the results:

bash
Copy code
python Stats.py
This script:

Reads the output CSV files.
Conducts statistical analyses to compare OpenCV and Pyzxing's performance.
Project Objective
This project aims to clarify the differences in performance between OpenCV and Pyzxing QR code decoding libraries. By using statistical analysis tools, the project highlights the trade-offs between the two libraries:

OpenCV: Faster decoding times but lower resilience to scratches.
Pyzxing: Higher success rates in decoding but slower decoding times.
These insights can guide users in choosing the appropriate library based on their specific use case.