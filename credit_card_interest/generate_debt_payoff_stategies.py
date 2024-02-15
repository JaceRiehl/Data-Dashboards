
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

def payoff_debt(debts, amount_put_towards_debts_monthly, snowball_method = True):
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
        while debts[i]["total_owed"] > 0:
            month += 1
            
            # add interest
            interest = add_interest_on_all_debts(debts)
            
            # pay the monthly amounts on every debt
            print(amount_put_towards_debts_monthly)
            amount_left_over_after_minimum_payments = pay_minimum_payments(debts, amount_put_towards_debts_monthly)
            print(amount_left_over_after_minimum_payments)
            # take away monthly amount
            remaining = debts[i]['total_owed'] - amount_left_over_after_minimum_payments - monthly_amount_left_over
            if remaining < 0:
                monthly_amount_left_over = abs(remaining)
            
            # append all the calculated_values
            res['total_remaining'].append(max(calc_total_debt_remaining(debts)-amount_left_over_after_minimum_payments, 0))
            res['month'].append(month)
            res['interest_paid'].append(res['interest_paid'][-1] + interest)
            
            # reduce debt
            if debts[i]['total_owed'] - amount_left_over_after_minimum_payments < 0:
                debts[i]['total_owed'] = 0
            else:
                debts[i]['total_owed'] = debts[i]['total_owed'] - amount_left_over_after_minimum_payments
        print(debts)
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

def pay_minimum_payments(debts, monthly_amount):
    leftover = monthly_amount
    for debt in debts:
        if debt['total_owed'] > 0:
            debt['total_owed'] -= debt['monthly_payment'] 
            leftover -= debt['monthly_payment']
    return leftover
    
        

snowball_df = pd.DataFrame(data=payoff_debt(debts_snowball, 1000, True))
avalance_df = pd.DataFrame(data=payoff_debt(debts_avalance, 1000, False))


debt_df.to_csv("initial_debts.csv",index=False)
snowball_df.to_csv("snowball_debt.csv",index=False)
avalance_df.to_csv("avalance_debt.csv",index=False)