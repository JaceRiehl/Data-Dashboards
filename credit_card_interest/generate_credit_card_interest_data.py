import csv
import pandas as pd

initial_princ = 1000
apr = 0.20
mininum_payment = 10
days_of_loan = 365
total_payed = 0
interest_payed = 0
principle_payed = 0
daily_interest_rate = apr/days_of_loan
# TODO: account for starting date and months of year
# TODO: run from terimal to input these numbers


princ_payed_log = []
total_payed_log = []
total_interest_log = []
total_principle_log = []
daily_interest_log = []
days = list(range(1,days_of_loan))
for i in range(1,days_of_loan):
    if i % 30 == 0:
        initial_princ = initial_princ - mininum_payment
        total_payed += mininum_payment
        
    interest = initial_princ * daily_interest_rate
    interest_payed += interest
    initial_princ += interest
    total_payed_log.append(round(total_payed, 2))
    total_interest_log.append(round(interest_payed, 2))
    total_principle_log.append(round(initial_princ, 2))
    daily_interest_log.append(round(interest, 2))
    
print(len(total_principle_log),len(daily_interest_log),len(total_interest_log),len(total_payed_log),len(days))
df_data = {
        'Day': days,
        'Principle': total_principle_log, 
        'Daily_interest': daily_interest_log,
        'Interest Payed': total_interest_log,
        'Total Payment': total_payed_log, 
    }

df = pd.DataFrame(data=df_data)
df["APR"] = apr * 100
df["Minimum Payment"] = mininum_payment
df.to_csv("credit_card_payment_data.csv", index=False)
