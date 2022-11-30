import pandas as pd
import seaborn as sns
import seaborn.objects as so
import matplotlib.pyplot as plt

sns.set_theme()
sns.set_style('white')
sns.set_context('talk')
plt.figure(figsize=(8,8))

infection_statistics_xls = pd.ExcelFile('Rådata/Folkhalsomyndigheten_Covid19.xlsx')
vaccination_statistics_xls = pd.ExcelFile('Rådata/Folkhalsomyndigheten_Covid19_Vaccine.xlsx')

veckodata_riket = pd.read_excel(infection_statistics_xls, 'Veckodata Riket')
 
date_column = [f'{year}v{week}' for year, week in zip(veckodata_riket.loc[:,'år'], veckodata_riket.loc[:,'veckonummer'])]
# Loop through columns 'year' and 'week' and append it as a string in the format 'YYYYvWW', such as '2020v06'. 
# Using zip() lets me loop through both columns at the same time.

veckodata_riket.insert(0, 'Vecka', date_column, True) # Insert new column.
veckodata_riket = veckodata_riket.drop(['år', 'veckonummer'], axis=1) # Remove 2 columns that were merged.

sns.lineplot(veckodata_riket, x='Vecka', y='Antal_fall_vecka')
sns.lineplot(veckodata_riket, x='Vecka', y='Antal_avlidna_vecka')

veckodata_plot_xticks = veckodata_riket.index
plt.xticks(veckodata_plot_xticks[::10], rotation='vertical')

plt.show()