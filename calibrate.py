import sys, pygame, math

pygame.init()

# print pygame.KMOD_NONE
# mods = pygame.key.get_mods()
# print bin(mods)
# sys.exit()
# if mods & pygame.KMOD_NUM:
#     sys.exit('Please turn off the NUM LOCK and try again.')
# if mods & pygame.KMOD_CAPS:
#     sys.exit('Please turn off the CAPS LOCK and try again.')
                
size = width, height = pygame.display.list_modes()[0]
black = 0, 0, 0
screen = pygame.display.set_mode(size)
myfont = pygame.font.SysFont('Times New Roman', 30)

points = []

running = True

while running:
    #clock.tick(30)
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
        elif event.type == pygame.MOUSEBUTTONUP:
            mousex,mousey = event.pos
            points.append((mousex,mousey))
            if len(points)==2:
                running = False

    screen.fill(black)

    # draw here

    msg_list = ['Please click two points separated by 3 inches,',
                    'the width of a standard post-it note.']
    for idx,msg in enumerate(msg_list):
        textsurface = myfont.render(msg, False, (255, 255, 255))
        screen.blit(textsurface,(0,0+idx*30))
        
    pygame.display.flip()
    
x1,y1 = points[0]
x2,y2 = points[1]
x1 = float(x1)
y1 = float(y1)
x2 = float(x2)
y2 = float(y2)

d = math.sqrt((y1-y2)**2+(x1-x2)**2)
dpi = d/3.0

f = open('./dpi.txt','w')
f.write('%0.1f'%dpi)
f.close()
