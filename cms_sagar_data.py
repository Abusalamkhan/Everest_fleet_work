from hashlib import new
from tokenize import blank_re
import pygsheets #Importing python in google sheets
import pandas as pd #importing pandas
from pandas import Series,DataFrame
import datetime
from datetime import datetime, timedelta,date
import numpy as np
import datetime as dt





# gc = pygsheets.authorize(service_file='/Users/karan_19981/Desktop/Work/Everest_Fleet/Database_Sheets/client_secret.json')

# gc = pygsheets.authorize(service_file='/home/ubuntu/scripts/client_secret.json')

gc = pygsheets.authorize(service_file='client_secret.json')


year = int(input('Enter a year:'))
month = int(input('Enter a month:'))
day = int(input('Enter a day:'))



last_week_day = datetime(year, month, day)

print(last_week_day)

today = date.today()




next_day = last_week_day + timedelta(days = 1)

print(next_day)

car_master_sheet_mumbai = gc.open("Car Master Sheet")
cms_mumbai_recovery_tab = car_master_sheet_mumbai.worksheet_by_title("Recovery")
cms_mumbai_recovery_data = pd.DataFrame(cms_mumbai_recovery_tab.get_all_records())
cms_mumbai_recovery_data = cms_mumbai_recovery_data[['Date','ETMID','Amount','DM Name']]
cms_mumbai_recovery_data.rename(columns={"ETMID":"ETM",'DM Name':"Remarks"},inplace = True)
cms_mumbai_recovery_data['Type'] = 'RECOVERY'
print(cms_mumbai_recovery_data.head())
cms_mumbai_recovery_data = cms_mumbai_recovery_data[['Date','ETM','Amount','Remarks','Type']]
print(cms_mumbai_recovery_data.head())



cms_mumbai_penalty_tab = car_master_sheet_mumbai.worksheet_by_title("Penalty")
cms_mumbai_penalty_data = pd.DataFrame(cms_mumbai_penalty_tab.get_all_records())
cms_mumbai_penalty_data = cms_mumbai_penalty_data[['Date in Payout','ETM','Penalty','Fine Amount']]
cms_mumbai_penalty_data.rename(columns={"Date in Payout":"Date",'Penalty':"Remarks","Fine Amount":"Amount"},inplace = True)
cms_mumbai_penalty_data['Type'] = np.where((cms_mumbai_penalty_data['Remarks'] == "Without Intimation"), "UNSCHEDULED_LEAVES", "ACCIDENT")
print(cms_mumbai_penalty_data.head())




cms_mumbai_B2B_tab = car_master_sheet_mumbai.worksheet_by_title("B2B")
cms_mumbai_B2B_data = pd.DataFrame(cms_mumbai_B2B_tab.get_all_records())
cms_mumbai_B2B_data = cms_mumbai_B2B_data[['Date','ETMID','Duty','TotalDutyPayout','Fuel','Toll']]
cms_mumbai_B2B_data.rename(columns={"ETMID":"ETM",'Duty':"Remarks"},inplace = True)

cms_mumbai_B2B_duty = cms_mumbai_B2B_data[['Date','ETM','Remarks','TotalDutyPayout']]
cms_mumbai_B2B_duty['Type'] = 'B2B_DUTY'
cms_mumbai_B2B_duty.rename(columns={"TotalDutyPayout":"Amount"},inplace = True)

cms_mumbai_B2B_fuel = cms_mumbai_B2B_data[['Date','ETM','Remarks','Fuel']]
cms_mumbai_B2B_fuel['Type'] = 'B2B_FUEL'
cms_mumbai_B2B_fuel.rename(columns={"Fuel":"Amount"},inplace = True)


cms_mumbai_B2B_toll = cms_mumbai_B2B_data[['Date','ETM','Remarks','Toll']]
cms_mumbai_B2B_toll['Type'] = 'B2B_TOLL'
cms_mumbai_B2B_toll.rename(columns={"Toll":"Amount"},inplace = True)



cms_mumbai_rto_tab = car_master_sheet_mumbai.worksheet_by_title("RTO")
cms_mumbai_rto_data = pd.DataFrame(cms_mumbai_rto_tab.get_all_records())
cms_mumbai_rto_data = cms_mumbai_rto_data[['Date in Payout','ETM','Penalty','Fine Amount']]
cms_mumbai_rto_data.rename(columns={"Date in Payout":"Date",'Penalty':"Remarks","Fine Amount":"Amount"},inplace = True)
cms_mumbai_rto_data['Type'] = 'RTO_FINE'





cms_mumbai_adjustment_tab = car_master_sheet_mumbai.worksheet_by_title("Adjustments")
cms_mumbai_adjustment_data = pd.DataFrame(cms_mumbai_adjustment_tab.get_all_records())
cms_mumbai_adjustment_data = cms_mumbai_adjustment_data[['Date','ETM ID','Type','Remark','Amount']]
cms_mumbai_adjustment_data.rename(columns={"ETM ID":"ETM",'Remark':"Remarks","Type":"Test Type"},inplace = True)


cms_mumbai_adjustment_data['Amount'] = cms_mumbai_adjustment_data['Amount'].replace(',','', regex=True)



cms_mumbai_adjustment_data[['Amount']] = cms_mumbai_adjustment_data[['Amount']].apply(pd.to_numeric)

col         = 'Test Type'
col1 = 'Amount'
conditions  = [ cms_mumbai_adjustment_data[col].str.contains("fuel",case = False),cms_mumbai_adjustment_data[col].str.contains("refer",case = False), cms_mumbai_adjustment_data[col].str.contains("life",case = False), cms_mumbai_adjustment_data[col].str.contains("repair",case = False),cms_mumbai_adjustment_data[col].str.contains("pun",case = False),cms_mumbai_adjustment_data[col].str.contains("toll",case = False),cms_mumbai_adjustment_data[col].str.contains("Penalty",case = False),cms_mumbai_adjustment_data[col].str.contains("reversal",case = False),cms_mumbai_adjustment_data[col].str.contains("joining fee",case = False),cms_mumbai_adjustment_data[col1] >= 0,cms_mumbai_adjustment_data[col1] < 0 ]
choices     = [ "FUEL_ADJUSTMENT","DRIVER_REFERENCE", 'LIFETIME_INCENTIVE', 'REPAIRS','REPAIRS','TOLL','PENALTY_REVERSAL','PENALTY_REVERSAL','JOINING_FEE','OTHER_ADDITIONS','OTHER_DEDUCTIONS']
    
cms_mumbai_adjustment_data["Type"] = np.select(conditions, choices, default=np.nan)

cms_mumbai_adjustment_data = cms_mumbai_adjustment_data[['Date','ETM','Remarks','Amount','Type']]





cms_mumbai_amount_paid_tab = car_master_sheet_mumbai.worksheet_by_title("Amount Paid")
cms_mumbai_amount_paid_data = pd.DataFrame(cms_mumbai_amount_paid_tab.get_all_records())
cms_mumbai_amount_paid_data = cms_mumbai_amount_paid_data[['Date','ETM','Remarks','Amount']]
cms_mumbai_amount_paid_data['Type'] = 'BANK_TRANSFER'


final_mumbai_data = pd.concat([cms_mumbai_recovery_data, cms_mumbai_amount_paid_data,cms_mumbai_adjustment_data,cms_mumbai_rto_data,cms_mumbai_B2B_toll,cms_mumbai_B2B_fuel,cms_mumbai_B2B_duty,cms_mumbai_penalty_data],ignore_index = True)

final_mumbai_data['Date'] = pd.to_datetime(final_mumbai_data['Date'],dayfirst=True)


final_mumbai_data['start date'] = last_week_day
final_mumbai_data['end date'] = next_day

final_mumbai_data = final_mumbai_data.loc[(final_mumbai_data['start date'] <= final_mumbai_data['Date']) & (final_mumbai_data['end date'] > final_mumbai_data['Date'])]

final_mumbai_data['ETM_NEW'] = final_mumbai_data['ETM'].str.upper() 


final_mumbai_data = final_mumbai_data[['ETM_NEW','Amount','Type','Remarks','Date']]

final_mumbai_data.rename(columns={"ETM_NEW":"ETM"},inplace = True)

final_mumbai_data_first =  final_mumbai_data.groupby(['ETM','Type'],as_index = False).first()

final_mumbai_data_first.drop(['Amount'],axis = 1, inplace = True)

final_mumbai_data = final_mumbai_data[['ETM','Amount','Type']]

final_mumbai_data['Amount'] = final_mumbai_data['Amount'].replace(',','', regex=True)



final_mumbai_data[['Amount']] = final_mumbai_data[['Amount']].apply(pd.to_numeric)



final_mumbai_data_sum =  final_mumbai_data.groupby(['ETM','Type'],as_index = False).sum()


final_mumbai_data= final_mumbai_data_sum.merge(final_mumbai_data_first, on=["ETM","Type"])

final_mumbai_data = final_mumbai_data.loc[final_mumbai_data['Amount'] != 0]

final_mumbai_data = final_mumbai_data[['Date','ETM','Type','Amount','Remarks']]


cms_test = gc.open("testing")
final_result = cms_test.worksheet_by_title("cms")
final_result.set_dataframe(final_mumbai_data,'A1')