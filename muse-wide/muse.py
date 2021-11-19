import os
import numpy as np
import pandas as pd
from astropy.io import fits
from astropy.table import Table

temlines = Table.read('MW_44fields_emline_table_v1.0.fits', format='fits')
df_em = temlines.to_pandas()
str_columns = df_em.select_dtypes([object])
str_columns = str_columns.stack().str.decode("utf-8").unstack()
for col in str_columns:
    df_em[col] = str_columns[col]
df_sel = df_em[['UNIQUE_ID', 'IDENT', 'SN', 'F_3KRON', 'F_3KRON_ERR']]
# ONLY KEEP LYA
lya_em = df_sel[df_sel['IDENT'] == 'Lya']
lya_em = lya_em[lya_em['SN'] >= 5.5]

maintable = Table.read('MW_44fields_main_table_v1.0.fits', format='fits')
df_mt = maintable.to_pandas()
str_columns = df_mt.select_dtypes([object])
str_columns = str_columns.stack().str.decode("utf-8").unstack()
for col in str_columns:
    df_mt[col] = str_columns[col]
df_mt = df_mt[['UNIQUE_ID', 'FIELD_NAME', 'RA', 'DEC', 'Z', 'Z_ERR', 'SKELTON_ID', 'GUO_ID']]

lya_full = lya_em.merge(df_mt, on='UNIQUE_ID')
lya_full = lya_full[lya_full['SKELTON_ID']!=0]
lya_full = lya_full[['UNIQUE_ID', 'SKELTON_ID', 'GUO_ID', 'RA', 'DEC', 'SN', 'F_3KRON', 'F_3KRON_ERR', 'Z', 'Z_ERR']]
fluxes = lya_full['F_3KRON'].values
errors = lya_full['F_3KRON_ERR'].values

lya_full.to_csv('../muse-wide.csv', index=False)