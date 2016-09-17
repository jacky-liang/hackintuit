SFR_PRICES = {'sf': 801880, 'sd': 535727, 'la':548553, 'se':441305, 'au':268904,'ny':1551019}
CON_PRICES = {'sf': 716936, 'sd': 395414, 'la':557365, 'se':300265, 'au':207049,'ny':1104667}
COST_OF_LIVING = {'sf': 1093.61*12, 'sd': 879.52*12, 'la':923.21*12, 'se':999.50*12, 'au':789.09*12,'ny':1166.64*12}

def time_to_afford(salary, price):
    #Based on federal Guidelines
    DEBT_TO_INCOME_RATIO = 0.43
    DOWN_PAYMENT_PERCENT = 0.2

    max_annual_contribution = DEBT_TO_INCOME_RATIO * salary
    down_payment = price * DOWN_PAYMENT_PERCENT

    return down_payment / max_annual_contribution

def debt_to_income(salary, price):
    monthly_payments = float(price) / 200000 * 1000
    annual_payments = 12 * monthly_payments
    return annual_payments / salary * 100

############################################################################################

def get_metrics(city, salary):
    sfr_price = SFR_PRICES[city]
    con_price = CON_PRICES[city]
    expected_salary = salary

    city_dict = dict()

    city_dict['sfr_price'] = sfr_price
    city_dict['con_price'] = con_price
    city_dict['time_to_house'] = time_to_afford(expected_salary, sfr_price)
    city_dict['time_to_con'] = time_to_afford(expected_salary, con_price)
    city_dict['expected_salary'] = expected_salary
    city_dict['house_hardship'] = debt_to_income(expected_salary, sfr_price)
    city_dict['con_hardship'] = debt_to_income(expected_salary, con_price)

    return city_dict

def city_metrics(state_salaries):
    cities = ['sf', 'sd', 'la', 'se', 'au','ny']
    city_to_state = {'sf':'CA', 'sd':'CA', 'la':'CA', 'se':'WA', 'au':'TX','ny':'NY'}

    def get_metrics(city):
        sfr_price = SFR_PRICES[city]
        con_price = CON_PRICES[city]
        expected_salary = state_salaries[city_to_state[city]]

        city_dict = dict()

        city_dict['sfr_price'] = sfr_price
        city_dict['con_price'] = con_price
        city_dict['time_to_house'] = time_to_afford(expected_salary, sfr_price)
        city_dict['time_to_con'] = time_to_afford(expected_salary, con_price)
        city_dict['expected_salary'] = expected_salary
        city_dict['house_hardship'] = debt_to_income(expected_salary, sfr_price)
        city_dict['con_hardship'] = debt_to_income(expected_salary, con_price)

        return city_dict

    # Dictionary of results
    d = dict()

    for city in cities:
        d[city] = get_metrics(city)

    return d

ans = city_metrics({'CA': 100000, 'WA': 90000, 'TX':800000, 'NY':120000})
print ans['sd']['time_to_house']