'''
Created on Jul 23, 2013

@author: Mike Gloudemans

An algorithm for the Brilliance Hunger Games on August 18, 2013.

'''

round_results = []
my_reputation = 0
hunting_mode = False
start_storing_results = False

def hunt_choices(round_number, current_food, current_reputation, m,  player_reputations):
    # The main routine that plays each individual round.
    
    # Declare all global variables used in the function
    global my_reputation     # Store info on reputation in a global variable for use in the hunt_outcomes function.
    my_reputation = current_reputation
    global round_results
    global hunting_mode
    
    num_opponents = len(player_reputations)
    
    if num_opponents == 1:
        # It's probably a bad idea to hunt if there are only two players left, because then
        # the opponent can always beat me by slacking. If I slack, then I should to have
        # at least a 50% chance of winning at this point (in the worst case, my opponent slacks every
        # time too, and then whoever was initially in the lead will ultimately win.)
        return ['s']
    
    ### For the first 20 rounds, just maintain a reputation close to 0.5.
    if round_number <= 20:
        hunt_decisions = ['s'] * (num_opponents / 2) + ['h'] * ( (num_opponents / 2) + num_opponents % 2)
        return hunt_decisions
    else:
        # After the first 20 rounds, it's time to start keeping track of some data!
        global start_storing_results
        start_storing_results = True
        
    ### After the first 20 rounds have passed, slowly tweak my reputation every few rounds and see
    ### how this affects other players' decisions of whether or not to hunt against me.
    
    # Every 14 rounds, determine whether my reputation is moving in the right direction, and 
    # adjust behavior accordingly.
    
    if len(round_results) == 14:
        recent_reputations = [item[0] for item in round_results]
        recent_hunt_percents = [item[1] for item in round_results]
        
        # Compute the change in my reputation and the change in the percentage of people that
        # hunted against me during in the last 14 rounds.
                
        # Compute average reputation during first and second halves of last 14 rounds
        initial_reputation = sum(recent_reputations[0:7]) / 7   
        final_reputation = sum(recent_reputations[7:]) / 7
        delta_reputation = final_reputation - initial_reputation
        
        # Compute percentage of people the hunted against me during first and second halves of last 14 rounds
        initial_hunt_percent = sum(recent_hunt_percents[0:7]) / 7
        final_hunt_percent = sum(recent_hunt_percents[7:]) / 7
        delta_hunt_percent = final_hunt_percent - initial_hunt_percent
        
        # Determine whether I'm moving my reputation in the correct direction.
        
        if (delta_reputation / 3) < delta_hunt_percent:
            # The increase/decrease in the percentage of people that hunted against me is sufficient 
            # to justify the amount of extra hunting that I'll have to do to maintain this level of
            # reputation. Keep adjusting my reputation in the same direction.
            pass
        else:
            # At the present time, it's not worthwhile for me to increase/decrease my reputation anymore
            # in the same direction. Try moving my reputation in the opposite direction instead.
            global hunting_mode
            hunting_mode = not hunting_mode
            
        # Clear round_results to start monitoring a new set of 14 rounds.
        round_results = []
        
    # Finally, hunt against everyone or slack against everyone, depending 
    # on the state of the hunting_mode variable.
    if hunting_mode:
        return ['h']*num_opponents
    else:
        return ['s']*num_opponents

    # NOTE: It seems like it might be a good idea to come up with a strategy for deciding 
    # against whom I should hunt in a given round (e.g. don't hunt against slackers or else they'll end
    # up winning...), but I'm going to take a risk and just treat everyone equally, hoping that the rest 
    # of the field punishes the slackers appropriately.
    

def hunt_outcomes(food_earnings):
    # hunt_outcomes is called after all hunts for the round are complete.
    
    ### All that's necessary to do here is calculate the percentage of people that
    ### hunted against me this round.
    
    hunting_opponents = 0
    for result in food_earnings:
        if result >= 0:
            hunting_opponents += 1
            
    # Calculate the percentage of opponents that hunted against me this round.
    hunt_percentage = hunting_opponents * 1.0 / len(food_earnings)
    
    # Store data on how many opponents hunt against me at a given level of reputation
    if start_storing_results:
        global round_results
        round_results.append((my_reputation,hunt_percentage))

def round_end(award, m, number_hunters):
    
    ###  I'm not going to do anything in this function, because none of these data are very
    ###  relevant for the purposes of my algorithm.
    
    pass