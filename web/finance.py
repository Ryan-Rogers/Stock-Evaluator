import json
import math
import codecs
from alpha_vantage.timeseries import TimeSeries
from matplotlib import pyplot
from random import randint
from datetime import datetime
from datetime import timedelta
from time import time

key = ''

max_seed = 20
start_capital = 5000.00  # Dollars
period = 9999  # ~27 years
start_date = datetime.strptime('1/1/00', '%m/%d/%y')

operations = ['+', '-', '*', '/', '0']
options = ['5. volume', '4. close', '2. high', '1. open', '3. low']
date_format = '%Y-%m-%d'

historical_file = 'MSFT_history.json'
seeds_file = 'MSFT_seeds.json'


class Seed:
    def __init__(self, pregenerated=None):
        if pregenerated:
            self.length = len(pregenerated)
            self.__raw = pregenerated

        # Generating new seed
        else:
            self.length = randint(1, max_seed)
            self.__raw = list()
            self.__generate()

    def __generate(self):
        for _ in range(self.length):
            self.__raw.append(randint(0, max(len(operations), len(options))))

        return self.__raw

    def n(self, position=0):
        return self.__raw[position % self.length]

    def __n_of(self, position, source):
        return source[self.n(position) % len(source)]

    def n_operation(self, position=0):
        return self.__n_of(position, operations)

    def n_option(self, position=0):
        return self.__n_of(position, options)

    def __str__(self):
        return str(self.__raw)


def plot(symbol):
    data = TimeSeries(key=key, output_format='pandas')
    data, meta_data = data.get_monthly(symbol)
    data['close'].plot()
    pyplot.title(symbol)
    pyplot.show()
    

def get_data(symbol):
    data = TimeSeries(key=key, output_format='json')
    return data.get_daily(symbol, outputsize='full')


def perform(val1, operation, val2):
    if operation == '+':
        return float(val1) + float(val2)
    if operation == '-':
        return float(val1) - float(val2)
    if operation == '*':
        return float(val1) * float(val2)
    if operation == '/':
        return float(val1) / float(val2)
    if operation == '0':
        return 0.0


def calculate_seed(seed, debug):
    if str(seed) in seed_data and not debug:
        return seed_data[str(seed)]

    shares = 0
    current_capital = start_capital
    current_date = start_date

    # Processing seed over range
    for _ in range(period):
        current_date += timedelta(days=1)
        formatted_date = current_date.strftime(date_format)
        if formatted_date not in historical_data:
            continue

        # Calculating portfolio adjustment
        close = float(historical_data[formatted_date]['4. close'])
        adjustment = 0.0
        for i in range(seed.length):
            adjustment += perform(historical_data[formatted_date][seed.n_option(i)], seed.n_operation(i),
                                  historical_data[formatted_date][seed.n_option(i + 1)])
        adjustment = int(adjustment)

        # Adjustment over max, just buying max
        max_buy = int(math.floor(current_capital / close))
        if adjustment >= max_buy:
            new_shares = max_buy

        # Adjustment below currently owned, just selling all
        elif adjustment <= shares:
            new_shares = (shares * -1)

        # Adjustment between min and max
        else:
            new_shares = adjustment

        shares += new_shares
        current_capital -= (new_shares * close)
        if current_capital < 0:
            print "Somehow had negative capital, quitting"
            raise Exception

        if debug and new_shares:  # On change
            print "\n" + str(formatted_date)
            if new_shares > 0:
                print "Bought " + str(new_shares) + " at " + str(close) + " each"
            else:
                print "Sold " + str(abs(new_shares)) + " at " + str(close) + " each"
            print "Now at " + str(shares) + ", worth $" + str(close * shares)
            print "Have $" + str(current_capital) + " Cash"
            print "Total net worth is $" + str(current_capital + (close * shares))

    # Calculating percent profit
    results = {'percent_profit': (((shares * close) - start_capital + current_capital) / start_capital) * 100.0}
    seed_data[str(seed)] = results
    return results


if __name__ == '__main__':
    # Loading data
    with open(historical_file, 'r') as raw_json:
        historical_data = json.load(raw_json)
    with open(seeds_file, 'r') as raw_json:
        seed_data = json.load(raw_json)

    # Used for progress updates
    num_process = 5000
    percent_progress = float(num_process) / 100

    # Calculating seeds
    for q in range(num_process):
        seed_results = calculate_seed(Seed(), False)

        # Printing progress
        if q % percent_progress == 0:
            print str(int(time())) + " Progress: " + str(int(q / percent_progress)) + "%"
            with open(seeds_file, 'wb') as raw_json:
                json.dump(seed_data, codecs.getwriter('utf-8')(raw_json), ensure_ascii=False, sort_keys=True, indent=4)

    # Calculating highest seed
    max_profit = 0.0
    max_profit_seed = None
    for seed in seed_data:
        if seed_data[seed]["percent_profit"] > max_profit:
            max_profit = seed_data[seed]['percent_profit']
            max_profit_seed = seed
    print "\nMax Seed Profit: " + "%.1f" % max_profit + "%"
    print seed

    # Saving results
    with open(seeds_file, 'wb') as raw_json:
        json.dump(seed_data, codecs.getwriter('utf-8')(raw_json), ensure_ascii=False, sort_keys=True, indent=4)

    # TODO Reverse iteration over period to allow for calculating of specific dates, ex: the last 90 days

