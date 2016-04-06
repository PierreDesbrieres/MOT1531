# -*- coding: utf-8 -*-

import Globals # We use global variables and random methods
import random

def calculus(customer, offer):  # This part calculates the utility for a customer with an offer
    u_week = int(abs(customer.week - offer[0]) * customer.k_week * Globals.WEEK_COEFF *\
             (1 + customer.reject_loop * Globals.REJECT_LOOP_COEFF) *\
             (1 + customer.other_loop * Globals.OTHER_LOOP_COEFF))
    u_time = int(abs(customer.time - offer[1]) * customer.k_time * Globals.DESTINATION_COEFF *\
             (1 + customer.reject_loop * Globals.REJECT_LOOP_COEFF) *\
             (1 + customer.other_loop * Globals.OTHER_LOOP_COEFF))
    u_destination = int(abs(customer.destination - offer[2]) * customer.k_destination *\
                    Globals.DESTINATION_COEFF *\
                    (1 + customer.reject_loop * Globals.REJECT_LOOP_COEFF) *\
                    (1 + customer.other_loop * Globals.OTHER_LOOP_COEFF))
    u_price = int(abs(offer[5] - customer.price) * customer.k_price * Globals.PRICE_COEFF *\
              (1 + customer.reject_loop * Globals.REJECT_LOOP_COEFF) *\
              (1 + customer.other_loop * Globals.OTHER_LOOP_COEFF))
    u_total = [u_week, u_time, u_destination, u_price] # For each part the calculus is based on the absolute 
    return(u_total)                                    # difference between the wish and the offer
    
def best_offer_index(customer):
    utilities = []
    utilities_split = []
    for i in range(len(Globals.OFFERS)):                     # For every offer
        if Globals.OFFERS[i][6]:                             # If the offer is available
            u_temp = calculus(customer, Globals.OFFERS[i])   # We calculate the utility
            utilities.append(sum(u_temp))                    # We store those utilities
            utilities_split.append(u_temp)                   # in two temporary lists
        else:                                                # If the offer isn't 
            utilities.append(12000)                          # We put 12 000 arbitrarily
            utilities_split.append([3000, 3000, 3000, 3000]) # and this arbitrary split
    u = min(utilities)        # We then take the minimum offer
    k = utilities.index(u)    # The index of this offer or its number in our offers table
    v = utilities_split[k]    # And the split of utilities
    customer.store.append([v, customer.other_loop, customer.reject_loop]) # We store it all in the store
    return([k,u,v]) # And we return the index, the utility and the split of the best offer
    
def fill_arg(frequency, split): # This is just a method to go from hourly data to minutely data randomly
    f = [0 for i in range(int(len(frequency) * split))]
    for i in range(len(frequency)):
        w = frequency[i]
        if w > split:
            while w != 0:
                for j in range(split):
                    if w > 0:
                        f[i*split + j] += 1
                        w -= 1
        else:
            for j in range(w):
                k = split
                while k == split:
                    k = int(split*random.random())
                f[i*split + k] += 1
    return f

def intercept(offer_1, offer_2):  # This method tells whether two offers intercept each other or not
    if offer_2[0] <= offer_1[0] <= offer_2[0] + offer_2[1]: # If the 1 starts between the 2 is over
        return True
    elif offer_1[0] <= offer_2[0] <= offer_1[0] + offer_1[1]: # Or the opposite
        return True
    else:
        return False # If they don't we return false
            
def booking(offer_index): # This is the booking method which makes all the offers intercepting the one taken by the customer not available
    k_up = 0 # We take advantage of the way the table is built here: we take a temporary index
    offer = Globals.OFFERS[offer_index] # We store the offer wanted by the customer
    while offer_index - k_up >= 0 and Globals.OFFERS[offer_index - k_up][2:4] == offer[2:4]: # While we can and the offers match in terms of destination, level and acc. nb
        if intercept(Globals.OFFERS[offer_index - k_up],Globals.OFFERS[offer_index]): # If the two offers intercept
            Globals.OFFERS[offer_index - k_up][6] = False # The offer is no longer available
        k_up += 1 # We go up the table this way
    k_down = 1 # We do the same thing while going down the table after that
    while offer_index + k_down < len(Globals.OFFERS) and Globals.OFFERS[offer_index + k_down][2:4] == offer[2:4]:
        if intercept(Globals.OFFERS[offer_index + k_down],Globals.OFFERS[offer_index]):
            Globals.OFFERS[offer_index + k_down][6] = False
        k_down += 1