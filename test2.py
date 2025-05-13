import pandas as pd

# Load the Excel file
file_path = "/mnt/e/UBUNTU/Hindi_usr_generation/hindi_generator_mask/output_results.xlsx"

# Read the Excel sheet
df = pd.read_excel(file_path)

# Extract the two columns as lists if they exist
if "r6_k1" in df.columns and "r6_k2" in df.columns:
    r6_k1_list = df["r6_k1"].dropna().tolist()
    r6_k2_list = df["r6_k2"].dropna().tolist()
else:
    r6_k1_list, r6_k2_list = [], []

# Define file paths for storing the lists separately
file_r6_k1 = "/mnt/e/UBUNTU/Hindi_usr_generation/hindi_generator_mask/r6_k1.txt"
file_r6_k2 = "/mnt/e/UBUNTU/Hindi_usr_generation/hindi_generator_mask/r6_k2.txt"

# Write r6_k1 list to its file
with open(file_r6_k1, "w") as file:
    for item in r6_k1_list:
        file.write(f"{item}\n")

# Write r6_k2 list to its file
with open(file_r6_k2, "w") as file:
    for item in r6_k2_list:
        file.write(f"{item}\n")

# Return file paths
file_r6_k1, file_r6_k2
