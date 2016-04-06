# -*- coding: utf-8 -*-

import Classes
import Globals
import Methods

def main():
    
    #Initialisation
    
    nb_cust_time = Methods.fill_arg(Globals.DISTRIBUTION_CUSTOMERS, 60) # This list know each minute how many customers arrive
    customers = []                                                      # This is the future list of customers
    for i in range(Globals.NB_CUSTOMERS):
        customers.append(Classes.Customer())                            # This is how the list is filled
    cust_index = []               # This list stores the indexes of the customers who are present
    offers_index = []             # This list stores the indexes of the offers who are presentes
    offers_completed = 0          # This counter increases everytime an offer is completed    
    offers_refused = 0            # This counter increases everytime an offer is refused and a customer leaves
    first_loop_counter = 0        # This counter counts the number of times all the customers go throught the loop change of wish
    second_loop_counter = 0       # This counter counts the number of times all the customers go throught the loop booking unavailable
    satisfaction_temp = []        # This list stores the utility of the customers who are present (with the offers they have)
    satisfaction_temp_split = []  # This list stores the split of the previous utility (destination, week, time and price)
    satisfaction_finale = [0 for i in range(len(customers))]       # This list stores the utility the customers leave the agency with
    satisfaction_finale_split = [0 for i in range(len(customers))] # Same for the split
    step_cust = 0  # This step allows us to know which is the next customer from the customer list to show up
    time = 0       # This is just a timer
    
    while time < (len(nb_cust_time) + 10) or cust_index != []:  # While there are customers remaining in the shop or outside
        
        
        if time < len(nb_cust_time):       # If there are still new customers to come
            new_custs = nb_cust_time[time] # The new number of customers arriving in the agency is givent by the list
        else:
            new_custs = 0
            
        if new_custs != 0:                                                 # For every new customer
            for i in range(new_custs):
                customers[step_cust].time_proc = time                      # We intialize their time_proc to the actual time
                cust_index.append(step_cust)                               # We store their index in the appropriate list
                [k, u, v] = Methods.best_offer_index(customers[step_cust]) # We give them the best offer
                offers_index.append(k)                                     # and store the characteristics
                satisfaction_temp.append(u)                                # of this offer in the
                satisfaction_temp_split.append(v)                          # corresponding lists
                step_cust += 1                                             # Then we increment the customer index for the next one
                
        if cust_index != []:          # If there are people in the store
            pop_list = []             # This will be explained later
            for i in range(len(cust_index)):  # For every customer in the store
                wait = time - customers[cust_index[i]].time_pro  # We calculate how long they have been waited
                if wait >= Globals.PROCESS_TIME:                 # If that time is greater than the process time they are processed
# We then check the satisfaction of the customers to be processed to determine the rest of the process
                    if satisfaction_temp[i] > Globals.THRESHOLD_2: # If the utility is too big they will leave                                     
                        satisfaction_finale[cust_index[i]] = satisfaction_temp[i]             # We store their final utility
                        satisfaction_finale_split[cust_index[i]] = satisfaction_temp_split[i] # and the split
                        pop_list.append(i)  # We add to the pop list their number
                        offers_refused += 1 # We increase the number of offers refused
                    elif satisfaction_temp[i] > Globals.THRESHOLD_1: # The elif means we are between the two thresholds
                        first_loop_counter += 1                                        # We are into the first loop
                        customers[cust_index[i]].modif(time)                           # We change the wishes (see Classes)
                        [k, u, v] = Methods.best_offer_index(customers[cust_index[i]]) # We change the stored values with a new offer
                        offers_index[i] = k
                        satisfaction_temp[i] = u
                        satisfaction_temp_split[i] = v 
                    else: # The only remaining possibility is we are below the smallest threshold
                        if Globals.OFFERS[offers_index[i]][6]: # If the offer is available
                            Methods.booking(offers_index[i])   # We book the corresponding offer
                            offers_completed += 1              # We have one more offer completed
                            satisfaction_finale[cust_index[i]] = satisfaction_temp[i]             # We can store the final utility
                            satisfaction_finale_split[cust_index[i]] = satisfaction_temp_split[i] # and the split
                            pop_list.append(i) # We add to the pop list the number of the customer
                        else: # If the offer is no longer available
                            customers[cust_index[i]].reject_loop += 1 # We go through the reject loop but don't change the wishes
                            [k, u, v] = Methods.best_offer_index(customers[cust_index[i]]) # The customer gets a new best offer
                            offers_index[i] = k                        # We store the new values corresponding to this customer
                            satisfaction_temp[i] = u
                            satisfaction_temp_split[i] = v
                            customers[cust_index[i]].time_proc = time  # and reset the waiting time                    
                            second_loop_counter += 1                   # Finally we increase the second loop counter
            if pop_list != []:                         # The pop list is more of a technical Python issue actually
                p = 0                                  # The only purpose of it is to remove the customers who are leaving the
                for i in pop_list:                     # agency (whether they leave with an offer or not) from the temporary lists
                    cust_index.pop(i - p)              # that represent the characteristics of the cutomers who are present
                    offers_index.pop(i - p)
                    satisfaction_temp.pop(i - p)
                    satisfaction_temp_split.pop(i - p)
                    p += 1
                pop_list = []
        time += 1                                      # Once everything is treated, the timer increases and the loop begins once more

    # From here the simulation is actually over
        
    loops = []  # Used as a check to control if the code works : not actually used here       
    first_loop_nb = 0    # We will count the number of people who went through the changing loop
    second_loop_nb = 0   # And the number of those who went through the reject loop
    for i in range(len(customers)):
        loops.append(customers[i].store)
        if customers[i].other_loop != 0:
            first_loop_nb += 1
        if customers[i].reject_loop != 0:
            second_loop_nb += 1
            
    # We print the results we are interested in to be able to copy them for future use        
    print("Number of potential offers : "+str(len(Globals.OFFERS)))
    print("Number of customers : "+str(Globals.NB_CUSTOMERS))
    print("Offers completed : "+str(offers_completed))
    print("Customers not served : "+str(offers_refused))
    av_ut = sum(satisfaction_finale) // len(satisfaction_finale)
    print("Average utility : "+str(av_ut))
    print("Number of first loops : "+str(first_loop_counter))
    print("Number of customers through first loop : "+str(first_loop_nb))
    print("Number of second loops : "+str(second_loop_counter))
    print("Number of customers through second loop : "+str(second_loop_nb))