import math
#this is working as expected
def yearly_payment (house_price, interest, percent_down):
	c = interest/(1200.)
	return 12.*(house_price*(1. - percent_down/100.)) * ( (c * (1. + c) ** 360. ) / ( ((1.  + c ) **360.) - 1. ) )

def can_buy_house(income, col, house_price, interest, percent_down, 
	                        cant_afford_col, cant_afford_mor, can_afford_house, state):
	#checking if can afford col
	if income < col:
		cant_afford_col.append(state)
		return
	#calcing house payment, surplus after col, and savings
	house_payment = yearly_payment(house_price, interest, percent_down)
	savings = income - col - house_payment
	amount_over_col = income - col
	#checking if can afford house payment
	if savings < 0:
		cant_afford_mor.append(state)
		return
    #calcing savings values, percent income taken by h payment, and puting all relevant details in list
	percent_savings = (int)(100*(savings/income) + .5)
	years_to_save_down = (int)(house_price*(percent_down/100)/amount_over_col + .5)
	percent_h_payment = (int)(house_payment/income + .5)
	can_afford_house.append((state, years_to_save_down, percent_h_payment, percent_savings, savings))
	return

#takes in a dict of incomes for each state, dict of median house price,
#dict of cost of living (col), and list of state with names matching keys in dicts 
#returns 3 lists: places can't aford col, can't afford house payment, can afford house payment
# for can afford h payment list holds tuples with: 
# (state, years to make down payment, percent income to h payment, percent of income savings, dollar savings)
def generate_lists(incomes, col, house_prices, states):
     cant_afford = []
     cant_afford_hpay = []
     can_afford_hpay = []
     for state in states:
     	can_buy_house(incomes[state], col[state], house_prices[state], 4, 20, 
     		  cant_afford, cant_afford_hpay, can_afford_hpay, state)
     return (cant_afford, cant_afford_hpay, can_afford_hpay)

