
import pandas as pd

def payoff_debt(debts, amount_put_towards_debts_monthly, snowball_method = True):
    res = {
        'month': [0],
        'total_remaining': [calc_total_debt_remaining(debts)],
        'interest_paid': [0],
    }
    
    debts = sort_debts_by_payoff_method(debts, snowball_method)
    month = 0
    
    for i in range(len(debts)):
        monthly_amount_left_over = 0
        while debts[i]["total_owed"] > 0:
            month += 1
            
            # add interest
            interest = add_interest_on_all_debts(debts)
            
            # pay the monthly amounts on every debt
            amount_left_over_after_minimum_payments = pay_minimum_payments(debts, amount_put_towards_debts_monthly)
            
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
    return res

def sort_debts_by_payoff_method(debts, snowball_method):
    if snowball_method:
        debts = sorted(debts, key=lambda x: x["total_owed"])
    else:
        debts = sorted(debts, key=lambda x: x["interest_rate"])[::-1]
    return debts
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
    return total_interest_added

def pay_minimum_payments(debts, monthly_amount):
    leftover = monthly_amount
    for debt in debts:
        if debt['total_owed'] > 0:
            debt['total_owed'] -= debt['monthly_payment'] 
            leftover -= debt['monthly_payment']
    return leftover
    
def read_debt_data(filename):
    data = pd.read_csv(filename)
    data_dict = data.to_dict(orient='records')
    return data_dict
        
debts_snowball = read_debt_data("initial_debts.csv")
debts_avalance = read_debt_data("initial_debts.csv")

snowball_df = pd.DataFrame(data=payoff_debt(debts_snowball, 1000, True))
avalance_df = pd.DataFrame(data=payoff_debt(debts_avalance, 1000, False))

snowball_df.to_csv("snowball_debt.csv",index=False)
avalance_df.to_csv("avalance_debt.csv",index=False)