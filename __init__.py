import sys, pygame, shutil, os
import time
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler, FileSystemEventHandler

try:
    import looky_config as lcfg
except ImportError:
    answer = raw_input('looky_config.py does not exist. Should it be automatically generated? [y/n] ').lower()
    if answer=='y':
        shutil.copyfile('./looky_config_template.py','./looky_config.py')
        import looky_config as lcfg
    else:
        sys.exit('Please create looky_config.py from looky_config_template.py.')
if not os.path.exists('./dpi.txt'):
    answer = raw_input('dpi.txt does not exist. Should calibrate.py be run to determine monitor DPI? [y/n] ').lower()
    if answer=='y':
        import calibrate
        pygame.quit()
    else:
        sys.exit('Please run calibrate.py first to establish the monitor DPI, or create a text file dpi.txt containing just this number.')


        
from constants import *
from components import Target,Modstate
    
import datetime



# load parameters from config file
line_color = lcfg.LINE_COLOR
background_color = lcfg.BACKGROUND_COLOR
font = lcfg.FONT
font_size = lcfg.FONT_SIZE
fps = lcfg.MAX_FPS
try:
    text_left = lcfg.TEXT_LEFT_OFFSET
except Exception as e:
    text_left = 0
try:
    display_mode_index = lcfg.DEFAULT_DISPLAY_MODE
except Exception as e:
    display_mode_index = 0

# open a log file and define a logging function:
#try:
#    logfile = open('log.txt','a')
#except Exception as e:
#    logfile = open('log.txt','a')
#logfile.write('blahblahblah')

def log(text,stdout=False):
    now = datetime.datetime.now()
    fid = open('./log.txt','a')
    fid.write('%s\t%s\n'%(now.strftime('%Y-%m-%d\t%H:%M:%S'),text))
    fid.close()
    #logfile.write('%s\t%s\n'%(now.strftime('%Y-%m-%d\t%H:%M:%S'),text))
    if stdout:
        print('%s\t%s\n'%(now.strftime('%Y-%m-%d\t%H:%M:%S'),text))
    
# initialize pygame, set some initial parameters:
pygame.init()
myfont = pygame.font.SysFont(font, font_size)

pygame.key.set_repeat(1000,100)

clock = pygame.time.Clock()

# set up the screen using the desired display mode:
display_modes = pygame.display.list_modes()
print('Display modes:')
for idx,dm in enumerate(display_modes):
    print('%d: %s'%(idx,dm))
# check if the requested index is too high
display_mode_index = min(display_mode_index,len(display_modes)-1)
size = width, height = display_modes[display_mode_index]
n_display_modes = len(display_modes)

sdl_x = -1920
sdl_y = 0
os.environ['SDL_VIDEO_WINDOW_POS'] = f"{sdl_x},{sdl_y}"

screen = pygame.display.set_mode(size)
hwidth = width//2
hheight = height//2
#pygame.display.toggle_fullscreen()

# initialize the Target object:
tar = Target()

# this function is used to cycle through possible
# display modes; time_of_last_mode_change is used
# to display the mode for a second as the user
# is cycling:
time_of_last_mode_change = 0
def cycle_modes():
    """Cycle through display modes."""
    global screen,size,width,height,hwidth,hheight,display_modes,display_mode_index,n_display_modes,time_of_last_mode_change
    time_of_last_mode_change = time.time()
    display_mode_index = (display_mode_index+1)%n_display_modes
    size = width, height = display_modes[display_mode_index]
    screen = pygame.display.set_mode(size)
    hwidth = width//2
    hheight = height//2

def exit():
    """Exit via sys.exit()."""
    sys.exit()

def fullscreen():
    """Toggle fullscreen mode."""
    pygame.display.toggle_fullscreen()

def toggle_help():
    """Toggle help hints."""
    global help_on
    help_on = not help_on
    
key_triples = [
    (pygame.K_ESCAPE,Modstate('any'),exit),
    (pygame.K_q,Modstate('any'),exit),
    (pygame.K_F5,Modstate(''),fullscreen),
    (pygame.K_LEFT,Modstate(''),tar.left),
    (pygame.K_RIGHT,Modstate(''),tar.right),
    (pygame.K_UP,Modstate(''),tar.up),
    (pygame.K_DOWN,Modstate(''),tar.down),
    (pygame.K_LEFT,Modstate('ctrl'),tar.small_left),
    (pygame.K_RIGHT,Modstate('ctrl'),tar.small_right),
    (pygame.K_UP,Modstate('ctrl'),tar.small_up),
    (pygame.K_DOWN,Modstate('ctrl'),tar.small_down),
    (pygame.K_LEFT,Modstate('shift-ctrl'),tar.very_small_left),
    (pygame.K_RIGHT,Modstate('shift-ctrl'),tar.very_small_right),
    (pygame.K_UP,Modstate('shift-ctrl'),tar.very_small_up),
    (pygame.K_DOWN,Modstate('shift-ctrl'),tar.very_small_down),
    (pygame.K_LEFT,Modstate('alt'),tar.offset_left),
    (pygame.K_RIGHT,Modstate('alt'),tar.offset_right),
    (pygame.K_UP,Modstate('alt'),tar.offset_up),
    (pygame.K_DOWN,Modstate('alt'),tar.offset_down),
    (pygame.K_EQUALS,Modstate('ctrl'),tar.increment_line_width),
    (pygame.K_MINUS,Modstate('ctrl'),tar.decrement_line_width),
    (pygame.K_EQUALS,Modstate(''),tar.increase_radius),
    (pygame.K_MINUS,Modstate(''),tar.decrease_radius),
    (pygame.K_SPACE,Modstate(''),tar.switch_eye),
    (pygame.K_m,Modstate(''),cycle_modes),
    (pygame.K_c,Modstate(''),tar.center),
    (pygame.K_c,Modstate('ctrl'),tar.center_offsets),
    (pygame.K_SLASH,Modstate(''),toggle_help),
    (pygame.K_PAGEUP,Modstate(''),tar.location_script_previous),
    (pygame.K_PAGEDOWN,Modstate(''),tar.location_script_next),
    (pygame.K_RETURN,Modstate(''),tar.freeze_target),
    (pygame.K_DELETE,Modstate(''),tar.clear_frozen),
    (pygame.K_s,Modstate(''),tar.create_location_script)
    ]

# Use the keys and function docstrings to make a help menu.
help_strings = []
for kt in key_triples:
    if kt[0] in [pygame.K_RIGHT,pygame.K_UP,pygame.K_DOWN]:
        continue
    elif kt[0]==pygame.K_LEFT:
        key_name = 'arrow'
    else:
        key_name = pygame.key.name(kt[0])
        
    modifier = kt[1].__str__()
    if modifier in ['any','none']:
        modifier = ''
    else:
        modifier = modifier+'-'
    doc = kt[2].__doc__
    lead = '%s%s:'%(modifier,key_name)
    while len(lead)<18:
        lead = lead+' '
    help_strings.append('%s %s'%(lead,doc))

# convert to a dictionary for efficient lookup:
key_dict = {}
for key,key_ms,func in key_triples:
    if key in key_dict.keys():
        key_dict[key].append((key_ms,func))
    else:
        key_dict[key] = [(key_ms,func)]
        

# note the time the loop starts:
t0 = time.time()
log_t0 = time.time()
# a couple of booleans to keep track of state:
printed = False
help_on = False

# current_ms keeps track of the currently pressed
# keyboard modifiers; its state is updated in the
# event loop below, using its own call to
# pygame.key.get_mods
current_ms = Modstate()


class ObserverHandler(FileSystemEventHandler):
    def __init__(self,target):
        super().__init__()
        self.target = target
    def on_created(self,event):
        filename = event.src_path
        ext = os.path.splitext(filename)[1]
        if ext.lower()=='.unp':
            outfn = filename.replace('.unp','')+'.looky'
            outstr = str(self.target)
            with open(outfn,'w') as fid:
                fid.write(outstr)
        

try:
    path = lcfg.DATA_MONITORING_DIRECTORY
    #event_handler = LoggingEventHandler()
    event_handler = ObserverHandler(tar)
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
except AttributeError as ae:
    print('DATA_MONITORING_DIRECTORY not set in looky_config.py. Proceeding without data monitoring.')
    pass
except FileNotFoundError as fnfe:
    print('DATA_MONITORING_DIRECTORY %s not found. Please edit looky_config.py as required.'%lcfg.DATA_MONITORING_DIRECTORY)
    sys.exit()


n_frames = 0
last_help_on = False
while 1:
    n_frames = n_frames + 1
    # throttle the frame rate to the lcfg value:
    clock.tick(fps)
    # check the current fps:
    fps = clock.get_fps()
    
    # get the system time and calculate the
    # age of the process and the time since
    # the last display mode change:
    t = time.time()
    mode_age = t-time_of_last_mode_change
    age = t-t0
    log_age = t-log_t0
    print(log_age)
    if (age):
        other_fps = float(n_frames)/float(age)
    else:
        other_fps = -1
    # set mode_changed to true if the mode
    # was changed in the last second:
    mode_changed = mode_age<1.0

    state_changed = False
    # after the target has been at one location
    # for more than X seconds, if the location
    # hasn't been printed to the log, print
    # it now.
    if not printed and log_age>2.0:
        log(tar.msg_log_entry(),True)
        printed = True
        log_t0 = time.time()
        
    for event in pygame.event.get():
        t0 = time.time()
        log_t0 = time.time()
        state_changed = True
        mouse_state_changed = False
        current_ms.update()
        alt_on = current_ms.alt
        if event.type == pygame.QUIT: exit()
        elif event.type == pygame.KEYDOWN:
            try:
                tups = key_dict[event.key]
                for key_ms,func in tups:
                    if key_ms==current_ms:
                        func()
                        break
            except Exception as e:
                pass
            printed = False
        elif event.type == pygame.MOUSEMOTION:
            continue
            mouse_state_changed = True
            mousex,mousey = event.pos
            mousex = mousex-hwidth
            mousey = mousey-hheight
            x_deg,y_deg = tar.px2deg(mousex,mousey)
        elif event.type == pygame.MOUSEBUTTONUP:
            mousex,mousey = event.pos
            mousex = mousex-hwidth
            mousey = mousey-hheight
            x_deg,y_deg = tar.px2deg(mousex,mousey)
            tar.set_position(x_deg,y_deg)
            printed = False

    if not state_changed and not mode_changed and not mouse_state_changed:
        continue


    screen.fill(background_color)

    # draw here

    lines = tar.get_lines()
    for pt1,pt2 in lines:
        dpt1 = (pt1[0]+hwidth,pt1[1]+hheight)
        dpt2 = (pt2[0]+hwidth,pt2[1]+hheight)
        pygame.draw.line(screen,line_color,dpt1,dpt2,tar.line_width_px)

    if lcfg.EMPTY_CENTER:
        cx,cy,crad = tar.get_circle()
        cx = cx+hwidth
        cy = cy+hheight
    pygame.draw.circle(screen,lcfg.BACKGROUND_COLOR,(cx,cy),crad,0)
    
    if alt_on:
        offset_lines = tar.get_offset_lines()
        for pt1,pt2 in offset_lines:
            dpt1 = (pt1[0]+hwidth,pt1[1]+hheight)
            dpt2 = (pt2[0]+hwidth,pt2[1]+hheight)
            pygame.draw.line(screen,RED,dpt1,dpt2,tar.line_width_px)
            
    msg_list = [tar.msg_ret_location()]
    msg_colors = [lcfg.WHITE]
    #msg_list = [tar.msg_ret_location(),tar.msg_abs_location()]
    #msg_colors = [lcfg.WHITE,lcfg.GRAY]
    #msg_list.append('%0.1f fps'%other_fps)
    #msg_colors.append(lcfg.GRAY)
    if mouse_state_changed:
        msg_list.append('%0.3f, %0.3f'%(x_deg,y_deg))
        msg_colors.append(lcfg.GREEN)
    if alt_on:
        msg_list.append(tar.msg_offset_location())
        msg_colors.append(lcfg.OFFSET_COLOR)
    if mode_changed:
        msg_list.append('%d x %d (mode %d)'%(width,height,display_mode_index))
        msg_colors.append(lcfg.WHITE)
    if help_on:
        msg_list = msg_list + help_strings
        msg_colors = msg_colors + [lcfg.HELP_COLOR]*len(help_strings)
    help_changed = not help_on==last_help_on
    if help_changed and help_on:
        for s in help_strings:
            print(s)
    last_help_on = help_on
        
    for idx,(msg,color) in enumerate(zip(msg_list,msg_colors)):
        textsurface = myfont.render(msg, False, color)
        screen.blit(textsurface,(text_left,0+idx*font_size))
        
    pygame.display.flip()
    
