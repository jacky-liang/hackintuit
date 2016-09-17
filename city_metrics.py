SFR_PRICES = {'sf': 801880, 'sd': 535727, 'la':548553, 'se':441305, 'au':268904,'ny':1551019}
CON_PRICES = {'sf': 716936, 'sd': 395414, 'la':557365, 'se':300265, 'au':207049,'ny':1104667}

def city_metrics(state_salaries):
    cities = ['sf', 'sd', 'la', 'se', 'au','ny']

    def get_metrics(city):
        sfr_price = SFR_PRICES[city]
        con_price = CON_PRICES[city]

        city_dict = dict()

        city_dict['sfr_price'] = sfr_price
        city_dict['con_price'] = con_price
        city_dict['avg_salary'] = state_salaries[city]

        return city_dict

    # Dictinoary of results
    d = dict()

    for city in cities:
        d[city] = get_metrics(city)

    return d

ans = city_metrics({'sf': 801880, 'sd': 535727, 'la':548553, 'se':441305, 'au':268904,'ny':1551019})
print ans