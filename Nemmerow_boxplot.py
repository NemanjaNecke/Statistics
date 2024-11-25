import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

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
