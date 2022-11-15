import pandas as pd
import seaborn as sns
import seaborn.objects as so

sns.set_theme()
sns.set_style('white')
sns.set_context('talk')

infection_statistics_xls = pd.ExcelFile('Rådata/Folkhalsomyndigheten_Covid19.xlsx')
vaccination_statistics_xls = pd.ExcelFile('Rådata/Folkhalsomyndigheten_Covid19_Vaccine.xlsx')

veckodata_riket = pd.read_excel(infection_statistics_xls, 'Veckodata Riket')

date_column = []
for year, week in zip(veckodata_riket.loc[:,'år'], veckodata_riket.loc[:,'veckonummer']):
    date_column.append(f'{year}v{week}')
 
date_column = [f'{year}v{week}' for year, week in zip(veckodata_riket.loc[:,'år'], veckodata_riket.loc[:,'veckonummer'])]
# Loop through columns 'year' and 'week' and append it as a string in the format 'YYYYvWW', such as '2020v06'. 
# Using zip() lets me loop through both columns at the same time.

veckodata_riket.insert(0, 'Vecka', date_column, True) # Insert new column.
veckodata_riket = veckodata_riket.drop(['år', 'veckonummer'], axis=1) # Remove 2 columns that were merged.

veckodata_plot = so.Plot(veckodata_riket, 'Vecka', 'Antal_fall_vecka').add(so.Line())

veckodata_plot.show()