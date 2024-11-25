import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the sediment and water data
file_path_1 = 'racun.xlsx'
file_path_2 = 'corrected_nemerow_pollution_index_results.xlsx'

# Read the data, excluding the 'Id' column
sediment_igeo = pd.read_excel(file_path_1, sheet_name='Sed_Igeo').drop(columns='Id.')
sediment_pi = pd.read_excel(file_path_1, sheet_name='Sed_PI').drop(columns='Id.')
water_igeo = pd.read_excel(file_path_1, sheet_name='Wat_Igeo').drop(columns='Id.')
water_pi = pd.read_excel(file_path_1, sheet_name='Wat_PI').drop(columns='Id.')

# ---------------------------------------------------------------
# Table Classification and Creation Functions
# ---------------------------------------------------------------
def classify_igeo(value):
    if value < 0:
        return 'Igeo < 0'
    elif 0 <= value < 1:
        return '0 <= Igeo < 1'
    elif 1 <= value < 2:
        return '1 <= Igeo < 2'
    elif 2 <= value < 3:
        return '2 <= Igeo < 3'
    elif 3 <= value < 4:
        return '3 <= Igeo < 4'
    elif 4 <= value < 5:
        return '4 <= Igeo < 5'
    else:
        return 'Igeo >= 5'

def classify_pi(value):
    if value < 1:
        return 'PI < 1'
    elif 1 <= value < 2:
        return '1 <= PI < 2'
    elif 2 <= value < 3:
        return '2 <= PI < 3'
    elif 3 <= value < 5:
        return '3 <= PI < 5'
    else:
        return 'PI >= 5'

def classify_pin(value):
    if value < 0.7:
        return 'PIN < 0.7'
    elif 0.7 <= value < 1:
        return '0.7 <= PIN < 1'
    elif 1 <= value < 2:
        return '1 <= PIN < 2'
    elif 2 <= value < 3:
        return '2 <= PIN < 3'
    else:
        return 'PIN >= 3'

# Create percentage tables function
def create_percentage_table(data, categories):
    table = data.apply(pd.Series.value_counts, normalize=True).fillna(0) * 100
    for category in categories:
        if category not in table.index:
            table.loc[category] = [0] * len(table.columns) # Add missing categories with 0% values
    return table.reindex(categories).fillna(0) # Ensure the categories are in correct order

# ---------------------------------------------------------------
# Igeo and PI Classification and Tables for Sediment and Water
# ---------------------------------------------------------------
sediment_igeo_classified = sediment_igeo.map(classify_igeo)
water_igeo_classified = water_igeo.map(classify_igeo)
sediment_pi_classified = sediment_pi.map(classify_pi)
water_pi_classified = water_pi.map(classify_pi)

categories_igeo = ['Igeo < 0', '0 <= Igeo < 1', '1 <= Igeo < 2', '2 <= Igeo < 3', '3 <= Igeo < 4', '4 <= Igeo < 5', 'Igeo >= 5']
categories_pi = ['PI < 1', '1 <= PI < 2', '2 <= PI < 3', '3 <= PI < 5', 'PI >= 5']
categories_pin = ['PIN < 0.7', '0.7 <= PIN < 1', '1 <= PIN < 2', '2 <= PIN < 3', 'PIN >= 3']

table_29_sediment = create_percentage_table(sediment_igeo_classified, categories_igeo)
table_29_water = create_percentage_table(water_igeo_classified, categories_igeo)
table_30_sediment = create_percentage_table(sediment_pi_classified, categories_pi)
table_30_water = create_percentage_table(water_pi_classified, categories_pi)
# PIN Data
pin_data = pd.read_excel(file_path_2)
pin_classified = pin_data.map(classify_pin)
print(pin_classified)
table_32_pin = create_percentage_table(pin_classified, categories_pin) # Assuming PIN uses similar categories as PI

# ---------------------------------------------------------------
# Save all tables to Excel
# ---------------------------------------------------------------
with pd.ExcelWriter('pollution_classification_tables_final.xlsx') as writer:
    table_29_sediment.to_excel(writer, sheet_name='Table 29 - Igeo Sediment')
    table_29_water.to_excel(writer, sheet_name='Table 29 - Igeo Water')
    table_30_sediment.to_excel(writer, sheet_name='Table 30 - PI Sediment')
    table_30_water.to_excel(writer, sheet_name='Table 30 - PI Water')
    table_32_pin.to_excel(writer, sheet_name='Table 32 - PIN Classification')
