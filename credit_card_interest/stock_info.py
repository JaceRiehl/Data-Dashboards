import yfinance as yf
import pandas as pd
from currency_converter import CurrencyConverter as cc
import requests


def calculate_total_money_in_sp500(term_in_months, amount_invested_monthly, average_dividends_percentage = 0):
    sp = yf.Ticker("^GSPC")
    amount_of_shares = 0
    amount_invested = 0
    dividends = 0
    
    if average_dividends_percentage > 1:
        average_dividends_percentage = average_dividends_percentage / 100
    shares = {
        "Shares_Owned": [], 
        "Dollar_Amount": [],
        "Date": [],
        "Stock_Price": [],
        "Amount_Invested": [],
        }
    
    for i, row in sp.history(period=str(term_in_months)+"mo", interval="1mo").iterrows():
        dividends += 1
        if dividends % 3 == 0 and average_dividends_percentage != 0:
            amount_of_shares += (amount_of_shares * row["High"] * average_dividends_percentage)/row["High"]
        
        amount_of_shares += amount_invested_monthly / row["High"]
        amount_invested += amount_invested_monthly
        shares["Shares_Owned"].append(amount_of_shares)
        shares["Dollar_Amount"].append(amount_of_shares * row["High"])
        shares["Date"].append(pd.to_datetime(i).date())
        shares["Stock_Price"].append(row["High"])
        shares["Amount_Invested"].append(amount_invested)
        
    return shares
    
def create_csv_of_sp500_investment(term_in_months, amount_invested_monthly, filepath, dividend_percentage_quarterly = 0):
    shares_timeperiod_calculated = calculate_total_money_in_sp500(term_in_months, amount_invested_monthly, dividend_percentage_quarterly)
    pd.DataFrame(data=shares_timeperiod_calculated).to_csv(filepath,index=False)
    

create_csv_of_sp500_investment(240, 500, "sp500_invested_over_20_years.csv")    
create_csv_of_sp500_investment(240, 1000, "sp1000_invested_over_20_years.csv")     

create_csv_of_sp500_investment(240, 500,"sp500_invested_over_20_years_dividends_reinvested.csv", 0.00375)    
create_csv_of_sp500_investment(240, 1000,"sp1000_invested_over_20_years_dividends_reinvested.csv", 0.00375)

create_csv_of_sp500_investment(360, 500,"sp500_invested_over_30_years_dividends_reinvested.csv", 0.00375)    
create_csv_of_sp500_investment(360, 1000,"sp1000_invested_over_30_years_dividends_reinvested.csv", 0.00375)      

sp = yf.Ticker("vfv.to")

sp.history(period="12mo").to_csv("vfv_stock_price.csv")

c = cc()
current_cad_conv = c.convert(1, 'USD', 'CAD')
current_cad_to_us_conv = c.convert(1, 'CAD', 'USD')

conv_df = pd.DataFrame(data={
        "USD to CAD": [current_cad_conv], 
        "CAD to USD": [current_cad_to_us_conv]
    })

conv_df.to_csv("current_cad_conversions.csv")

# response = requests.get("https://www.bankofcanada.ca/valet/lists/groups/json")

# boc_resp = response.json()




# boc_df = pd.DataFrame(data=boc_resp).to_csv("boc.csv")

# print(boc_df)