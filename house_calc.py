import math
#this is working as expected
def yearly_payment (house_price, interest, percent_down):
	c = interest/(1200)
	return 12*(house_price*(1 - percent_down/100)) * ( (c * (1 + c) ** 360 ) / ( ((1 + c ) **360) - 1 ) )

def trunc_hunds(val):
	return ((float)((int)(val*100 + .5)))/100
def can_buy_house(income, col, house_price, interest, percent_down, 
	                        cant_afford_col, cant_afford_mor, can_afford_house, city):
	#checking if can afford col
	if income < col:
		cant_afford_col.append(city)
		return
	#calcing house payment, surplus after col, and savings
	house_payment = trunc_hunds(yearly_payment(house_price, interest, percent_down))
	savings = trunc_hunds(income - col - house_payment)
	amount_over_col = income - col
	#checking if can afford house payment
	if savings < 0:
		cant_afford_mor.append(city)
		return
    #calcing savings values, percent income taken by h payment, and puting all relevant details in list
	percent_savings = trunc_hunds(100*(savings/income))
	down_payment = trunc_hunds(house_price*(percent_down/100))
	years_to_save_down = trunc_hunds(down_payment/amount_over_col)
	percent_h_payment = trunc_hunds(100*house_payment/income) 
	can_afford_house.append((city, down_payment, years_to_save_down, house_payment, percent_h_payment, savings, percent_savings))
	return

#takes in a dict of incomes for each state, dict of median house price,
#dict of cost of living (col), and list of state with names matching keys in dicts 
#returns 3 lists: places can't aford col, can't afford house payment, can afford house payment
# for can afford h payment list holds tuples with: 
# (state, years to make down payment, house payment, percent income to h payment, percent of income savings, dollar savings)
def generate_lists(incomes, col, house_prices, cities):
     cant_afford = []
     cant_afford_hpay = []
     can_afford_hpay = []
     for city in cities:
     	state = cities[city]
     	can_buy_house(income[state], col[city], house_prices[city], 4, 20, 
     		  cant_afford, cant_afford_hpay, can_afford_hpay, city)
     return (cant_afford, cant_afford_hpay, can_afford_hpay)


#tests
#cities = {'LA': 'CA', 'Atlanta': 'GA', 'Miami': 'FL'}
#house_prices = {'LA': 100000, 'Atlanta': 50000, 'Miami': 10000}
#col = {'LA': 5000, 'Atlanta': 5000, 'Miami': 5000}
#income = {'CA': 5200, 'GA': 4000, 'FL': 6000}