
import pandas as pd

debts_snowball = [
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
        "interest_rate": 0.3,
    },
]

debts_avalance = [
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
        "interest_rate": 0.3,
    },
]

debt_df = pd.DataFrame(data = debts_snowball)

print(debt_df)
def payoff_debt(debts, amount_put_towards_debts_monthly, snowball_method = True):
    print(debts)
    res = {
        'month': [0],
        'total_remaining': [calc_total_debt_remaining(debts)],
        'interest_paid': [0],
    }
    if snowball_method:
        debts = sorted(debts, key=lambda x: x["total_owed"])
    else:
        debts = sorted(debts, key=lambda x: x["interest_rate"])[::-1]
    month = 0
    
    for i in range(len(debts)):
        monthly_amount_left_over = 0
        total_remaining = debts[i]["total_owed"]
        while debts[i]["total_owed"] > 0:
            # add interest
            interest = add_interest_on_all_debts(debts)
            
            month += 1
            # take away monthly amount
            remaining = debts[i]['total_owed'] - amount_put_towards_debts_monthly - monthly_amount_left_over
            if remaining < 0:
                monthly_amount_left_over = abs(remaining)
            
            
            # append all the calculated_values
            res['total_remaining'].append(calc_total_debt_remaining(debts))
            res['month'].append(month)
            res['interest_paid'].append(res['interest_paid'][-1] + interest)
            
            # reduce debt
            if debts[i]['total_owed'] - amount_put_towards_debts_monthly < 0:
                debts[i]['total_owed'] = 0
            else:
                debts[i]['total_owed'] = debts[i]['total_owed'] - amount_put_towards_debts_monthly
    return res

def calc_total_debt_remaining(debts):
    total_debts = 0
    for i in debts:
        total_debts += i['total_owed']
    return total_debts

def add_interest_on_all_debts(debts):
    total_interest_added = 0
    for i in debts:
        interest = round(i['total_owed'] * (i['interest_rate'] / 12))
        i['total_owed'] += interest
        total_interest_added += interest
    return interest
        

print(payoff_debt(debts_snowball, 1000, True))
print("\n\n\n\n\n")
print(payoff_debt(debts_avalance, 1000, False))