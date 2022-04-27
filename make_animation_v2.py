import numpy as np
from matplotlib import pyplot as plt
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from fig2gif import GIF
from location_script import location_script


## invert locations for this version, in which the fixation star moves

location_script0 = [p for p in location_script]

location_script = [(-a,-b) for a,b in location_script]

xmax = np.max([ls[0] for ls in location_script])
ymax = np.max([ls[1] for ls in location_script])
xmin = np.min([ls[0] for ls in location_script])
ymin = np.min([ls[1] for ls in location_script])

xmax0 = np.max([ls[0] for ls in location_script0])
ymax0 = np.max([ls[1] for ls in location_script0])
xmin0 = np.min([ls[0] for ls in location_script0])
ymin0 = np.min([ls[1] for ls in location_script0])


oct_color = (0.75,0.00,0.00)
led_color = (0.00,0.75,0.00)
bg_color = (0.00,0.00,0.00)

dark_time = 60.0*5.0
location_time = 3.0
flash_delay = 0.5
startup_delay = 5.0
flash_duration = 0.5
dt = 0.5
noise_rms = 0.25
oct_scan_time = 0.2
stimulus_radius = 0.4
make_movie = True
speedup = 5.0

N = len(location_script)

T = dark_time+N*location_time
t_arr = np.arange(0,T,dt)


requested_flash_times = dark_time+flash_delay+np.arange(0,N*location_time,location_time)+startup_delay
flash_times = []
for rft in requested_flash_times:
    flash_times.append(t_arr[np.argmin(np.abs(rft-t_arr))])

flash_times = np.array(flash_times)
noise = np.random.randn(len(flash_times))*noise_rms
flash_times = flash_times + noise

flash_starts = flash_times
flash_ends = flash_starts+flash_duration

requested_t_start = dark_time-5.0
requested_t_end = T
t_start_idx = np.argmin(np.abs(requested_t_start-t_arr))
t_end_idx = np.argmin(np.abs(requested_t_end-t_arr))


def draw_dark_adaptation(ax,edgecolor='w',facecolor='w'):
    dark_x1 = 0
    dark_dx = dark_time
    dark_x2 = dark_x1+dark_dx
    meas_x1 = flash_starts[0]
    meas_x2 = flash_ends[-1]
    meas_dx = meas_x2-meas_x1
    
    drect = patches.Rectangle((dark_x1, .7), dark_dx, .05, linewidth=2, edgecolor=edgecolor, facecolor=facecolor)
    # Add the patch to the Axes
    ax.add_patch(drect)
    ax.text(dark_x1,1,'dark adaptation',c='w')

    mrect = patches.Rectangle((meas_x1,.7),meas_dx,.05, linewidth=2, edgecolor=edgecolor, facecolor=facecolor)
    ax.add_patch(mrect)
    ax.text(meas_x1,1,'measurement',c='w')
    
def draw_flashes(ax,color='g'):
    for ft in flash_times:
        ax.arrow(ft,0,0,0.5,color=color)

def draw_oct(ax,loc,t,scan_length=1.0,scan_time=oct_scan_time,alpha=0.75):
    x = loc[0]
    y = loc[1]
    x1 = x-scan_length/2.0
    x2 = x+scan_length/2.0

    scan_x = (t%scan_time)/scan_time*scan_length+x1
    plt.plot([x1,x2],[y,y],color=oct_color,marker=None,linestyle='-',linewidth=2,alpha=alpha)
    plt.plot(scan_x,y,color=oct_color,marker='o',markersize=2)


def draw_stim(ax,loc,color=led_color,rad=stimulus_radius,alpha=0.75):
    circ = patches.Circle((loc[0],loc[1]),rad,color=color,alpha=alpha)
    ax.add_patch(circ)


def draw_fixation(ax,loc,rad = 1.0):
    x0,y0 = loc
    for theta in np.arange(0,2*np.pi,np.pi/4.0):
        x1 = np.cos(theta)*rad+x0
        y1 = np.sin(theta)*rad+y0
        ax.plot([x0,x1],[y0,y1],'w-',linewidth=2)

flash_idx = None

loc = location_script[0]
oct_loc = location_script[0]



if make_movie:
    mov = GIF('experiment_cartoon_%dx_v2.gif'%speedup,fps=speedup/dt)

fig = plt.figure(figsize=(8,5))
fig.set_facecolor('k')
fig.set_edgecolor('k')

ax1 = fig.add_axes([0.05,0.7,0.9,0.1])
ax2 = fig.add_axes([0.05,0.1,0.9,0.5])

for t in t_arr[t_start_idx:t_end_idx]:
    ax1.clear()
    ax1.set_facecolor('k')
    ax1.set_yticks([])
    ax1.set_xlim((-10,T+10))
    ax1.set_ylim((-.2,1.2))
    
    
    ax1.set_xticks(np.arange(0,T,60))
    ax1.set_xticklabels(['%d'%round(s/60.0) for s in np.arange(0,T,60)])
    ax1.spines['bottom'].set_color('w')
    #ax1.spines['top'].set_color('w')
    #ax1.spines['left'].set_color('w')
    #ax1.spines['right'].set_color('w')
    ax1.tick_params(axis='x', colors='w')
    ax1.xaxis.label.set_color('w')
    ax1.set_xlabel('time (m)')
    ax1.set_title('timeline')
    ax1.title.set_color('w')
    
    draw_dark_adaptation(ax1)
    draw_flashes(ax1)
    ax1.axvline(t,ymin=0.0,ymax=0.5,c='w')
    


    ax2.clear()
    ax2.axis('equal')
    ax2.set_xlim((xmin-5,xmax+3))
    ax2.set_ylim((ymin-3,ymax+3))
    ax2.set_facecolor('k')
    ax2.set_yticks([])
    ax2.set_xticks([])
    ax2.xaxis.label.set_color('w')
    ax2.set_xlabel('patient view')
    ax2.title.set_color('w')

    if t>dark_time:
        draw_oct(ax2,(0,0),t)

        flash = False

        for n in range(N):
            if t<=flash_ends[n]+.5:
                oct_loc = location_script[n]
                break
        
        for n in range(N):
            if flash_starts[n]<=t<=flash_ends[n]:
                flash = True
                flash_idx = n
                loc = location_script[flash_idx]
                break

        if flash:
            draw_stim(ax2,(0,0))

        draw_fixation(ax2,oct_loc)
    

    if make_movie:
        mov.add(fig)
    plt.pause(dt/100.0)

if make_movie:
    mov.make()

ax1.clear()
ax1.set_facecolor('k')
ax1.set_yticks([])
ax1.set_xlim((-10,T+10))
ax1.set_ylim((-.2,1.2))


ax1.set_xticks(np.arange(0,T,60))
ax1.set_xticklabels(['%d'%round(s/60.0) for s in np.arange(0,T,60)])
ax1.spines['bottom'].set_color('w')
#ax1.spines['top'].set_color('w')
#ax1.spines['left'].set_color('w')
#ax1.spines['right'].set_color('w')
ax1.tick_params(axis='x', colors='w')
ax1.xaxis.label.set_color('w')
ax1.set_xlabel('time (m)')
ax1.set_title('timeline')
ax1.title.set_color('w')

draw_dark_adaptation(ax1)
draw_flashes(ax1)

ax2.clear()
ax2.axis('equal')
ax2.set_xlim((xmin0-5,xmax0+3))
ax2.set_ylim((ymin0-3,ymax0+3))
ax2.set_facecolor('k')
ax2.set_yticks([])
ax2.set_xticks([])
ax2.xaxis.label.set_color('w')
ax2.set_xlabel('imaged locations')
ax2.title.set_color('g')


#draw_fixation(ax2,(0,0))

ax2.text(0,0.5,'fovea',c='w',ha='center',va='center')
ax2.text(0,0,'*',c='w',ha='center',va='center')

for n in range(N):
    draw_stim(ax2,location_script0[n])
    plt.text(*location_script0[n],'%d'%(n+1),ha='center',va='center',color='w')

sbx = -2.0
sby = 0.0
plt.plot([sbx-2,sbx-1],[sby+0,sby+0],'w-',linewidth=3)
plt.text(sbx-1.5,sby-.1,'$1^\circ$',ha='center',va='top',color='w')
    
plt.savefig('experiment_cartoon_summary_v2.png',dpi=300)
plt.pause(.00001)
    
