import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
file_path_2 = 'corrected_nemerow_pollution_index_results.xlsx'
# Load the sediment and water data
file_path_1 = 'racun.xlsx'

# Read the data, excluding the 'Id' column
sediment_igeo = pd.read_excel(file_path_1, sheet_name='Sed_Igeo').drop(columns='Id.')
sediment_pi = pd.read_excel(file_path_1, sheet_name='Sed_PI').drop(columns='Id.')
water_igeo = pd.read_excel(file_path_1, sheet_name='Wat_Igeo').drop(columns='Id.')
water_pi = pd.read_excel(file_path_1, sheet_name='Wat_PI').drop(columns='Id.')

# ---------------------------------------------------------------
# Create Individual Boxplots for Each Element Combined into One Image
# ---------------------------------------------------------------
def create_boxplots(data, title, filename):
    elements = data.columns # Element columns like Zn, Cu, Pb, etc.
    fig, axs = plt.subplots(1, len(elements), figsize=(15, 6)) # Adjust layout based on number of elements
    fig.suptitle(title, fontsize=16)
    
    # Loop through each element and plot the corresponding boxplot
    for ax, element in zip(axs, elements):
        sns.boxplot(y=data[element].dropna(), ax=ax) # Use only the valid (non-NaN) data
        ax.set_title(element)
        ax.set_xticklabels([element], rotation=45) # Label with element name

    plt.tight_layout()
    plt.subplots_adjust(top=0.85) # Adjust space for the title
    plt.savefig(filename)
    plt.close()

# ---------------------------------------------------------------
# Generate 4 different boxplot images for sediment and water data
# ---------------------------------------------------------------

# 1. Igeo for Water
create_boxplots(water_igeo, 'Igeo Индекс за воду', 'igeo_boxplot_water.png')

# 2. Igeo for Sediment
create_boxplots(sediment_igeo, 'Igeo Индекс за седимент', 'igeo_boxplot_sediment.png')

# 3. PI for Water
create_boxplots(water_pi, 'PI Индекс за воду', 'pi_boxplot_water.png')

# 4. PI for Sediment
create_boxplots(sediment_pi, 'PI Индекс за седимент', 'pi_boxplot_sediment.png')


print("Boxplots have been successfully created and saved as individual images.")
