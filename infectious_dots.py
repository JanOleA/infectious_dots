import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
import random
from settings import *

print(f"Dots per square unit = {N/box_size**2}")

class dot:
    def __init__(self):
        self.x = box_size*np.random.random()
        self.y = box_size*np.random.random()
        self.vel_x = 0
        self.vel_y = 0
        self.max_vel = 20
        self.infected_days = 0
        self.immune_days = 0
        self.infected_duration = int(np.mean([infection_length_max,
                                              infection_length_min]))

        self.immunity_duration = int(np.mean([immunity_length_min,
                                              immunity_length_max]))

        self.state = "susceptible"
        self.behaviour = "normal"
        self.set_normal()

        self.home_x = int(np.random.random()*box_size)
        self.home_y = int(np.random.random()*box_size)
        self.home_radius = 10
        self.home_counter = 0

        self.work_x = box_size/2
        self.work_y = box_size/2
        self.work_radius = 10
        self.work_counter = 0
        self.reach_home = False
        self.reach_work = False

        self.go_to_work_chance = go_to_work_chance

        self.infected_others = 0


    def go_home(self):
        self.behaviour = "move_home"
        self.reach_home = False


    def go_work(self):
        self.behaviour = "move_work"
        self.reach_work = False


    def set_normal(self):
        if self.behaviour not in ["move_home", "move_work"]:
            self.behaviour = "normal"
        self.return_behaviour = "normal"


    def set_slow(self):
        if self.behaviour not in ["move_home", "move_work"]:
            self.behaviour = "slow"
        self.return_behaviour = "slow"


    @property
    def color(self):
        if self.state == "immune":
            return "green"
        if self.state == "susceptible":
            return "blue"
        if self.state == "infected":
            return "red"
        if self.state == "removed":
            return "purple"


    def normal_motion(self):
        self.vel_x += (np.random.random() - 0.5)*0.1 - self.vel_x*abs(self.vel_x)*0.01
        self.vel_y += (np.random.random() - 0.5)*0.1 - self.vel_y*abs(self.vel_y)*0.01


    def slow_motion(self):
        self.vel_x += (np.random.random() - 0.5)*0.1 - self.vel_x*0.8
        self.vel_y += (np.random.random() - 0.5)*0.1 - self.vel_y*0.8


    def move(self, dots, dots_positions):
        distance_home = np.sqrt((self.x - self.home_x)**2
                              + (self.y - self.home_y)**2)

        distance_work = np.sqrt((self.x - self.work_x)**2
                              + (self.y - self.work_y)**2)

        if np.random.random() < self.go_to_work_chance:
            self.go_work()

        if self.behaviour == "normal":
            self.normal_motion()

        if self.behaviour == "slow":
            self.slow_motion()

        if self.behaviour == "move_home":
            self.home_counter += 1
            if distance_home > self.home_radius:
                if self.reach_home:
                    self.vel_x *= -1
                    self.vel_y *= -1
                else:
                    self.vel_x = (self.home_x - self.x)/max([abs(self.home_x - self.x)**0.2, 1])
                    self.vel_y = (self.home_y - self.y)/max([abs(self.home_y - self.y)**0.2, 1])
                self.reach_home = False
            else:
                if not self.reach_home:
                    self.reach_home = True
                    self.vel_x = (np.random.random() - 0.5)*0.1
                    self.vel_y = (np.random.random() - 0.5)*0.1
                if self.return_behaviour == "normal":
                    self.normal_motion()
                if self.return_behaviour == "slow":
                    self.slow_motion()

            if self.home_counter > stay_home_time:
                self.behaviour = self.return_behaviour
                self.home_counter = 0
                self.vel_x = (np.random.random() - 0.5)*0.1
                self.vel_y = (np.random.random() - 0.5)*0.1

        if self.behaviour == "move_work":
            self.work_counter += 1
            if distance_work > self.work_radius:
                if self.reach_work:
                    self.vel_x *= -1
                    self.vel_y *= -1
                else:
                    self.vel_x = (self.work_x - self.x)/max([abs(self.work_x - self.x)**0.2, 1])
                    self.vel_y = (self.work_y - self.y)/max([abs(self.work_y - self.y)**0.2, 1])
                self.reach_work = False
            else:
                if not self.reach_work:
                    self.reach_work = True
                    self.vel_x = (np.random.random() - 0.5)*0.1
                    self.vel_y = (np.random.random() - 0.5)*0.1
                if self.return_behaviour == "normal":
                    self.normal_motion()
                if self.return_behaviour == "slow":
                    self.slow_motion()

            if self.work_counter > stay_work_time:
                self.behaviour = self.return_behaviour
                self.work_counter = 0
                self.vel_x = (np.random.random() - 0.5)*0.1
                self.vel_y = (np.random.random() - 0.5)*0.1
                self.go_home()

        if self.vel_x > self.max_vel:
            self.vel_x = self.max_vel
        if self.vel_x < -self.max_vel:
            self.vel_x = -self.max_vel

        if self.vel_y > self.max_vel:
            self.vel_Y = self.max_vel
        if self.vel_y < -self.max_vel:
            self.vel_y = -self.max_vel

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
                self.immunity_duration = np.random.randint(immunity_length_min, immunity_length_max + 1)
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
                    self.infected_others += 1
                    dot.state = "infected"
                    dot.infected_days = 0
                    dot.infected_duration = np.random.randint(infection_length_min, infection_length_max + 1)


""" Initialize dots and set initial states """
dots = [dot() for i in range(N)]
for i in range(tot_infected):
    dots[i].state = "infected"
random.shuffle(dots)
for i in range(int(N*ratio_slow)):
    dots[i].set_slow()
random.shuffle(dots)
for i in range(int(N*ratio_immune)):
    dots[i].state = "immune"
random.shuffle(dots)

if all_home:
    for dot in dots:
        dot.go_home()
        dot.x = dot.home_x
        dot.y = dot.home_y

x_positions = []
y_positions = []
colors = []

num_susceptible = np.zeros(max_frames)
num_infected = np.zeros(max_frames)
r_over_time = np.zeros(max_frames)

dots_x_positions = np.array([dot.x for dot in dots])
dots_y_positions = np.array([dot.y for dot in dots])

slow_triggered = False
reduced_work_triggered = False

for frame in range(max_frames):
    r_values = []
    for dot in dots:
        dot.infect_near(dots,
                        [dots_x_positions, dots_y_positions],
                        chance = infection_chance,
                        radius = infection_radius)
        dot.move(dots, [dots_x_positions, dots_y_positions])
        if dot.state == "susceptible":
            num_susceptible[frame] += 1
        elif dot.state == "infected":
            num_infected[frame] += 1
            if dot.infected_others > 0:
                r_values.append(dot.infected_others)

    if num_infected[frame] > set_slow_threshold and not slow_triggered:
        for i in range(int(N*set_slow_ratio)):
            dots[i].set_slow()
        slow_triggered = True

    if num_infected[frame] < set_fast_threshold and slow_triggered:
        for dot in dots:
            dot.set_normal()
        for i in range(int(N*ratio_slow)):
            dots[i].set_slow()
        slow_triggered = False

    if num_infected[frame] > reduced_go_to_work_threshold and not reduced_work_triggered:
        for dot in dots:
            dot.go_to_work_chance = reduced_go_to_work_chance
        reduced_work_triggered = True

    if num_infected[frame] < increase_go_to_work_threshold and reduced_work_triggered:
        for dot in dots:
            dot.go_to_work_chance = go_to_work_chance
        reduced_work_triggered = False

    dots_x_positions = np.array([dot.x for dot in dots])
    dots_y_positions = np.array([dot.y for dot in dots])

    x_positions.append(dots_x_positions)
    y_positions.append(dots_y_positions)
    colors.append([dot.color for dot in dots])

    if sum(r_values) > 0:
        r_over_time[frame] = np.average(r_values)

    if frame % 1 == 0:
        print(f"Frame {frame}, num_infected = {num_infected[frame]}, R = {r_over_time[frame]:2.4f}   ", end = "\r")

    if num_infected[frame] == 0:
        print(f"Ending after {frame} frames with 0 infected                   ")
        max_frames = frame
        num_susceptible = num_susceptible[:frame]
        num_infected = num_infected[:frame]
        r_over_time = r_over_time[:frame]
        num_removed = N - (num_infected + num_susceptible)
        break
    num_removed = N - (num_infected + num_susceptible)

fig, ax1 = plt.subplots(figsize=(7,7))
l1 = ax1.plot(num_susceptible, label="susceptible")
l2 = ax1.plot(num_infected, label="infected")
l3 = ax1.plot(num_removed, label="removed & immune")
ax1.set_xlabel("Simulation frame")
ax1.set_ylabel("# of dots", color = "blue")
plt.title(plot_title)

ax2 = ax1.twinx()
l4 = ax2.plot(r_over_time, "--", color = "red", label="R value")
ax2.set_ylabel("R value", color = "red")

lns = l1 + l2 + l3 + l4
labs = [l.get_label() for l in lns]
ax1.legend(lns, labs, loc = 1)

plt.savefig("results/" + filename + ".pdf", dpi = 300)

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
    plt.title(f"Frame {i}, number of infected = {num_infected[i]}, R value = {r_over_time[i]:2.4f}")
    return d,

Writer = animation.writers['ffmpeg']
writer = Writer(fps=fps, metadata=dict(artist='Me'), bitrate=3000)

anim = animation.FuncAnimation(fig, animate, frames=max_frames, interval=20)
if save_anim: anim.save("results/" + filename + ".mp4", writer=writer)
plt.show()
