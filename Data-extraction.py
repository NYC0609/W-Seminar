import pandas as pd
import requests
import numpy as np

# Fetch the data.
df = pd.read_csv("https://ourworldindata.org/grapher/technology-adoption-by-households-in-the-united-states.csv?v=1&csvType=full&useColumnShortNames=true", storage_options = {'User-Agent': 'Our World In Data data fetch/1.0'})

print(df.head)

refrigerator_df = df[df['entity'] == 'Refrigerator']
print(refrigerator_df)
percentage_list = np.array(list(refrigerator_df[refrigerator_df.columns[2]]))
fractions_list = percentage_list/100
fractions_rounded = [round(i, 4) for i in fractions_list]
print(fractions_rounded)