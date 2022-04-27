import numpy as np
from matplotlib import pyplot as plt
import matplotlib.pyplot as plt
import matplotlib.patches as patches

from fig2gif import GIF

from location_script import location_script

location_script = location_script[:20]

location_script = [(0,0)]+location_script

xmax = np.max([ls[0] for ls in location_script])
ymax = np.max([ls[1] for ls in location_script])
xmin = np.min([ls[0] for ls in location_script])
ymin = np.min([ls[1] for ls in location_script])

print(xmin,xmax,ymin,ymax)

oct_color = (0.75,0.00,0.00)
led_color = (0.00,0.75,0.00)
bg_color = (0.00,0.00,0.00)

dark_time = 60.0*5.0
location_time = 5.0
flash_delay = 1.0
startup_delay = 5.0

N = len(location_script)

T = dark_time+N*location_time
dt = 0.2
t_arr = np.arange(0,T,dt)


requested_flash_times = dark_time+flash_delay+np.arange(0,N*location_time,location_time)+startup_delay
flash_times = []
for rft in requested_flash_times:
    flash_times.append(t_arr[np.argmin(np.abs(rft-t_arr))])

flash_times = np.array(flash_times)
noise_rms = 0.25
noise = np.random.randn(len(flash_times))*noise_rms
flash_times = flash_times + noise


flash_duration = 0.5

fig = plt.figure(figsize=(8,5))

ax1 = fig.add_axes([0.02,0.7,0.96,0.1])
ax2 = fig.add_axes([0.02,0.0,0.96,0.7])

requested_t_start = dark_time-10.0
requested_t_end = dark_time+10.0
t_start_idx = np.argmin(np.abs(requested_t_start-t_arr))
t_end_idx = np.argmin(np.abs(requested_t_end-t_arr))


def draw_dark_adaptation(ax,edgecolor='w',facecolor='k'):
    # Create a Rectangle patch
    rect = patches.Rectangle((0, 0), dark_time, 1, linewidth=3, edgecolor=edgecolor, facecolor=facecolor)
    # Add the patch to the Axes
    ax.add_patch(rect)
    
def draw_flashes(ax,color='g'):
    for ft in flash_times:
        ax.arrow(ft,0,0,0.5,color=color)

def draw_oct(ax,loc,t,scan_length=1.0,scan_time=1.0):
    x = loc[0]
    y = loc[1]
    x1 = x-scan_length/2.0
    x2 = x+scan_length/2.0

    scan_x = (t%1.0)/scan_time*scan_length+x1
    plt.plot([x1,x2],[y,y],color=oct_color,marker=None,linestyle='-',linewidth=3,alpha=0.5)
    plt.plot(scan_x,y,color=oct_color,marker='o',markersize=3)


def draw_stim(ax,loc,color=led_color,rad=0.5):
    circ = patches.Circle((loc[0],loc[1]),rad,color=color)
    ax.add_patch(circ)
    
for t in t_arr[t_start_idx:t_end_idx]:
    ax1.clear()
    ax1.set_facecolor('k')
    ax1.set_yticks([])
    ax1.set_xlim((-10,T+10))
    ax1.set_ylim((-.2,1.2))
    
    
    ax1.set_xticks(np.arange(0,T,60))
    ax1.set_xticklabels(['%d'%round(s/60.0) for s in np.arange(0,T,60)])


    draw_dark_adaptation(ax1)
    draw_flashes(ax1)
    ax1.axvline(t,c='w')
    


    ax2.clear()
    ax2.set_xlim((xmin-3,xmax+3))
    ax2.set_ylim((ymin-3,ymax+3))
    if t>dark_time:
        flash_idx = np.where(flash_times>=t)[0][0]
        loc = location_script[flash_idx]
        draw_oct(ax2,loc,t)
        print(t,flash_times[flash_idx],flash_times[flash_idx]+flash_duration)
        if t>=flash_times[flash_idx] and t<=flash_times[flash_idx]+flash_duration:
            draw_stim(ax2,loc)

        
    plt.pause(dt/100.0)



plt.show()
