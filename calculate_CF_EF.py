import pandas as pd
# Load the sediment data from the provided Excel file
file_path = 'racun.xlsx'
# Load the sediment concentration data for metals and Fe
sediment_data = pd.read_excel(file_path, sheet_name='Sediment Data')
cf_calc = pd.DataFrame()
# Background values for the calculation
background_values = {
    'Zn (mg/kg)': 70,  # mg/kg
    'As (mg/kg)': 1.80,  # mg/kg
    'Hg (mg/kg)': 0.08,  # mg/kg
    'Cd (mg/kg)': 0.2,  # mg/kg
    'Cu (mg/kg)': 55,  # mg/kg
    'Fe (mg/kg)': 3.59,  # %
    'Pb (mg/kg)': 12.5,  # mg/kg
    'Ni (mg/kg)': 75  # mg/kg
}
print(sediment_data.columns)
# Function to calculate Contamination Factor (CF)
def calculate_cf(row, element):
    return row[element] / background_values[element]
# Function to calculate Enrichment Factor (EF)
def calculate_ef(row, element):
    fe_sample = row['Fe (mg/kg)']  # Fe value in the sample
    fe_background = background_values['Fe (mg/kg)']
    return (row[element] / background_values[element]) / (fe_sample / fe_background)
# Apply CF and EF calculations for As and Hg
cf_calc['CF_As'] = sediment_data.apply(calculate_cf, element='As (mg/kg)', axis=1)
cf_calc['CF_Hg'] = sediment_data.apply(calculate_cf, element='Hg (mg/kg)', axis=1)
cf_calc['CF_Zn'] = sediment_data.apply(calculate_cf, element='Zn (mg/kg)', axis=1)
cf_calc['CF_Cd'] = sediment_data.apply(calculate_cf, element='Cd (mg/kg)', axis=1)
cf_calc['CF_Cu'] = sediment_data.apply(calculate_cf, element='Cu (mg/kg)', axis=1)
cf_calc['CF_Fe'] = sediment_data.apply(calculate_cf, element='Fe (mg/kg)', axis=1)
cf_calc['CF_Pb'] = sediment_data.apply(calculate_cf, element='Pb (mg/kg)', axis=1)
cf_calc['CF_Ni'] = sediment_data.apply(calculate_cf, element='Ni (mg/kg)', axis=1)
# Calculate EF for all relevant metals
for element in ['Zn (mg/kg)', 'As (mg/kg)', 'Hg (mg/kg)', 'Cd (mg/kg)', 'Cu (mg/kg)', 'Pb (mg/kg)', 'Ni (mg/kg)']:
    cf_calc[f'EF_{element}'] = sediment_data.apply(calculate_ef, element=element, axis=1)
    
# Save the CF and EF results to a new Excel sheet

cf_calc.round(2)
output_file = 'cf_ef_results.xlsx'
cf_calc.to_excel(output_file, index=False)
output_file
