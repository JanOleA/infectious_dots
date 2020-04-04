N = 2000 # number of dots
tot_infected = 1 # infected to start off with
box_size = 500 # size of each edge of the box

infection_chance = 0.05 # chance for an infected dot to infect a susceptible dot each frame
infection_radius = 7 # radius within which an infected dot can infect others

# how many dots to start off with moving slowly (ratio)
ratio_slow = 0.1

# how many dots will start off immune (ratio)
ratio_immune = 0

set_slow_ratio = 0.95 # ratio of dots to set to slow movement after the threshold of infected dots is reached
set_slow_threshold = 300 # threshold of number of infected where the number of slow dots is increased
set_fast_threshold = 0 # threshold where dots will begin to move fast again if number of infected drops below

infection_length_min = 200 # minimum frames the infection lasts
infection_length_max = 250 # maximum frames the infection lasts

immunity_length_min = 5000 # minimum number of frames immunity lasts
immunity_length_max = 5500 # maximum number of frames immunity lasts

""" 'Work', for all dots, is in the center of the box.
After going to work a dot will always go home after, then begin to drift randomly.
"""
stay_work_time = 30 # how long to stay "at work" before going home
stay_home_time = 30 # how long to stay "at home" before beginning to drift
go_to_work_chance = 0.0001 # chance each frame that a dot decides to go "to work"
reduced_go_to_work_chance = 0.00001 # chance after reduction in how many goes to work
reduced_go_to_work_threshold = 2000 # threshold of number of infected where the chance to go to work is reduced
increase_go_to_work_threshold = 0 # threshold where dots will increase work chance again if number of infected drops below

all_home = False # if True, all dots will start of at home

max_frames = 5000

filename = "slow_after_300_low_infection_chance"
fps = 40
save_anim = True
