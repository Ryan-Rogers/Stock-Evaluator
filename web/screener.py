# !/usr/bin/python
import os.path
from yahoo_finance import Share
ticker_list = []

def menu():
    """ show menu """
    print ('\n')
    print (30 * '-')
    print ("   M A I N - M E N U")
    print (30 * '-')
    print ("1. Import Tickers (tickers.txt)")
    print ("2. Manual Input")
    print ("3. Run Analysis")
    print ("4. Andrew's Algo")
    print ("5. Exit Program")
    print (30 * '-')
    #try:
    selection = int(raw_input('Enter your choice [1-5] : '))
    options = {1: import_tickers, 2: manual_tickers, 3: run_analysis, 4: andrews_algo, 5: exit_program}
    options[selection]()
    #except ValueError:
    #    print("Please enter only integers please!")
    #    exit()


def import_tickers():
    """import tickers from tickers.txt in working directory"""
    global ticker_list
    if os.path.isfile('tickers.txt') == True:
        with open('tickers.txt') as f:
            ticker_list = f.readlines()
        ticker_list = [x.strip() for x in ticker_list]
        print ticker_list
        print("import successful")
        f.close()
        #return content
    else:
        print("no text file found")

def manual_tickers():
    """manually enter tickers"""
    global ticker_list
    ticker_list.append(raw_input('Enter a stock ticker : '))
    print("Ticker Entry Successful")

def run_analysis():
    """run analysis on tickers"""
    global ticker_list
    for x in ticker_list:
        yahoo = Share(x)
        print(5 * '-----')
        print(yahoo.get_name())
        print(yahoo.get_open())
        print(yahoo.get_price())
        print(yahoo.get_trade_datetime())
        print(5 * '-----')
        print('\n')

def andrews_algo():
    """various metrics for a given ticker"""
    global ticker_list
    for x in ticker_list:
        yahoo = Share(x)
        print(5 * '-----')
        print(yahoo.get_name())
        print("Current Price: " + str(yahoo.get_price()))
        dollar_volume = float(yahoo.get_price())*float(yahoo.get_volume())
        if dollar_volume > 20000000.0:
            print("High Trading Liquidity, dollar volume: $" + str(dollar_volume)) #larger dollar volume = more momentum
        else:
            print("Low Trading Liquidity, dollar volume: $" + str(dollar_volume))
        peg = float(yahoo.get_price_earnings_growth_ratio()) #PEG is apparently inaccurate need to implement checks/also check conditional logic
        if peg > 1.5:
            print("Undervalued, Large Growth Potential, PEG ratio: " + str(peg))
        elif peg >= 1.0 and peg < 1.4:
            print ("Fairly Priced, Low Growth Potential, PEG ratio: " + str(peg))
        elif peg < 1:
            print ("Overvalued, High Risk Potential, PEG ratio: " + str(peg))

        #need ROE, increasing ROE signals regular profit generation

        #need to get beta value to determine volatility

        #actual EPS vs next quarter estimated EPS - predict imminent stock jump or crash

        #find the formula to calculate future theoretical earnings

        # market_cap = float(yahoo.get_market_cap())
        # if market_cap > 200000000000.0:
        #     print("Mega Cap, Market Capitalization: " + str(market_cap))
        # elif market_cap > 10000000000.0 and market_cap < 200000000000.0:
        #     print("Large Cap, Market Capitalization: " + str(market_cap))
        # elif market_cap > 2000000000.0 and market_cap < 10000000000.0:
        #     print("Mid Cap, Market Capitalization: " + str(market_cap))
        # elif market_cap > 300000000.0 and market_cap < 2000000000.0:
        #     print("Small Cap, Market Capitalization: " + str(market_cap))
        # elif market_cap > 50000000.0 and market_cap < 300000000.0:
        #     print("Micro Cap, Market Capitalization: " + str(market_cap))
        # elif market_cap < 50000000.0:
        #     print("Nano Cap, Market Capitalization: " + str(market_cap))
        print(5 * '-----')
        print('\n')

def exit_program():
    """exit program"""
    print("Exiting Program")
    exit()

if __name__ == '__main__':
    # yahoo = Share('OHI')
    # print(yahoo.get_earnings_share())
    # print(yahoo.get_EPS_estimate_next_quarter())
    while True:
        menu()
