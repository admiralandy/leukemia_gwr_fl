# %%
import pandas as pd
import geopandas as gpd

data = pd.read_csv('E:\\fl_leuk\\health\\cc-est2023-agesex-12.csv')

# Calculate the total population for 0-15 years
age_0_15 = data['UNDER5_TOT'] + data['AGE513_TOT']
data['POP_0_15'] = age_0_15

age_65_plus = data['AGE65PLUS_TOT']
data['POP_65_PLUS'] = age_65_plus

# Select the geographic identifier columns and the new calculated columns
data['PCT_ATRISK'] = ((data['POP_0_15'] + data['POP_65_PLUS']) / data['POPESTIMATE'] * 100).round(2)
# Select the geographic identifier columns and the new calculated column
columns_to_keep = ['COUNTY', 'STNAME', 'CTYNAME', 'YEAR', 'PCT_ATRISK']
data = data[data['YEAR'] == 5]
data['CTYNAME'] = data['CTYNAME'].str.replace(' County', '')
result = data[columns_to_keep]
print(result.iloc[:, :5].head())
# Save the result to a new CSV file
result.to_csv('E:\\fl_leuk\\health\\atriskpop.csv', index=False)


# %%
data2 = pd.read_csv('E:\\fl_leuk\\health\\obese.csv')
data3 = pd.read_csv('E:\\fl_leuk\\health\\pct_smokers.csv')
data2.info()
data3.info()

geodata  = gpd.read_file('E:\\fl_leuk\\leukemia_fl_updated.shp')
geodata.info()


# %%
obesity_data = pd.read_csv('E:\\fl_leuk\\health\\obese.csv')
smoking_data = pd.read_csv('E:\\fl_leuk\\health\\pct_smokers.csv')

# Load GeoDataFrame
geodata = gpd.read_file('E:\\fl_leuk\\leukemia_fl_updated.shp')

# Merge Percent columns with GeoDataFrame
geodata = geodata.merge(obesity_data[['Name', 'obs_pct']], left_on='NAME', right_on='Name', how='left')
geodata = geodata.merge(smoking_data[['Name', 'Percent_smokers']], left_on='NAME', right_on='Name', how='left')
# Convert COUNTY in both datasets to string for consistent data type
result['COUNTY'] = result['COUNTY'].astype(str)
geodata['COUNTY'] = geodata['COUNTY'].astype(str)
# Merge PCT_ATRISK with GeoDataFrame
geodata = geodata.merge(result[['CTYNAME', 'PCT_ATRISK']], left_on='NAME', right_on='CTYNAME', how='left')



# Drop duplicate 'Name' columns after merge
geodata = geodata.drop(columns=['Name_x', 'Name_y','CTYNAME','PERCENT_AD'], errors='ignore')

# Save updated GeoDataFrame


# %%
data4 = pd.read_csv('E:\\fl_leuk\\hydrocarb_area_frac.csv')
data5 = pd.read_csv('E:\\fl_leuk\\pesticide_area_frac1.csv')

geodata['FIPS'] = geodata['FIPS'].astype(str)
data4['fips'] = data4['fips'].astype(str)
data5['fips'] = data5['fips'].astype(str)

geodata['FIPS'] = geodata['FIPS'].str.zfill(3)
data4['fips'] = data4['fips'].str.zfill(3)
data5['fips'] = data5['fips'].str.zfill(3)
# Merge hydrocarbon percentage
geodata = geodata.merge(data5[['fips', 'pesticide_pct']], 
                        left_on='FIPS', 
                        right_on='fips', 
                        how='left')

geodata = geodata.merge(data4[['fips', 'hydrocarbon_percentage']], 
                        left_on='FIPS', 
                        right_on='fips', 
                        how='left')
geodata.rename(columns={'hydrocarbon_percentage': 'hydro_pct'}, inplace=True)
# Optionally, drop the redundant fips columns if you want
geodata.drop(columns=['fips_x', 'fips_y'], inplace=True)
# Drop duplicate fips columns if created
geodata = geodata.drop(columns=['fips_x', 'fips_y'], errors='ignore')
geodata.to_file('E:\\fl_leuk\\leukemia_fl.shp')
geodata.head(n=10)


