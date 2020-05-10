N = 1000 # number of dots #2000
tot_infected = 2 # infected to start off with
box_size = 300 # size of each edge of the box #400

infection_chance = 0.03 # chance for an infected dot to infect a susceptible dot each frame
infection_radius = 7 # radius within which an infected dot can infect others

# how many dots to start off with moving slowly (ratio)
ratio_slow = 0.3

# how many dots will start off immune (ratio)
ratio_immune = 0

set_slow_ratio = 0.95 # ratio of dots to set to slow movement after the threshold of infected dots is reached
set_slow_threshold = 5000 # threshold of number of infected where the number of slow dots is increased
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
go_to_work_chance = 0.0002 # chance each frame that a dot decides to go "to work"
reduced_go_to_work_chance = 0.00001 # chance after reduction in how many goes to work
reduced_go_to_work_threshold = 5000 # threshold of number of infected where the chance to go to work is reduced
increase_go_to_work_threshold = 0 # threshold where dots will increase work chance again if number of infected drops below

all_home = True # if True, all dots will start of at home

healthcare_limit = 0.35 # capacity of the healthcare system (ratio of N)
death_chance_wi_care = 0.0005 # chance of death per day of infection for dots receiving healthcare
death_chance_no_care = 0.01 # chance of death per day of infection for dots not receiving healthcare

max_frames = 5000

filename = "30p_slow_frequent_work_test"
plot_title = f"30% slow, frequent work\nhealthcare capacity for 35%"
fps = 40
save_anim = True

if plot_title == "" or plot_title == None:
    plot_title = f"InfC = {infection_chance} | InfRad = {infection_radius} | SSl = {ratio_slow} | SIm = {ratio_immune} | SetSlR = {set_slow_ratio}\nSetSlT = {set_slow_threshold} | SetFaT = {set_fast_threshold} | "
    plot_title += f"InfL = {infection_length_min} - {infection_length_max} | Im_L = {immunity_length_min} - {immunity_length_max}\nStWTim = {stay_work_time} | StHTim = {stay_home_time} | GW_C = {go_to_work_chance}\nRedGW_C = {reduced_go_to_work_chance} | RedGW_T = {reduced_go_to_work_threshold} | IncGW_T = {increase_go_to_work_threshold}"
    plot_title += f" | AH = {all_home}"