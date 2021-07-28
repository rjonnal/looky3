from constants import *
import math
import sys
import pygame
import looky_config as lcfg

class Target:
    """The target object must do the following:
    1. Know the current position of the target.
    2. Know the current center (origin) of its
       coordinate system.
    3. Be able to provide instructions to draw
       itself in screen coordinates.
    4. Provide a string describing retinal location
       and eye.
    """

    def __init__(self):
        self.eye = RIGHT

        try:
            with open('offsets.txt') as fid:
                self.x0_deg = float(fid.readline())
                self.y0_deg = float(fid.readline())
        except Exception as e:
            print e
            self.x0_deg = lcfg.X_OFFSET_DEG
            self.y0_deg = lcfg.Y_OFFSET_DEG

        self.x_deg = 0.0
        self.y_deg = 0.0

        self.step = lcfg.STEP_SIZE_DEG
        self.small_step = lcfg.STEP_FINE_DEG
        self.very_small_step = lcfg.STEP_VERY_FINE_DEG
        self.offset_step = lcfg.STEP_OFFSET_DEG

        self.screen_distance_m = lcfg.SCREEN_DISTANCE_M
        self.vflip = lcfg.VERTICAL_ORIENTATION
        self.hflip = lcfg.HORIZONTAL_ORIENTATION

        self.snap = lcfg.SNAP_MOUSE_TO_FINE_GRID

        self.center_rad = lcfg.EMPTY_CENTER

        try:
            with open('dpi.txt') as fid:
                dpi = float(fid.readline())
        except Exception as e:
            print 'Could not read dpi.txt',e

        px_per_m = dpi/25.4*1000.
        m_per_deg = math.sin(1.0/180.0*math.pi)*self.screen_distance_m
        self.pixels_per_degree = px_per_m*m_per_deg
        self.rad = lcfg.RADIUS_DEG
        self.line_width_px = lcfg.LINE_WIDTH_PX

    def deg2px(self,xdeg,ydeg):
        xpx = (self.x0_deg+xdeg)*self.pixels_per_degree
        ypx = (self.y0_deg+ydeg)*self.pixels_per_degree
        return xpx,ypx

    def set_position(self,xdeg,ydeg):
        if self.snap:
            xdeg = round(xdeg*self.step/self.small_step)*self.small_step
            ydeg = round(ydeg*self.step/self.small_step)*self.small_step
        self.x_deg = xdeg
        self.y_deg = ydeg
    
    def px2deg(self,xpx,ypx):
        xdeg = (xpx/self.pixels_per_degree)-self.x0_deg
        ydeg = (ypx/self.pixels_per_degree)-self.y0_deg
        return xdeg,ydeg
    
    def get_quadrant(self):
        hlist = ['NASAL','CENTER','TEMPORAL']
        vlist = ['SUPERIOR','CENTER','INFERIOR']
        def sign(num):
            if num==0:
                return 0
            elif num>0:
                return 1
            else:
                return -1
        hidx = int(sign(self.x_deg)*self.eye*self.hflip)+1
        vidx = int(sign(self.y_deg)*self.vflip)+1
        return hlist[hidx],vlist[vidx]
    
    def switch_eye(self):
        """Switch eye."""
        self.eye = self.eye*(-1)

    def __str__(self):
        if self.eye==RIGHT:
            eye = 'right'
        else:
            eye = 'left'

        hquad,vquad = self.get_quadrant()
        hq = hquad[0]
        vq = vquad[0]
            
        outlist = ['abs location (%0.3f,%0.3f)'%(self.x_deg,self.y_deg),
                'ret location (%0.3f %s, %0.3f %s)'%(abs(self.x_deg),hq,abs(self.y_deg),vq),
                'offset (%0.3f,%0.3f)'%(self.x0_deg,self.y0_deg),
                'eye %s'%eye]
        return '\n'.join(outlist)

    def msg_abs_location(self):
        return '%0.3f,%0.3f (abs)'%(self.x_deg,self.y_deg)


    def msg_log_entry(self):
        if self.eye==RIGHT:
            eye = 'right'
        else:
            eye = 'left'

        hquad,vquad = self.get_quadrant()
        hq = hquad[0]
        vq = vquad[0]

        return '%0.4f %s\t%0.4f %s\t%s eye'%(abs(self.x_deg),hq,abs(self.y_deg),vq,eye)
        
    def msg_ret_location(self):
        if self.eye==RIGHT:
            eye = 'right'
        else:
            eye = 'left'

        hquad,vquad = self.get_quadrant()
        hq = hquad[0]
        vq = vquad[0]

        return '%0.4f %s, %0.4f %s (%s eye)'%(abs(self.x_deg),hq,abs(self.y_deg),vq,eye)
        
    def msg_offset_location(self):
        return 'offset (%0.4f,%0.4f)'%(self.x0_deg,self.y0_deg)

    
    def get_lines(self):
        lines = []
        for theta in range(0,180,45):
            line = []
            theta_rad = float(theta)/180.0*math.pi
            x1 = self.rad*math.sin(theta_rad)+self.x_deg
            y1 = self.rad*math.cos(theta_rad)+self.y_deg
            x2 = self.rad*math.sin(theta_rad+math.pi)+self.x_deg
            y2 = self.rad*math.cos(theta_rad+math.pi)+self.y_deg
            x1px,y1px = self.deg2px(x1,y1)
            x2px,y2px = self.deg2px(x2,y2)
            lines.append([(x1px,y1px),(x2px,y2px)])
        return lines

    def get_circle(self):
        x,y = self.deg2px(self.x_deg,self.y_deg)
        rad = self.center_rad*self.pixels_per_degree
        return int(x),int(y),int(rad)

    def get_offset_lines(self):
        lines = []
        for theta in range(0,180,90):
            line = []
            theta_rad = float(theta)/180.0*math.pi
            x1 = self.rad*math.sin(theta_rad)
            y1 = self.rad*math.cos(theta_rad)
            x2 = self.rad*math.sin(theta_rad+math.pi)
            y2 = self.rad*math.cos(theta_rad+math.pi)
            x1px,y1px = self.deg2px(x1,y1)
            x2px,y2px = self.deg2px(x2,y2)
            lines.append([(x1px,y1px),(x2px,y2px)])
        return lines
    
    def left(self):
        """Move full step."""
        self.x_deg = self.x_deg - self.step
    def right(self):
        """Move right full step."""
        self.x_deg = self.x_deg + self.step
    def up(self):
        """Move up full step."""
        self.y_deg = self.y_deg - self.step
    def down(self):
        """Move down full step."""
        self.y_deg = self.y_deg + self.step
        
    def small_left(self):
        """Move fine step."""
        self.x_deg = self.x_deg - self.small_step
    def small_right(self):
        """Move right fine step."""
        self.x_deg = self.x_deg + self.small_step
    def small_up(self):
        """Move up fine step."""
        self.y_deg = self.y_deg - self.small_step
    def small_down(self):
        """Move down fine step."""
        self.y_deg = self.y_deg + self.small_step
        
    def very_small_left(self):
        """Move very fine step."""
        self.x_deg = self.x_deg - self.very_small_step
    def very_small_right(self):
        """Move right very fine step."""
        self.x_deg = self.x_deg + self.very_small_step
    def very_small_up(self):
        """Move up very fine step."""
        self.y_deg = self.y_deg - self.very_small_step
    def very_small_down(self):
        """Move down very fine step."""
        self.y_deg = self.y_deg + self.very_small_step
        
    def offset_left(self):
        """Move offset."""
        self.x0_deg = self.x0_deg - self.offset_step
        self.write_offsets()
    def offset_right(self):
        """Move offset right."""
        self.x0_deg = self.x0_deg + self.offset_step
        self.write_offsets()
    def offset_up(self):
        """Move offset up."""
        self.y0_deg = self.y0_deg - self.offset_step
        self.write_offsets()
    def offset_down(self):
        """Move offset down."""
        self.y0_deg = self.y0_deg + self.offset_step
        self.write_offsets()
        
    def write_offsets(self):
        with open('offsets.txt','wb') as fid:
            fid.write('%0.3f\n'%self.x0_deg)
            fid.write('%0.3f\n'%self.y0_deg)
        
    def center(self):
        """Center target."""
        self.y_deg = 0.0
        self.x_deg = 0.0

    def center_offsets(self):
        """Center (zero) the offsets."""
        self.x0_deg = 0.0
        self.y0_deg = 0.0
        self.write_offsets()

    def increment_line_width(self):
        """Increase line width."""
        self.line_width_px+=1
        
    def decrement_line_width(self):
        """Decrease line width."""
        self.line_width_px-=1
        if self.line_width_px<1:
            self.line_width_px = 1

    def increase_radius(self):
        """Increase target radius."""
        self.rad+=self.small_step
        
    def decrease_radius(self):
        """Decrease target radius."""
        self.rad-=self.small_step
        
        
        
        
class Modstate:

    def __init__(self,state_string=''):
        self.ctrl = state_string.lower().find('ctrl')>-1
        self.shift = state_string.lower().find('shift')>-1
        self.alt = state_string.lower().find('alt')>-1
        self.any = state_string.lower().find('any')>-1
        
    def __str__(self):
        out = []
        if self.shift: out.append('shift')
        if self.alt: out.append('alt')
        if self.ctrl: out.append('ctrl')
        if self.any: out.append('any')
        if len(out):
            out = '_'.join(out)
        else:
            out = 'none'
        return out

    def __eq__(self,ms):
        return (self.ctrl==ms.ctrl and self.alt==ms.alt and self.shift==ms.shift) or self.any

    def update(self):
        mods = pygame.key.get_mods()
        self.ctrl = not (mods & pygame.KMOD_CTRL)==0
        self.alt = not (mods & pygame.KMOD_ALT)==0
        self.shift = not (mods & pygame.KMOD_SHIFT)==0
    

