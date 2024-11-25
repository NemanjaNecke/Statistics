import pandas as pd
import numpy as np

# Load the 'spss.xlsx' data sheet
data = pd.read_excel('spss.xlsx').set_index('Id.')

# Splitting the data into sediment (mg/kg) and water (µg/l) data
sediment_columns = [col for col in data.columns if 'mg/kg' in col]
water_columns = [col for col in data.columns if 'µg/l' in col]

sediment_data = data[sediment_columns]
water_data = data[water_columns]

# Updated Reference values (Cᵢₙ) for sediment
reference_values_sediment = {
    'Zn (mg/kg)': 70.00,
    'As (mg/kg)': 1.80,
    'Hg (mg/kg)': 0.08,
    'Cd (mg/kg)': 0.2,
    'Cu (mg/kg)': 55.00,
    'Fe (mg/kg)': 3.59,
    'Pb (mg/kg)': 12.50,
    'Ni (mg/kg)': 75.00
}

# Toxic response factors (Tᵢᵣ) for sediment
toxic_response_factors_sediment = {
    'Zn (mg/kg)': 1,
    'As (mg/kg)': 10,
    'Hg (mg/kg)': 40,
    'Cd (mg/kg)': 30,
    'Cu (mg/kg)': 5,
    'Fe (mg/kg)': 1,
    'Pb (mg/kg)': 5,
    'Ni (mg/kg)': 5
}

# Reference values (Cᵢₙ) for water
reference_values_water = {
    'As (µg/l)': 9.50,
    'Cd (µg/l)': 0.30,
    'Cr (µg/l)': 123.20,
    'Cu (µg/l)': 28.30,
    'Hg (µg/l)': 0.10,
    'Ni (µg/l)': 57.00,
    'Pb (µg/l)': 19.80,
    'Zn (µg/l)': 84.00
}

# Toxic response factors (Tᵢᵣ) for water
toxic_response_factors_water = {
    'As (µg/l)': 10,
    'Cd (µg/l)': 30,
    'Cr (µg/l)': 2,
    'Cu (µg/l)': 5,
    'Hg (µg/l)': 40,
    'Ni (µg/l)': 5,
    'Pb (µg/l)': 5,
    'Zn (µg/l)': 1
}

# Function to calculate PLI
def calculate_pli(data, background):
    contamination_factors = data.div(background)
    pli = contamination_factors.prod(axis=1)**(1.0 / len(contamination_factors.columns))
    return pli

# Function to calculate Igeo
def calculate_igeo(data, background):
    igeo = np.log2(data.div(background) / 1.5)
    return igeo

# Function to calculate PI (Pollution Index)
def calculate_pi(data, background):
    pi = data.div(background)
    return pi

# Function to calculate ΣTUs (Toxic Units)
def calculate_tus(data, background, toxic_response_factors):
    contamination_factors = data.div(background)
    tus = contamination_factors.mul(pd.Series(toxic_response_factors), axis=1)
    total_tus = tus.sum(axis=1)
    return tus, total_tus

# Perform calculations for sediment and water
# Sediment Calculations
pli_sediment = calculate_pli(sediment_data, pd.Series(reference_values_sediment))
igeo_sediment = calculate_igeo(sediment_data, pd.Series(reference_values_sediment))
pi_sediment = calculate_pi(sediment_data, pd.Series(reference_values_sediment))
tus_sediment, total_tus_sediment = calculate_tus(sediment_data, pd.Series(reference_values_sediment), toxic_response_factors_sediment)

# Water Calculations
pli_water = calculate_pli(water_data, pd.Series(reference_values_water))
igeo_water = calculate_igeo(water_data, pd.Series(reference_values_water))
pi_water = calculate_pi(water_data, pd.Series(reference_values_water))
tus_water, total_tus_water = calculate_tus(water_data, pd.Series(reference_values_water), toxic_response_factors_water)

# Create a Pandas Excel writer object
with pd.ExcelWriter('calculated_indices_results.xlsx') as writer:
    # Write data and results for sediment
    sediment_data.to_excel(writer, sheet_name='Sediment Data')
    pd.Series(reference_values_sediment).to_excel(writer, sheet_name='Sediment Data', startrow=len(sediment_data) + 3, header=False)
    
    # PLI, Igeo, PI, and ΣTUs with shortened sheet names and proper column names
    pd.DataFrame(pli_sediment, columns=['PLI (Sediment)']).to_excel(writer, sheet_name='Sed_PLI')
    pd.DataFrame(igeo_sediment, columns=sediment_data.columns).to_excel(writer, sheet_name='Sed_Igeo')
    pd.DataFrame(pi_sediment, columns=sediment_data.columns).to_excel(writer, sheet_name='Sed_PI')
    pd.DataFrame(tus_sediment, columns=sediment_data.columns).to_excel(writer, sheet_name='Sed_TU')
    pd.DataFrame(total_tus_sediment, columns=['Total Toxic Units (Sediment)']).to_excel(writer, sheet_name='Sed_Total_TU')

    # Write data and results for water
    water_data.to_excel(writer, sheet_name='Water Data')
    pd.Series(reference_values_water).to_excel(writer, sheet_name='Water Data', startrow=len(water_data) + 3, header=False)
    
    # PLI, Igeo, PI, and ΣTUs with shortened sheet names and proper column names
    pd.DataFrame(pli_water, columns=['PLI (Water)']).to_excel(writer, sheet_name='Wat_PLI')
    pd.DataFrame(igeo_water, columns=water_data.columns).to_excel(writer, sheet_name='Wat_Igeo')
    pd.DataFrame(pi_water, columns=water_data.columns).to_excel(writer, sheet_name='Wat_PI')
    pd.DataFrame(tus_water, columns=water_data.columns).to_excel(writer, sheet_name='Wat_TU')
    pd.DataFrame(total_tus_water, columns=['Total Toxic Units (Water)']).to_excel(writer, sheet_name='Wat_Total_TU')

# Output completion message
print("Final calculations completed and saved to 'calculated_indices_results.xlsx'.")
