# !/usr/bin/python
import os.path
from yahoo_finance import Share
from time import sleep

ticker_list = list()
line_separator = '\n' + (26 * '-')


def import_tickers():
    """
    Imports the tickers from tickers.txt in working directory
    :return:
    """
    global ticker_list

    if not os.path.isfile('tickers.txt'):
        print("No text file found")
        print("Create a 'tickers.txt' in this directory1")
        return

    with open('tickers.txt') as tickers_file:
        tickers = tickers_file.readlines()
        tickers = [ticker.strip() for ticker in tickers]

        print tickers
        print("import successful")


def manual_tickers():
    """
    Manually add a new ticker
    :return:
    """
    global ticker_list
    ticker_list.append(raw_input('Enter a stock ticker : '))
    print("Ticker Entry Successful")


def run_analysis():
    """
    Run analysis on the current global ticker list
    :return:
    """
    global ticker_list

    if len(ticker_list) == 0:
        print("No stocks in current ticker list")
        return

    for ticker in ticker_list:
        stock = Share(ticker)

        print(line_separator)
        print("Name: " + str(stock.get_name()))
        print("Open: " + str(stock.get_open()))
        print("Price: " + str(stock.get_price()))
        # print("Time :" + str(stock.get_trade_datetime()))
        # print("Earnings Share :" + str(stock.get_earnings_share()))
        # print("EPS Estimate :" + str(stock.get_EPS_estimate_next_quarter()))
        print(line_separator)


def andrews_algo():
    """
    Various metrics for a given ticker
    :param tickers:
    :return:
    """
    global ticker_list

    for ticker in ticker_list:
        stock = Share(ticker)

        print(line_separator)
        print(stock.get_name())
        print("Current Price: " + str(stock.get_price()))

        # Dollar volume == momentum
        dollar_volume = float(stock.get_price()) * float(stock.get_volume())
        if dollar_volume > 20000000.0:
            print("High Trading Liquidity, dollar volume: " + num_to_short_text(dollar_volume))
        else:
            print("Low Trading Liquidity, dollar volume: " + num_to_short_text(dollar_volume))

        # PEG is apparently inaccurate need to implement checks/also check conditional logic
        peg = float(stock.get_price_earnings_growth_ratio())
        if peg > 1.5:
            print("Undervalued, Large Growth Potential, PEG ratio: " + str(peg))
        elif peg < 1:
            print("Overvalued, High Risk Potential, PEG ratio: " + str(peg))
        else:
            print("Fairly Priced, Low Growth Potential, PEG ratio: " + str(peg))

        # TODO: ROE (increasing ROE signals regular profit generation)
        # TODO: Beta value to determine volatility
        # TODO: Actual EPS vs next quarter estimated EPS (to predict imminent stock jump or crash)
        # TODO: Formula to calculate future theoretical earnings

        # Converting textual numbers to floats
        market_cap = short_text_to_float(stock.get_market_cap())
        if market_cap > 200000000000.0:
            print("Mega Cap")
        elif market_cap > 10000000000.0:
            print("Large Cap")
        elif market_cap > 2000000000.0:
            print("Mid Cap")
        elif market_cap > 300000000.0:
            print("Small Cap")
        elif market_cap > 50000000.0:
            print("Micro Cap")
        else:
            print("Nano Cap")

        print("Market Capitalization: " + num_to_short_text(market_cap))

        print(line_separator)


def num_to_short_text(num):
    if num > 1000000000000:
        return "%.2f" % (num / 1000000000000) + "T"

    if num > 1000000000:
        return "%.2f" % (num / 1000000000) + "B"

    if num > 1000000:
        return "%.2f" % (num / 1000000) + "M"

    # num is already short
    return "%.2f" % num


def short_text_to_float(raw_num):
    str_num = str(raw_num)

    if str_num.endswith('T'):
        return float(str_num.split('T')[0]) * 1000000000000

    if str_num.endswith('B'):
        return float(str_num.split('B')[0]) * 1000000000

    if str_num.endswith('M'):
        return float(str_num.split('M')[0]) * 1000000

    # str_num is already int
    return float(raw_num)

if __name__ == '__main__':
    print("Starting program")
    options = [import_tickers, manual_tickers, run_analysis, andrews_algo]

    while True:
        print(line_separator + "\n\tM A I N - M E N U" + line_separator)

        for option in options:
            print(str(options.index(option)) + ". " + option.__name__)

        print(line_separator)

        selection = int(raw_input('Enter your choice: '))

        if selection < len(options):
            options[selection]()
            sleep(2)

        else:
            print("Exiting program")
            exit()
