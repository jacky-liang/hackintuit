import IPython

from house_calc import generate_lists

if __name__ == '__main__':
    states = ['CA','WA']
    incomes = {'CA':90000,'WA':70000}
    col = {'CA':20000,'WA':10000}
    house_prices = {'CA':1.2e6, 'WA':0.7e6}

    a, b, c = generate_lists(incomes, col, house_prices, states)
    IPython.embed()
    exit(0)