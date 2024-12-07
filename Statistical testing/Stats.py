import os
import pandas as pd
from scipy import stats

# Define the base directory relative to the script location
BASE_DIR = os.path.dirname(__file__)

# Paths to the CSV files (relative paths)
opencv_path = os.path.join(BASE_DIR, "QRCodeScanner", "OpenCVPerformance", "scratch_results_OpenCV.csv")
pyzxing_path = os.path.join(BASE_DIR, "QRCodeScanner", "pyzxingPerformance", "pyzxing_results_csv.csv")

# Load the datasets
df_opencv = pd.read_csv(opencv_path)
df_pyzxing = pd.read_csv(pyzxing_path)

# Ensure data is correctly loaded by inspecting the first few rows (optional)
print("OpenCV Data Sample:")
print(df_opencv.head())
print("Pyzxing Data Sample:")
print(df_pyzxing.head())

# Null Hypothesis (H0):
# For decoding time: OpenCV's decoding time is equal to or slower than pyzxing's decoding time.
# For success rate: There is no significant difference in success rates between pyzxing and OpenCV.

# Alternative Hypothesis (H1):
# For decoding time: OpenCV has a significantly faster decoding time than pyzxing.
# For success rate: Pyzxing has a significantly higher success rate than OpenCV.

# Calculate mean time to decode for each library at each scratch level
opencv_times = df_opencv.groupby('Scratch Level')['Decode Status (Boolean)'].mean()
pyzxing_times = df_pyzxing.groupby('Scratch Level')['Decode Status (Boolean)'].mean()

# Output the mean decoding times for both libraries
print("\nMean Time to Decode for OpenCV:")
print(opencv_times)
print("\nMean Time to Decode for pyzxing:")
print(pyzxing_times)

# Perform Paired t-test (converted to one-tailed)
t_stat, p_value_two_tailed = stats.ttest_rel(opencv_times, pyzxing_times)
if t_stat < 0:
    p_value_one_tailed = p_value_two_tailed / 2.0
else:
    p_value_one_tailed = 1.0 - (p_value_two_tailed / 2.0)

print(f"\nOne-tailed t-test result for time to decode:\n"
      f"t-statistic = {t_stat}\np-value = {p_value_one_tailed}")

# Print hypotheses for decoding time
print("\nNull Hypothesis (H0):")
print("For decoding time: OpenCV's decoding time is equal to or slower than pyzxing's decoding time.")
print("Alternative Hypothesis (H1):")
print("For decoding time: OpenCV has a significantly faster decoding time than pyzxing.")

# Calculate success rates (assuming 'Decode Status' is boolean, True = success, False = failure)
opencv_success_rate = df_opencv.groupby('Scratch Level')['Decode Status (Boolean)'].mean()
pyzxing_success_rate = df_pyzxing.groupby('Scratch Level')['Decode Status (Boolean)'].mean()

# Output the success rates for both libraries
print("\nSuccess Rate for OpenCV:")
print(opencv_success_rate)
print("\nSuccess Rate for pyzxing:")
print(pyzxing_success_rate)

# Chi-Square Test for Success Rate
opencv_success_failure = df_opencv.groupby('Scratch Level')['Decode Status (Boolean)'].value_counts().unstack(fill_value=0)
pyzxing_success_failure = df_pyzxing.groupby('Scratch Level')['Decode Status (Boolean)'].value_counts().unstack(fill_value=0)

chi2_stat, p_val, dof, expected = stats.chi2_contingency([opencv_success_failure[True], pyzxing_success_failure[True]])

print(f"\nChi-Square Test result for success rate:\n"
      f"Chi2-statistic = {chi2_stat}\np-value = {p_val}\nDegrees of freedom = {dof}\nExpected frequencies:\n{expected}")

# Print hypotheses for success rate
print("\nNull Hypothesis (H0):")
print("For success rate: There is no significant difference in success rates between pyzxing and OpenCV.")
print("Alternative Hypothesis (H1):")
print("For success rate: Pyzxing has a significantly higher success rate than OpenCV.")

# Interpret results for the time test using the one-tailed p-value
if p_value_one_tailed < 0.05 and t_stat < 0:
    print("\nThe one-tailed t-test suggests OpenCV has a significantly faster decoding time than pyzxing.")
else:
    print("\nThe one-tailed t-test suggests OpenCV does not have a faster decoding time than pyzxing.")

# For Chi-Square Test: Pyzxing has a higher success rate
opencv_success_count = opencv_success_failure[True].sum()
pyzxing_success_count = pyzxing_success_failure[True].sum()

if p_val < 0.05 and pyzxing_success_count > opencv_success_count:
    print("\nThe Chi-Square test suggests pyzxing has a significantly higher success rate than OpenCV.")
else:
    print("\nThe Chi-Square test suggests no significant difference in the success rates between pyzxing and OpenCV.")

print("---------INDIVIDUAL SCRATCH LEVEL TESTING-----------")
# Now run the paired t-test (one-tailed) and Chi-Square test for each scratch level (up to level 3)

for level in range(1, 4):  # Loop through levels 1, 2, and 3
    print(f"\nTesting for Scratch Level {level}:")
    opencv_level = df_opencv[df_opencv['Scratch Level'] == level]
    pyzxing_level = df_pyzxing[df_pyzxing['Scratch Level'] == level]

    # Paired t-test for decoding time (one-tailed)
    t_stat_level, p_value_level_two_tailed = stats.ttest_rel(opencv_level['Time to Decode'], pyzxing_level['Time to Decode'])
    if t_stat_level < 0:
        p_value_level_one_tailed = p_value_level_two_tailed / 2.0
    else:
        p_value_level_one_tailed = 1.0 - (p_value_level_two_tailed / 2.0)

    print(f"One-tailed t-test for time to decode at Level {level}:\n"
          f"t-statistic = {t_stat_level}\np-value = {p_value_level_one_tailed}")

    print("\nNull Hypothesis (H0):")
    print(f"For decoding time at Scratch Level {level}: OpenCV's decoding time is equal to or slower than pyzxing's decoding time.")
    print("Alternative Hypothesis (H1):")
    print(f"For decoding time at Scratch Level {level}: OpenCV has a significantly faster decoding time than pyzxing.")

    # Chi-Square Test for success rate at this level
    opencv_success_failure_level = opencv_level.groupby('Decode Status (Boolean)').size()
    pyzxing_success_failure_level = pyzxing_level.groupby('Decode Status (Boolean)').size()
    chi2_stat_level, p_val_level, dof_level, expected_level = stats.chi2_contingency(
        [opencv_success_failure_level, pyzxing_success_failure_level])

    print(f"Chi-Square Test for success rate at Level {level}:\n"
          f"Chi2-statistic = {chi2_stat_level}\np-value = {p_val_level}\nDegrees of freedom = {dof_level}\n"
          f"Expected frequencies:\n{expected_level}")

    print("\nNull Hypothesis (H0):")
    print(f"For success rate at Scratch Level {level}: There is no significant difference in success rates between pyzxing and OpenCV.")
    print("Alternative Hypothesis (H1):")
    print(f"For success rate at Scratch Level {level}: Pyzxing has a significantly higher success rate than OpenCV.")

    opencv_success_count_level = opencv_success_failure_level[True]
    pyzxing_success_count_level = pyzxing_success_failure_level[True]

    if p_value_level_one_tailed < 0.05 and t_stat_level < 0:
        print(f"\nThe one-tailed t-test suggests OpenCV has a significantly faster decoding time at Level {level}.")
    else:
        print(f"\nThe one-tailed t-test suggests OpenCV does not have a faster decoding time at Level {level}.")

    if p_val_level < 0.05 and pyzxing_success_count_level > opencv_success_count_level:
        print(f"\nThe Chi-Square test suggests pyzxing has a significantly higher success rate at Level {level}.")
    else:
        print(f"\nThe Chi-Square test suggests no significant difference in the success rates at Level {level}.")
