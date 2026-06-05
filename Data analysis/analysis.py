import os
import pyreadr
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from icecream import ic
import statistics

path = os.path.join('Data analysis','netdiffuseR-master', 'data', 'brfarmers.rdata')
data = pyreadr.read_r(path)['brfarmers']

data_df: pd.DataFrame = pd.DataFrame.from_dict(data)

print(list(data_df.columns))

contacts = data_df['contact']
contacts= contacts.dropna()
ic(contacts)

print('average contacts: ', sum(contacts)/len(contacts))
print('contacts standard deviation: ', statistics.stdev(contacts))
npcontacts = np.array(contacts)
ic(npcontacts)
contacts_hist = np.histogram(npcontacts, bins=max(contacts))

plt.plot(contacts_hist[0])
plt.title('contact histogram')
plt.show()


toa_list = np.array(data['toa'])
hist = np.histogram(toa_list, bins=20)[0]
cumulative_toa = np.cumsum(hist)
print(cumulative_toa)
plt.show()

fig, ax = plt.subplots(1, 2, figsize=(20, 10))
ax[0].bar(np.linspace(1, len(hist), num=len(hist)), hist, width=1)
ax[1].plot(np.linspace(1, len(cumulative_toa), num=len(cumulative_toa)), cumulative_toa)
ic(list(cumulative_toa))
plt.title('adoption over time')
plt.show()

""" df = pd.DataFrame.from_dict(data, columns=data.keys())
print(df) """