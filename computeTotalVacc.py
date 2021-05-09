# Script to compute total vaccinated.
import pandas as pd
from scipy.stats import lognorm
import math
import numpy as np
import os
import sys

def statecode(statename):
    '''
    Returns state name from state code
    '''
    if statename == "Andhra Pradesh":
        return "AP"
    elif statename == "Andaman and Nicobar Islands":
        return "AN"
    elif statename == "Arunachal Pradesh":
        return "AR"
    elif statename == "Assam":
        return "AS"
    elif statename == "Bihar":
        return "BR"
    elif statename == "Chandigarh":
        return "CH"
    elif statename == "Chhattisgarh":
        return "CT"
    elif statename == "Dadra and Nagar Haveli and Daman and Diu":
        return "DD"
    elif statename == "Delhi":
        return "DL"
    elif statename == "Goa":
        return "GA"
    elif statename == "Gujarat":
        return "GJ"
    elif statename == "Haryana":
        return "HR"
    elif statename == "Himachal Pradesh":
        return "HP"
    elif statename == "Jharkhand":
        return "JH"
    elif statename == "Jammu and Kashmir":
        return "JK"
    elif statename == "Karnataka":
        return "KA"
    elif statename == "Kerala":
        return "KL"
    elif statename == "Ladakh":
        return "LA"
    elif statename == "Lakshadweep":
        return "LD"
    elif statename == "Madhya Pradesh":
        return "MP"
    elif statename == "Maharashtra":
        return "MH"
    elif statename == "Manipur":
        return "MN"
    elif statename == "Meghalaya":
        return "ML"
    elif statename == "Mizoram":
        return "MZ"
    elif statename == "Nagaland":
        return "NL"
    elif statename == "Odisha":
        return "OR"
    elif statename == "Punjab":
        return "PB"
    elif statename == "Puducherry":
        return "PY"
    elif statename == "Rajasthan":
        return "RJ"
    elif statename == "Sikkim":
        return "SK"
    elif statename == "Tamil Nadu":
        return "TN"
    elif statename == "Telangana":
        return "TG"
    elif statename == "Tripura":
        return "TR"
    elif statename == "Uttar Pradesh":
        return "UP"
    elif statename == "Uttarakhand":
        return "UT"
    elif statename == "West Bengal":
        return "WB"
    else:
        return statename

def statename(statecode):
    '''
    Returns state name from state code
    '''
    if statecode == "AP":
        return "Andhra Pradesh"
    elif statecode == "AN":
        return "Andaman and Nicobar Islands"
    elif statecode == "AR":
        return "Arunachal Pradesh"
    elif statecode == "AS":
        return "Assam"
    elif statecode == "BR":
        return "Bihar"
    elif statecode == "CH":
        return "Chandigarh"
    elif statecode == "CT":
        return "Chhattisgarh"
    elif statecode == "DD":
        return "Dadra and Nagar Haveli and Daman and Diu"
    elif statecode == "DL":
        return "Delhi"
    elif statecode == "GA":
        return "Goa"
    elif statecode == "GJ":
        return "Gujarat"
    elif statecode == "HR":
        return "Haryana"
    elif statecode == "HP":
        return "Himachal Pradesh"
    elif statecode == "JH":
        return "Jharkhand"
    elif statecode == "JK":
        return "Jammu and Kashmir"
    elif statecode == "KA":
        return "Karnataka"
    elif statecode == "KL":
        return "Kerala"
    elif statecode == "LA":
        return "Ladakh"
    elif statecode == "LD":
        return "Lakshadweep"
    elif statecode == "MP":
        return "Madhya Pradesh"
    elif statecode == "MH":
        return "Maharashtra"
    elif statecode == "MN":
        return "Manipur"
    elif statecode == "ML":
        return "Meghalaya"
    elif statecode == "MZ":
        return "Mizoram"
    elif statecode == "NL":
        return "Nagaland"
    elif statecode == "OR":
        return "Odisha"
    elif statecode == "PB":
        return "Punjab"
    elif statecode == "PY":
        return "Puducherry"
    elif statecode == "RJ":
        return "Rajasthan"
    elif statecode == "SK":
        return "Sikkim"
    elif statecode == "TN":
        return "Tamil Nadu"
    elif statecode == "TG":
        return "Telengana"
    elif statecode == "TR":
        return "Tripura"
    elif statecode == "UP":
        return "Uttar Pradesh"
    elif statecode == "UT":
        return "Uttarakhand"
    elif statecode == "WB":
        return "West Bengal"
    elif statecode == "UN":
        return "Miscellaneous"
    else:
        return statecode

vaccine_daily = pd.read_csv("vaccine_doses_statewise.csv").T #Have to transpose so that states are in columns and dates are in rows

date = input("\nEnter a date from"+ vaccine_daily.index[1] +"to"+ vaccine_daily.index[-1]+"\n(In the format DD/MM/YY, eg: 24/03/21): ")

vaccine_daily.columns = vaccine_daily.iloc[0]

vaccine_daily = vaccine_daily.drop(index='State')

vaccine_daily[statename("LD")] = vaccine_daily[statename("LD")]+vaccine_daily[statename("DD")]+vaccine_daily[statename("ML")]+vaccine_daily[statename("MZ")]+vaccine_daily[statename("NL")]+vaccine_daily[statename('UN')]

# Delete regions that we do not need
del vaccine_daily[statename("DD")]
del vaccine_daily[statename("ML")]
del vaccine_daily[statename("MZ")]
del vaccine_daily[statename("NL")]
del vaccine_daily[statename('UN')]
# Rename column TT as Total
vaccine_daily.rename(columns={"TT" : "Total"}, inplace=True)

columns_list = vaccine_daily.columns

vac_list = [0 for x in range(33)] # 32 states and 1 total. This is fixed in the C++ code.

date_index = vaccine_daily.index.get_loc(date)

for k, column in enumerate(columns_list):

        vac_list[k] = vaccine_daily.iloc[date_index, k]

vac_df = pd.DataFrame()
vac_df["State"] = [statecode(x) for x in columns_list]
vac_df["InitialVac"] = vac_list

vac_df.to_csv(date.replace('/','-') + '-vac_IC.data', sep=' ', index=False)
