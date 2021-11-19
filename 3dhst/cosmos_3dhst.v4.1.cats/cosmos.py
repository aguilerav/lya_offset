import os
import numpy as np
import pandas as pd
from astropy.io import fits
from astropy.table import Table
from uncertainties import ufloat


data = np.genfromtxt('Catalog/cosmos_3dhst.v4.1.cat')
file = open('Catalog/cosmos_3dhst.v4.1.cat', 'r')
header = file.readline()
header = header.split()
header.pop(0)
df_cat = pd.DataFrame(data, columns=header)

df_cat.drop(['x', 'y', 'faper_F160W', 'eaper_F160W', 'faper_F140W',
                'eaper_F140W', 'tot_cor', 'wmin_ground', 'wmin_hst',
                'wmin_irac', 'wmin_wfc3', 'z_spec', 'star_flag', 'kron_radius',
                'a_image', 'b_image', 'theta_J2000', 'class_star', 'flux_radius',
                'fwhm_image', 'flags', 'IRAC1_contam', 'IRAC2_contam',
                'IRAC3_contam', 'IRAC4_contam', 'contam_flag', 'f140w_flag',
                'use_phot', 'near_star', 'nexp_f125w', 'nexp_f140w', 'nexp_f160w'], axis=1, inplace=True)

drop_columns = [df_cat.columns.to_numpy()[i] for i in range(len(df_cat.columns.to_numpy())) if 'w_' in df_cat.columns.to_numpy()[i]]
df_cat.drop(drop_columns, axis=1, inplace=True)

#CONVERT AB TO FNU
def AB_to_Fnu(mag, mag_err):
    AB = ufloat(mag, mag_err)
    Fnu = 10**((25-AB)/2.5)
    Fnu = Fnu * 10**(-29.44)
    return (Fnu.n, Fnu.s)

filters = [col for col in df_cat.columns.to_numpy() if 'f_' in col]
errs = [col for col in df_cat.columns.to_numpy() if 'e_' in col]

df_cat.to_csv('../../3dhst_cosmos.csv', index=False)