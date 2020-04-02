import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
import random

N = 1000 # number of dots
tot_infected = 1 # infected in the beginning
box_size = 250 # size of each edge of the box

infection_chance = 0.2 # chance for an infected dot to infect a susceptible dot per frame
infection_radius = 7 # radius within which an infected dot can infect others

ratio_slow = 0.1 # ratio of dots to start off with slow movement
ratio_immune = 0 # ratio of dots to start off immune

set_slow_ratio = 0.9 # ratio of dots to set to slow movement after the threshold of infected dots is reached
set_slow_threshold = 100 # threshold of number of infected where the number of slow dots is increased
set_fast_threshold = 0 # threshold where dots will begin to move fast again if number of infected drops below

infection_length_min = 100 # minimum frames the infection lasts
infection_length_max = 150 # maximum frames the infection lasts

immunity_length_min = 500 # minimum number of frames immunity lasts
immunity_length_max = 550 # maximum number of frames immunity lasts

max_frames = 5000

filename = "slow_after_100_immunitydrop"
fps = 40

class dot:
    def __init__(self):
        self.x = box_size*np.random.random()
        self.y = box_size*np.random.random()
        self.vel_x = 0
        self.vel_y = 0
        self.infected_days = 0
        self.immune_days = 0
        self.infected_duration = int(np.mean([infection_length_max,
                                              infection_length_min]))

        self.immunity_duration = int(np.mean([immunity_length_min,
                                              immunity_length_max]))

        self.state = "susceptible"
        self.behaviour = "normal"


    @property
    def color(self):
        if self.state == "susceptible":
            return "blue"
        if self.state == "infected":
            return "red"
        if self.state == "removed":
            return "purple"


    def move(self, dots):
        if self.behaviour == "normal":
            self.vel_x += (np.random.random() - 0.5)*0.1 - self.vel_x*abs(self.vel_x)*0.01
            self.vel_y += (np.random.random() - 0.5)*0.1 - self.vel_y*abs(self.vel_y)*0.01
            new_x = self.x + self.vel_x
            new_y = self.y + self.vel_y

        if self.behaviour == "slow":
            self.vel_x += (np.random.random() - 0.5)*0.1 - self.vel_x*0.8
            self.vel_y += (np.random.random() - 0.5)*0.1 - self.vel_y*0.8
            new_x = self.x + self.vel_x
            new_y = self.y + self.vel_y

        if new_x < 0 or new_x > box_size:
            self.vel_x *= -1
        else:
            self.x = new_x

        if new_y < 0 or new_y > box_size:
            self.vel_y *= -1
        else:
            self.y = new_y

        if self.state == "infected":
            self.infected_days += 1
            if self.infected_days > self.infected_duration:
                self.state = "removed"
                self.immune_days = 0
                self.immunity_duration = np.random.randint(immunity_length_min,
                                                           immunity_length_max + 1)

        if self.state == "removed":
            self.immune_days += 1
            if self.immune_days > self.immunity_duration:
                self.state = "susceptible"
                self.immune_days = 0


    def near_dots(self, dots, dots_positions, radius = 5):
        """ return all dots within a given radius """
        dots = np.array(dots)
        x_positions = dots_positions[0]
        y_positions = dots_positions[1]

        x_dists = self.x - x_positions
        y_dists = self.y - y_positions

        abs_dists = np.sqrt((x_dists**2 + y_dists**2))

        dots_within = dots[abs_dists < radius]
        dots_within = dots_within[dots_within != self]

        return dots_within


    def infect_near(self, dots, dots_positions, chance = 0.2, radius = 5):
        """ if infected, infect other dots nearby with a given chance """
        if self.state == "infected":
            close_dots = self.near_dots(dots, dots_positions, radius)
            rolls = np.random.random(size = len(close_dots))
            infect_dots = close_dots[rolls < chance]

            for dot in infect_dots:
                if dot.state == "susceptible":
                    dot.state = "infected"
                    dot.infected_days = 0
                    dot.infected_duration = np.random.randint(infection_length_min,
                                                              infection_length_max + 1)


""" Initialize dots and set initial states """
dots = [dot() for i in range(N)]
for i in range(tot_infected):
    dots[i].state = "infected"
random.shuffle(dots)
for i in range(int(N*ratio_slow)):
    dots[i].behaviour = "slow"
random.shuffle(dots)
for i in range(int(N*ratio_immune)):
    dots[i].state = "removed"
random.shuffle(dots)

x_positions = []
y_positions = []
colors = []

num_susceptible = np.zeros(max_frames)
num_infected = np.zeros(max_frames)

dots_x_positions = np.array([dot.x for dot in dots])
dots_y_positions = np.array([dot.y for dot in dots])

slow_triggered = False

for frame in range(max_frames):
    for dot in dots:
        dot.infect_near(dots,
                        [dots_x_positions, dots_y_positions],
                        chance = infection_chance,
                        radius = infection_radius)
        dot.move(dots)
        if dot.state == "susceptible":
            num_susceptible[frame] += 1
        if dot.state == "infected":
            num_infected[frame] += 1

    if num_infected[frame] > set_slow_threshold and not slow_triggered:
        for i in range(int(N*set_slow_ratio)):
            dots[i].behaviour = "slow"
        slow_triggered = True

    if num_infected[frame] < set_fast_threshold and slow_triggered:
        for dot in dots:
            dot.behaviour = "normal"
        for i in range(int(N*ratio_slow)):
            dots[i].behaviour = "slow"
        slow_triggered = False

    dots_x_positions = np.array([dot.x for dot in dots])
    dots_y_positions = np.array([dot.y for dot in dots])

    x_positions.append(dots_x_positions)
    y_positions.append(dots_y_positions)
    colors.append([dot.color for dot in dots])

    if frame % 1 == 0:
        print(f"Frame {frame}, num_infected = {num_infected[frame]}   ", end = "\r")

    if num_infected[frame] == 0:
        print(f"Ending after {frame} frames with 0 infected")
        max_frames = frame
        num_susceptible = num_susceptible[:frame]
        num_infected = num_infected[:frame]
        num_removed = N - (num_infected + num_susceptible)
        break
    num_removed = N - (num_infected + num_susceptible)

fig = plt.figure(figsize=(7,7))
plt.plot(num_susceptible, label="susceptible")
plt.plot(num_infected, label="infected")
plt.plot(num_removed, label="removed")
plt.legend()
plt.xlabel("Simulation frame")
plt.ylabel("# of dots")

plt.savefig(filename + ".pdf", dpi = 300)

fig = plt.figure(figsize=(7,7))
ax = plt.axes(xlim=(0, box_size), ylim=(0, box_size))
d = ax.scatter([dot.x for dot in dots],
               [dot.y for dot in dots],
               s = 2000/box_size,
               c = [dot.color for dot in dots])

def animate(i):
    x_positions_i = x_positions[i]
    y_positions_i = y_positions[i]
    colors_i = colors[i]
    d.set_offsets(np.array([x_positions_i, y_positions_i]).T)
    d.set_color(colors_i)
    plt.title(f"Frame {i}, number of infected = {num_infected[i]}")
    return d,

Writer = animation.writers['ffmpeg']
writer = Writer(fps=fps, metadata=dict(artist='Me'), bitrate=3000)

anim = animation.FuncAnimation(fig, animate, frames=max_frames, interval=20)
anim.save(filename + ".mp4", writer=writer)
plt.show()
