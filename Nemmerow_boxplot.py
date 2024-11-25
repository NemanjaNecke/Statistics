import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

import numpy as np
import pandas as pd

# Create a dictionary with CF (PI) values for water and sediment
cf_water = {
    'Zn': [0.050, 0.050, 0.050, 0.050, 0.050, 0.050, 0.050, 0.050, 0.050],
    'As': [0.002, 0.005, 0.004, 0.005, 0.005, 0.005, 0.019, 0.014, 0.005],
    'Hg': [1.250, 1.250, 1.250, 1.250, 1.250, 1.250, 1.250, 1.250, 1.250],
    'Cd': [0.010, 0.010, 0.010, 0.010, 0.010, 0.010, 0.010, 0.010, 0.010],
    'Cu': [0.025, 0.025, 0.025, 0.025, 0.025, 0.025, 0.025, 0.025, 0.025],
    'Fe': [0.001, 0.001, 0.001, 0.001, 0.001, 0.001, 0.001, 0.001, 0.001],
    'Pb': [0.050, 0.050, 0.050, 0.050, 0.050, 0.050, 0.050, 0.050, 0.050],
    'Ni': [0.053, 0.016, 0.021, 0.025, 0.025, 0.021, 0.065, 0.045, 0.022]
}


# Convert the CF values to DataFrames for water and sediment
df_water = pd.DataFrame(cf_water)
df_sediment = pd.read_excel('cf_ef_results.xlsx')
df_sediment = df_sediment[['CF_As',	'CF_Hg'	,'CF_Zn',	'CF_Cd',	'CF_Cu',	'CF_Fe',	'CF_Pb',	'CF_Ni']]

# Function to calculate Nemerow Pollution Index with the correct formula
def calculate_nemerow_pollution_index(df):
    # Calculate PI_max (maximum CF value for each sample)
    PI_max = df.max(axis=1)
    
    # Calculate the average PI (mean CF value for each sample)
    PI_avg = df.mean(axis=1)
    
    # Calculate Nemerow Pollution Index (PI_N) with the correct formula
    n = len(df.columns)
    PI_N = np.sqrt(((1/n * np.sum(df.sub(1), axis=1))**2 + PI_max**2) / 2)
    
    return PI_N

# Calculate Nemerow Pollution Index for water and sediment
pi_n_water = calculate_nemerow_pollution_index(df_water)
pi_n_sediment = calculate_nemerow_pollution_index(df_sediment)

# Display the results
print("Nemerow Pollution Index for Water Samples:\n", pi_n_water)
print("\nNemerow Pollution Index for Sediment Samples:\n", pi_n_sediment)

# Save the results to Excel
output = pd.DataFrame({
    'Water PI_N': pi_n_water,
    'Sediment PI_N': pi_n_sediment
})

output.to_excel('corrected_nemerow_pollution_index_results.xlsx', index=False)

print("Nemerow Pollution Index calculations saved to 'corrected_nemerow_pollution_index_results.xlsx'.")


# Function to create individual boxplots for each column and save them as separate PNG files
def create_individual_boxplots(data, filename_prefix):
    elements = data.columns  # Column names from the dataframe
    
    for element in elements:
        # Create a figure for each boxplot
        plt.figure(figsize=(6, 6))
        sns.boxplot(y=data[element].dropna())  # Drop NaN values for plotting
        plt.title(f"Boxplot for {element}", fontsize=16)
        plt.ylabel(element, fontsize=14)
        plt.tight_layout()
        
        # Save each plot with a unique filename
        filename = f"{filename_prefix}_{element}.png"
        plt.savefig(filename)
        plt.close()

# Load your data from the uploaded file
file_path = "/mnt/data/file-H4WKDNDvSshBdt31JkjRQb"
data = pd.read_excel(file_path)

# Generate individual boxplots for each column
create_individual_boxplots(data, "boxplot")
