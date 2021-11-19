import os
import re
import numpy as np
import pandas as pd

data = np.genfromtxt('grecco-z3.8.cat.dat', dtype=str)
f = open('grecco-z3.8.cat.dat', 'r')
f.readline()
header = f.readline()
headers = header.split()
headers.pop(0)
headers.pop(26)
for i in range(len(headers)):
    if '.' in headers[i]:
        cut = headers[i].find('.')
        cut += 1
        headers[i] = headers[i][cut:]

df = pd.DataFrame(data, columns=headers)
df[headers[4:]] = df[headers[4:]].apply(pd.to_numeric, errors='coerce')

def convert_id(id):
    nmbr = re.sub('[^0-9]', '', id)
    return nmbr

df['ID'] = df['ID'].apply(convert_id)
df = df[df['Lya_SN[sigmas]'] >= 5.5]

df.to_csv('../grecco.csv', index=False)
