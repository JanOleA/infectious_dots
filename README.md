# Basic Python disease spread simulator.

#### Disclaimer
I am not an epidemiologist. This simulator does not in any way accurately portray disease spread in the real world. It is a pet project of mine just because I find it interesting (and obviously very relevant right now).

### Parameters
All parameters for the simulation are contained in _settings.py_

### Output
The program produces three output files for each run, with the root of the filename given in _settings.py_, these are:
 - root.pdf - susceptible, infected, removed and dead, plot over time.
 - root_dr.pdf - cumulative death rate over time
 - root.mp4 - simulation video

### Running the program
Once simulation parameters are provided in _settings.py_ the program can be ran simply with:
 - python infectious\_dots.py

### Movement modes
The two main movement modes are "fast" and "slow".  
In the fast movement mode, each velocity vector changes according to the following equation each frame:  
~~~~Python
vel += (random(0,1) - 0.5)*0.1 - vel*abs(vel)*0.01
~~~~
In the slow movement mode, each velocity vector changes according to the following equation each frame:  
~~~~Python
vel += (random(0,1) - 0.5)*0.1 - vel*0.8
~~~~

### Parameters
#### General
- N:  
Number of dots (agents) in the simulation  
- tot\_infected:  
Number of dots that start off with infection
- ratio\_immune:  
The number of dots that start off immune.
- box\_size:  
Length of each side of the simulation area
- max\_frames:  
Maximum number of frames to simulate. The simulation will stop earlier if the number of infected drops to 0.
#### Infection spread
- infection\_chance:  
The chance per frame that a dot will infect any other dot within the infection radius. Applies to all dots within the radius of an infected dot.
- infection\_radius:  
The radius within which an infected dot can infect others.
#### Dot speed behaviour
- radio\_slow:  
The ratio of dots that begin in the slow movement mode (0 is none, 1 is all). 
- set\_slow\_ratio:  
The ratio of dots that will be set to the slow movement mode once a given threshold is reached.
- set\_slow\_threshold:  
Once this number of dots are infected, the ratio of dots with slow movement mode will be set to the value given with _set\_slow\_ratio_
- set\_fast\_threshold:  
If the number of infected dots drops below this value, the movement modes will be set back to the default.
#### Infection length parameters
- infection\_length\_min:  
Minimum number frames the infection will last.
- infection\_length\_max:  
Maximum number of frames the infection will last. The value will be a random (uniform) number between the limits.
- immunity\_length\_min:  
Minimum number of frames immunity will last.
- immunity\_length\_max:  
Maximum number of frames immunity will last. The value will be a random (uniform) number between the limits.
#### Dot meeting area parameters
There is a common meeting area in the center of the simulation for the dots (called "work"). Every dot has a random place in the simulation are that is its "home". Every frame there is a chance that a dot will move to the common area, before returning to its "home" after a given number of frames. The dot will then stay at home for a given number of frames before beginning to drift as usual.
- stay\_work\_time:  
Number of frames to stay at work before returning to home.
- stay\_home\_time:  
Number of frames to stay at home before beginning to drift.
- go\_to\_work\_chance:  
Chance every frame that the dot will decide to go to work.
- reduced\_go\_to\_work\_chance:  
Reduced chance per frame for the dots to go to work, applied after a given threshold of infected dots is reached.
- reduced\_go\_to\_work\_threshold:  
Once this number of dots are infected, the lower chance for going to work will be applied to all dots.
- increase\_go\_to\_work\_threshold:  
If the number of infected drops below this value, the default chance for going to work will be reapplied.
- all\_home:  
True or False. If True, all the dots will begin at their "home" position and begin drifting after _stay\_home\_time_ frames has passed.
#### Healthcare and death parameters
All dots require healthcare if they get sick. Dots without healthcare have a different chance of dying than dots with healthcare. If there are not enough spaces, dots will wait until a spot opens up before receiving care.
- healthcare\_limit:  
Capacity of the healthcare system. I.e. the ratio of the total number of dots that can receive healthcare simultaneously. (0 is none, 1 is all)
- death\_chance\_wi\_care:  
Chance per frame that a dot receiving healthcare will die.
- death\_chance\_no\_care:  
Chance per frame that a dot not receiving healthcare will die.
#### Plotting
- filename:  
The filename root. See the Output section above for details.
- plot\_title:  
The title to display on the plots.
- fps:  
Frames per seconds in the saved video.
- save\_anim:  
True or False. If True will save the animation as an MP4 file.

NOTE: If plot\_title is left as an empty string or as None, a title will be generated with the simulation parameters displayed as follows:
- InfC = infection chance
- InfRad = infection radius
- SSl = default slow ratio
- SIm = initial immune ratio
- SetSlR = set slow ratio
- SetSlT = set slow threshold
- SetFaT = set fast threshold
- InfL = infection length interval
- Im_L = immunity length interval
- StWTim = time dots stay at work
- StHTim = time dots stay at home
- GW\_C = chance to go to work per frame
- RedGW\_C = reduced chance to go to work per frame
- RedGW\_T = reduced chance to go to work threshold
- IncGW\_T = increased chance to go to work threshold
- AH = whether or not all dots started at home
