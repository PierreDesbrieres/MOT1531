# -*- coding: utf-8 -*-

import random  # Random library used in the programming
import Globals # We also use a lot of global variables explained in the global part

class Customer():          # This class represents a customer
    def __init__(self):    # This defines how customers are created
        self.k_week = (0.5 + random.random())   # These parameters are the relative  
        self.k_time = (0.5 + random.random())   # importance the customer gives to the week, 
        self.k_price = (0.5 + random.random())  # the time, the price or the destination
        self.k_destination = (0.5 + random.random()) * Globals.DESTINATION_COEFF
        self.week = 1 + int(random.random()*Globals.WEEKS) # The week of departure wanted is random
        temp = random.random()                                                    # We added another step
        if temp < 0.7:                                                            # for the intitialisation
            self.time = 1 + int(random.random()*min(3,Globals.WEEKS - self.week)) # of the time wanted for the
        else:                                                                     # holidays to match a more accurate
            self.time = 1 + int(random.random()*(Globals.WEEKS - self.week))      # distribution (more than 70% less than 3 weeks)
        self.destination = 1 + int(random.random()*Globals.DESTINATIONS) # The destination wanted is random
        self.price = int(Globals.PRICE * (0.5 + random.random()) *\
                     (self.destination / 4) * self.time * (0.5 + random.random())) # Price depends on the time and a richness factor
        self.wish = [self.week, self.time, self.destination, self.price] # The wish is th combination of all that
        self.reject_loop = 0 # This counter counts the number of times a customer went through the reject loop
        self.other_loop = 0  # Same counter but for the loop of changing their wishes
        self.time_proc = 0   # Used to know what time the customer starts being processed
        self.store = []      # Used to store each time the utility each offer offered had (not relevant)
        
    def modif(self, time):                                                         # This method is used when the customer 
        self.week = 1 + int(random.random()*Globals.WEEKS*0.99)                    # goes through the other loop and changes 
        self.time = 1 + int(random.random()*(Globals.WEEKS - self.week)*0.99)      # his wishes but not his parameters
        self.destination = 1 + int(random.random()*Globals.DESTINATIONS*0.99)      
        self.price = int(Globals.PRICE * (0.5 + random.random()) *\
                     (self.destination / 4) * self.time * (0.5 + random.random()))
        self.wish = [self.week, self.time, self.destination, self.price]
        self.time_proc = time                                                      # The customer has to wait another process time
        self.other_loop += 1                                                       # We increment the counter here
        