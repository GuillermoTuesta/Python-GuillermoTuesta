import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import seaborn.objects as so
import plotly_express as px

sns.set_theme()
sns.set_style('white')
sns.set_context('talk')

infection_statistics_xls = pd.ExcelFile('Rådata/Folkhalsomyndigheten_Covid19.xlsx')
vaccination_statistics_xls = pd.ExcelFile('Rådata/Folkhalsomyndigheten_Covid19_Vaccine.xlsx')

veckodata_riket = pd.read_excel(infection_statistics_xls, 'Veckodata Riket')

date_column = [f'{year}v{week}' for year, week in zip(veckodata_riket.loc[:,'år'], veckodata_riket.loc[:,'veckonummer'])]
# Loop through columns 'year' and 'week' and append it as a string in the format 'YYYYvWW', such as '2020v06'. 
# Using zip() lets me loop through both columns at the same time.

veckodata_riket.insert(0, 'Vecka', date_column, True) # Insert newly created column.
veckodata_riket = veckodata_riket.drop(['år', 'veckonummer'], axis=1) # Remove the 2 columns that were merged.

subplot_veckodata_riket = sns.FacetGrid(veckodata_riket, )
# https://stackoverflow.com/questions/65855605/spacing-of-x-axis-label-in-seaborn-plot

#sns.lineplot(data=veckodata_riket, x='Vecka', y='Antal_avlidna_vecka')
#sns.lineplot(data=veckodata_riket, x='Vecka', y='Antal_fall_vecka') 




