
import pandas as pd

debts = [
    {
        "monthly_payment": 10,
        "total_owed": 2000,
        "interest_rate": 0.15,
    },
    {
        "monthly_payment": 10,
        "total_owed": 3000,
        "interest_rate": 0.20,
    },
    {
        "monthly_payment": 10,
        "total_owed": 5000,
        "interest_rate": 0.25,
    },
    {
        "monthly_payment": 10,
        "total_owed": 10000,
        "interest_rate": 0.5,
    },
]

debt_df = pd.DataFrame(data = debts)

print(debt_df)
def snowball_method(debts, amount_put_towards_debts_monthly):
    res = {
        'month': [0],
        'total_remaining': [calc_total_debt_remaining(debts)],
        'interest_paid': [0],
    }
    print(res)
    debts = sorted(debts, key=lambda x: x["total_owed"])
    month = 0
    interest_paid = 0
    for debt in debts:
        monthly_amount_left_over = 0
        total_remaining = debt["total_owed"]
        while debt["total_owed"] > 0:
            month += 1
            # take away monthly amount
            remaining = debt['total_owed'] - amount_put_towards_debts_monthly - monthly_amount_left_over
            if remaining < 0:
                monthly_amount_left_over = abs(remaining)
            
            # add interest
            interest = debt['total_owed'] * (debt['interest_rate'] / 12)
            
            # append all the calculated_values
            res['total_remaining'].append(res['total_remaining'][-1] - monthly_amount_left_over)
            res['month'].append(month)
            res['interest_paid'].append(res['interest_paid'][-1] + interest)
            
def calc_total_debt_remaining(debts):
    total_debts = 0
    for i in debts:
        total_debts += i['total_owed']
    return total_debts

def add_interest_on_all_debts(debts):
    for i in debts:
        i['total_owed'] += round(i['total_owed'] * (i['interest_rate'] / 12))
    return debts
        
# snowball_method(debts, 500)
        
add_interest_on_all_debts(debts)
        
# want a df of the starting debts
# second df of the month, total_remaining, interest paid