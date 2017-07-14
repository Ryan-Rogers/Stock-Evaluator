# !/usr/bin/python
import os.path
from yahoo_finance import Share

def menu():
    """ show menu """
    print ('\n')
    print (30 * '-')
    print ("   M A I N - M E N U")
    print (30 * '-')
    print ("1. Import Tickers (tickers.txt)")
    print ("2. Manual Input")
    print ("3. Run Analysis")
    print ("4. Exit program")
    print (30 * '-')
    try:
        selection = int(raw_input('Enter your choice [1-4] : '))
        options = {1: import_tickers, 2: manual_tickers, 3: run_analysis, 4: exit_program}
        options[selection]()
    except ValueError:
        print("Please enter only integers please!")
        exit()

def import_tickers():
    """import tickers from tickers.txt in working directory"""
    if os.path.isfile('tickers.txt') == True:
        with open('tickers.txt') as f:
            content = f.readlines()
        content = [x.strip() for x in content]
        print content
        print("import successful")
        f.close()
        return content
    else:
        print("no text file found")

def manual_tickers():
    """manually enter tickers"""
    print("Enter Tickers")

def run_analysis():
    """run analysis on tickers"""
    yahoo = Share('aapl')
    print yahoo.get_open()
    print yahoo.get_price()
    print yahoo.get_trade_datetime()

def exit_program():
    """exit program"""
    print("Exiting Program")
    exit()

if __name__ == '__main__':
    while True:
        menu()
