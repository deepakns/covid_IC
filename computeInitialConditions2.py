import pandas as pd
from scipy.stats import lognorm
import math


def log_normal_pdf(x):
    '''
    Function to calculate PDF of a log-normal distribution
    with mu=1.62 and sigma=0.42 at a given x
    '''
    return lognorm.pdf(x, 0.42, scale = math.exp(1.62))



# Read csv data
state_wise_daily = pd.read_csv("state_wise_daily.csv")

# Get date as input from user
date = input("\nEnter a date from"+ state_wise_daily.head(1)["Date"].values[0] +"to"+ state_wise_daily.tail(1)["Date"].values[0]+"\n(In the format DD-Mon-YY, eg: 24-Mar-20): ")

# Combine the columns Status and Date to form a column named Daily_Status
state_wise_daily['Daily_Status'] = state_wise_daily["Status"] + "-" + state_wise_daily["Date"]

# Delete the columns Status and Date
del state_wise_daily['Date']
del state_wise_daily['Status']
del state_wise_daily['Date_YMD']

state_wise_daily["LD"] = state_wise_daily["LD"]+state_wise_daily["DN"]+state_wise_daily["DD"]+state_wise_daily["ML"]+state_wise_daily["MZ"]+state_wise_daily["NL"]+state_wise_daily['UN']

# Delete regions that we do not need
del state_wise_daily["DN"]
del state_wise_daily["DD"]
del state_wise_daily["ML"]
del state_wise_daily["MZ"]
del state_wise_daily["NL"]
del state_wise_daily['UN']
# Rename column TT as Total
state_wise_daily.rename(columns={"TT" : "Total"}, inplace=True)

# Move the column Total to the end
column_total = state_wise_daily.pop("Total")
state_wise_daily["Total"] = column_total

# A list of elements from Daily_Status
date_status_list = state_wise_daily["Daily_Status"]
date_status_list_rec = state_wise_daily["Daily_Status"]
date_status_list_des = state_wise_daily["Daily_Status"]

# Filter out recovered and deceased cases from the list
date_status_list = [date_status for date_status in date_status_list if "Confirmed" in date_status]
date_status_list_rec = [date_status for date_status in date_status_list_rec if "Recovered" in date_status]
date_status_list_des = [date_status for date_status in date_status_list_des if "Deceased" in date_status]
print(len(date_status_list))
print(len(date_status_list_rec))
print(len(date_status_list_des))
# Set the column Daily_Status as the index of the DataFrame
state_wise_daily.set_index("Daily_Status", inplace = True)

# List of column names
columns_list = state_wise_daily.columns

# List for storing data to be written into a file
initial_conditions_list = [0 for x in range(33)]
total_list = [0 for x in range(33)]
recovered_list = [0 for x in range(33)]
deceased_list = [0 for x in range(33)]

# Position corresponding to initial date in date_status_list
date_index = date_status_list.index("Confirmed-"+date)+1
print(date_index)
# Compute and fill required initial conditions data into dict
for k, column in enumerate(columns_list):
    initial_conditions_list[k] = 0
    for ii in range(0,date_index):
        initial_conditions_list[k] = initial_conditions_list[k] + state_wise_daily.loc[date_status_list[ii], column] - state_wise_daily.loc[date_status_list_rec[ii], column] - state_wise_daily.loc[date_status_list_des[ii], column]
        total_list[k] = total_list[k] + state_wise_daily.loc[date_status_list_rec[ii], column] + state_wise_daily.loc[date_status_list_des[ii], column]
        recovered_list[k] = recovered_list[k] + state_wise_daily.loc[date_status_list_rec[ii], column]
        deceased_list[k] = deceased_list[k] + state_wise_daily.loc[date_status_list_des[ii], column]
    for i, date_status in enumerate(date_status_list[date_index:date_index + 14]):
        initial_conditions_list[k] += log_normal_pdf(i+1)*state_wise_daily.loc[date_status, column]
    initial_conditions_list[k] = round(initial_conditions_list[k])

# Pandas DataFrame to store initial conditions
initial_conditions_df = pd.DataFrame()

initial_conditions_df["State"] = columns_list
initial_conditions_df["Initial"] = initial_conditions_list

total_df = pd.DataFrame()
total_df["State"] = columns_list
total_df["Initial"] = total_list

recovered_df = pd.DataFrame()
recovered_df["State"] = columns_list
recovered_df["Initial"] = recovered_list

deceased_df = pd.DataFrame()
deceased_df["State"] = columns_list
deceased_df["Initial"] = deceased_list

# Write initial conditions DataFrame to csv file
initial_conditions_df.to_csv(date + '-initial2.data', sep=' ', index=False)

total_df.to_csv(date + '-initial_R.data', sep=' ', index=False) # total removed

recovered_df.to_csv(date + '-initial_recovered.data', sep=' ', index=False) # total recovered

deceased_df.to_csv(date + '-initial_deceased.data', sep=' ', index=False)


print("\nData written into " + date + '-initial2.data\n')
