# Celeries

We used data from the American Community Survey 5-Year Data in the states of California, New York, Washington, Florida, Texas, and Illinois for persons. We cleaned the data to use 5 parameters: state, sex, stem, marriage status, and total income.

### Training the Neural Net
We take in a number of features that are representative of income such as location, age, and occupation category.  We run a fully connected neural network with 3 hidden layers of sizes 100, 100, and 50 respectively using RELU activation.  We use the l2 norm for loss.

### House Calculations
House calculations are based off the assumption that the borrower spends 43% of his or her income towards housing.  These numbers are within Fannie Mae guidelines of below 45% and are a reasonable assumption for modeling the salaries of new graduates.

Expected Annual Income:  Expected salary
Average House Price:  Average house price for the selected city
Average Condo Price:  Average condo price for the selected city
Time to Buy a House:  Estimated number of years to save for a 20% down payment for a house
Time to Buy a Condo:  Estimated number of years to save for a 20% down payment for a condo
House Difficulty: Percentage of your income that will go towards purchasing a house in you selected city
Condo Difficulty:  Percentage of your income that will go towards purchasing a condo in you selected city