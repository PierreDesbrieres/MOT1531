# -*- coding: utf-8 -*-
"""
Created on Wed Mar 16 09:31:08 2016

@author: Pierre
"""

import random

WEEKS = 52                # We focus on a panel of 52 weeks available (a year)
DESTINATIONS = 10         # We focus on 10 different destinations
OFFERS_DESTINATIONS_1 = 5 # We created 3 types of accommodation : cheap
OFFERS_DESTINATIONS_2 = 3 # intermediate
OFFERS_DESTINATIONS_3 = 2 # expensive. These exist for all destinations
OFFERS_NB = DESTINATIONS * (OFFERS_DESTINATIONS_1 + OFFERS_DESTINATIONS_2 +\
            OFFERS_DESTINATIONS_3)
PRICE = 50 # This is the base price we calculate our prices with
THRESHOLD_1 = 100  # If the utility of the customer is below this threshold he is interested in that offer
THRESHOLD_2 = 2000 # If the utility is above this threshold the customer leaves
# If the utility is between the two, the customer goes through the loop and changes his wishes
PROCESS_TIME = 1 # The time it takes to be processed
FREQUENCY_CUSTOMERS = [0.04, 0.06, 0.08, 0.10, 0.13, 0.17, 0.21, 0.21] # The frequency of customers through the day (hours)
NB_CUSTOMERS = 500 # The number of customers we used for our simulation
DISTRIBUTION_CUSTOMERS = [int(x * NB_CUSTOMERS) for x in FREQUENCY_CUSTOMERS] # We calculate the number of customers per hour
REJECT_LOOP_COEFF = 0.5 # The downside of going through the reject loop
OTHER_LOOP_COEFF = 0.05 # The downside of going through the changing wishes loop
WEEK_COEFF = 4          # Theses coefficients were
TIME_COEFF = 6          # calibrated during the simulations
DESTINATION_COEFF = 10  # so that globally each criteria
PRICE_COEFF = 0.5       # gets the average same importance
# (Despite the different orders of magnitude)


# The following is just the construction of every offer possible
# The result is a table like this (just not in the same order):
# Dest | Week | Time | Level of acc. | Acc. nb | Price | Available |
#   1  |  1   |  1   |       1       |    1    | price |    True   |
#   1  |  1   |  2   |       1       |    1    | price |    True   |
#   1  |  1   |  3   |       1       |    1    | price |    True   | 
# ...
#   1  |  1   |  52  |       1       |    1    | price |    True   |
#   1  |  2   |  1   |       1       |    1    | price |    True   |
# ...
#   1  |  52  |  1   |       1       |    1    | price |    True   |
#   1  |  1   |  1   |       1       |    2    | price |    True   |
# ...
#   1  |  52  |  1   |       1       |    5    | price |    True   |
#   1  |  1   |  1   |       2       |    1    | price |    True   |
# ...
#   1  |  52  |  1   |       3       |    2    | price |    True   |
#   2  |  1   |  1   |       1       |    1    | price |    True   |

# We just repertoriate every offer, even if some are not compatible
# (the first two for instance)

OFFERS = []
for i in range(DESTINATIONS):
    i_bis = i + 1
    for j in range(OFFERS_DESTINATIONS_1):
        price = int(max((i_bis) / 4, 1) * (0.8 + random.random() * 0.4) * 1 *\
                PRICE)
        for k in range(WEEKS):
            k_bis = k + 1
            time_max = WEEKS - k
            for l in range(time_max):
                offer = [k_bis, l + 1, i_bis, 1, j + 1, price * (l + 1), True]
                OFFERS.append(offer)
    for j in range(OFFERS_DESTINATIONS_2):
        price = int(max((i_bis) / 4, 1) * (0.8 + random.random() * 0.4) * 2 *\
                PRICE)
        for k in range(WEEKS):
            k_bis = k + 1
            time_max = WEEKS - k
            for l in range(time_max):
                offer = [k_bis, l + 1, i_bis, 2, j + 1, price * (l + 1), True]
                OFFERS.append(offer)
    for j in range(OFFERS_DESTINATIONS_3):
        price = int(max((i_bis) / 4, 1) * (0.8 + random.random() * 0.4) * 3 *\
                PRICE)
        for k in range(WEEKS):
            k_bis = k + 1
            time_max = WEEKS - k
            for l in range(time_max):
                offer = [k_bis, l + 1, i_bis, 3, j + 1, price * (l + 1), True]
                OFFERS.append(offer)
