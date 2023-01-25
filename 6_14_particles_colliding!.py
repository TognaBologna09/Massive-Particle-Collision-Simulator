# -*- coding: utf-8 -*-
"""
Created on Mon Jun 14 00:43:59 2021

@author: awgiu
"""

# -*- coding: utf-8 -*-
"""
Created on Sun Jun 13 15:44:27 2021

@author: awgiu
"""


# pygame kinetic theory of gases attempt #4 

import numpy as np

import pygame,sys 

# mass particle object asset tools
class MassParticle:
    """this is a class for a mass particle, using numpy libraries"""
    
    def __init__(self, mass, x, y, radius, vx, vy, color):
        
        self.mass = mass;
        self.x = x
        self.y = y
        self.radius = radius
        self.vx = vx
        self.vy = vy
        self.color = color
    
    def move(self, centercoord, delta_pos, radius, constraint):
        """This function moves the particle"""
        # center is updated by new position in x, or y coordinate frame 
        centercoord += delta_pos 
    
        # bounce conditions... 
    
        #should the center go below its radius (boundary is below constraint in x,y)
        if centercoord < radius: 
        # center is unchanged, but the new position is its radius
            centercoord, delta_pos = radius, -delta_pos
            # and its position is negative to fit into the game_window
        # should the center reach its constraint minus its radius (boundary is above constraint in x,y)
        if centercoord > constraint - radius: 
        # update the new position,velocity making it negative to match game_window frame
            centercoord, delta_pos = constraint - radius, -delta_pos   
           
        return centercoord, delta_pos     
    
    def update_move(self, X,Y, VX,VY):
        """Function modifies itself to the new parameters"""
        
        self.x = X
        self.y = Y
        self.vx = VX
        self.vy = VY
        # class object is updated!
        
    def unit_vectorize(self, u1, u2, q1, q2):
        """This function turns the input parameters to a 2D unit vector"""
        
        vectoru, vectorq = u2 - u1, q2 - q1
        mag = np.sqrt(vectoru**2 + vectorq**2)
        if mag == 0:
            return pygame.math.Vector2(vectoru, vectorq)
        else:
            unit_vector = pygame.math.Vector2(vectoru, vectorq)/mag
        
        return unit_vector

# using the two classes to create the sim
import random
# generating random example
randposx,randposy = random.randint(0,100),random.randint(0,100)
randvx = random.randint(-10,10)
randvy = np.sqrt(100 - randvx**2) 
masspart = MassParticle(1, randposx, randposy, 10, randvx, randvy, (255,0,0))

rmovex,rmovevx = masspart.move(randposx, randvx, masspart.radius, 100)
rmovey,rmovevy = masspart.move(randposy, randvy, masspart.radius, 100)

randposvec = masspart.unit_vectorize(randposx, rmovex, randposy, rmovey)
randvelvec = masspart.unit_vectorize(randvx, rmovevx, randvy, rmovevy)

# another one
randposx2,randposy2 = random.randint(0,100),random.randint(0,100)
randvx2 = random.randint(-10,10)
randvy2 = np.sqrt(100 - randvx2**2)
# masspart2 = MassParticle(1, randposx, randposy, 10, randvx2, randvy2, (0,0,255))


print(randposvec)
print(randvelvec)



# random gas needs random library
def game():
    
    # intialize pygame
    pygame.init()
    # now using pygame class to define window
    size = width,height = round(900),round(730)
    window = pygame.display.set_mode(size)
    
    clock = pygame.time.Clock()
    
    # fps counter
    font = pygame.font.SysFont("Arial", 20)
    def update_fps():
        fps = str(int(clock.get_fps()))
        fps_text = font.render(fps, 1, (255,0,0) )
        return fps_text
    
    # useful color codes RGB
    black = 0, 0, 0
    red = 255, 51 ,51
    orange = 255, 178, 102
    yellow = 255, 255, 69
    green = 153, 255, 51
    greenblue = 51, 255, 178
    cyan = 51, 255, 255
    blue = 51, 153, 255
    purple = 190, 150, 255
    pink = 255, 153, 204
    teal = 0, 128, 128
    gray = 224, 224, 224
    darkgray = 64, 64, 64
    color_list = [red, orange, yellow, green, greenblue, cyan, blue, purple, pink, teal]
    
    # storing particles in a list
    particle_list =[]
    
    # collision counter 
    hit_count = 0
    
# creating the game loop
    while 1:
        
        # tick the clock
        clock.tick(60)
        # but update the counter
        fps_count = update_fps()
        
        # now observe events
        for event in pygame.event.get():
            
            # enabling quit condition
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                break
            
            # # user end functions
            elif event.type == pygame.KEYDOWN:
                
                # Spacebar
                if event.key == pygame.K_SPACE:
                    randvx = random.uniform(-1,1)
                    randvy = np.sqrt(1 - randvx**2)
                    particle_list.insert(0, MassParticle(0.25, round(np.random.randint(0,width)), round(np.random.randint(0,height)), 4, randvx, randvy, random.choice(color_list) ) ) 
                    print('Spacebar! new particle list length :'+ str(len(particle_list)) )
        
        #bg color
        window.fill((80,80,52))
        
        # move the particles
        
        # 
        ignore_list = []
        
        for i1,mp1 in enumerate(particle_list):
            
            if i1 in ignore_list:
                pass
            
            # moving vars
           
            # move_vec1 = mp1.unit_vectorize(movex1, mp1.x, movey1, mp1.y)
            # vel_vec1 = mp1.unit_vectorize(movevx1, mp1.vx, movevy1, mp1.vy)
            # print('checking for collisions...')
            
            # checking vars for collisions
            if len(particle_list) ==1:
                
                # print('solo particle.')
                # print(i1)
                movex1,movevx1 = mp1.move(mp1.x, mp1.vx, mp1.radius, width)
                movey1,movevy1 = mp1.move(mp1.y, mp1.vy, mp1.radius, height)
                
                # mp1.x,mp1.vx = movex1, movevx1
                # mp1.y,mp1.vy = movey1, movevy1
                mp1.update_move(movex1,movey1,movevx1,movevy1)
                
            elif len(particle_list)>1:
                # print('multiple particles.')
                for i2,mp2 in enumerate(particle_list):
                    # can't collide with itself
                    if i1==i2:
                        pass
                    else:
                        # print(i1,i2)
                        movex1,movevx1 = mp1.move(mp1.x, mp1.vx, mp1.radius, width)
                        movey1,movevy1 = mp1.move(mp1.y, mp1.vy, mp1.radius, height)
                        
                        r1 = np.zeros(2)
                        r1[0],r1[1] = movex1,movey1 
                        v1 = np.zeros(2)
                        v1[0],v1[1] = movevx1,movevy1
                        # generate projected move for next particle
                        movex2,movevx2 = mp2.move(mp2.x, mp2.vx, mp2.radius, width)
                        movey2,movevy2 = mp2.move(mp2.y, mp2.vy, mp2.radius, height)
                        
                        r2 = np.zeros(2)
                        r2[0],r2[1] = movex2,movey2
                        v2 = np.zeros(2)
                        v2[0],v2[1] = movevx2,movevy2
                        
                        # move_vec2 = mp2.unit_vectorize(movex2, mp2.x, movey2, mp2.y)
                        # vel_vec2 = mp2.unit_vectorize(movevx2, mp2.vx, movevy2, mp2.vy)
                        
                        if movex1 + mp1.radius + mp2.radius > movex2 and movex1 < movex2 + mp1.radius + mp2.radius and movey1 + mp1.radius + mp2.radius > movey2 and movey1 < movey2 + mp1.radius + mp2.radius:
                            
                            ## really near each other
                            
                            distsq = (movex2-movex1)**2 + (movey2 - movey1)**2
                            overlap_dist = mp1.radius**2 + mp2.radius**2
                            
                            if distsq > overlap_dist: 
                            # print('too far.')
                            
                            # no possible collision
                            
                            
                            # mp1.x,mp1.vx = movex1,movevx1
                            # mp1.y,mp1.vy = movey1,movevy1
                            
                            # mp2.x,mp2.vx = movex2,movevx2
                            # mp2.y,mp2.vy = movey2,movevy2
                                far = 1
                                # ignore_list.append(mp1)
                                # ignore_list.append(mp2)
                                
                            elif distsq <= overlap_dist:
                                
                                hit_count+=1
                                print('hit! -->'+str(hit_count))
                                
                                #current_sep_vec = pygame.math.Vector2(mp1.x-mp2.x, mp1.y-mp2.y)
                                
                                # update velocity vector 1
                                # newvel_vec = vel_vec1 - current_sep_vec*(2*mp2.mass/(mp1.mass+mp2.mass)*np.dot(vel_vec1,current_sep_vec)/distsq
                                             
                                ## INELASTIC COLLISIONS ###
                                new_v2 = v1 - (2*mp2.mass/(mp1.mass+mp2.mass))*np.dot(v1-v2,r1-r2)/np.dot(r1-r2,r1-r2)*(r1-r2)
                                # new_v1 = v2 - (2*mp1.mass/(mp1.mass+mp2.mass))*np.dot(v2-v1,r2-r1)/np.dot(r2-r1,r2-r1)*(r1-r2)
                                #
                                nmovex1,nmovevx1 = mp1.move(mp1.x, new_v2[0], mp1.radius, width)
                                nmovey1,nmovevy1 = mp1.move(mp1.y, new_v2[1], mp1.radius, height)
                                # 
                                # movex1,movevx1 = nmovex1,nmovevx1
                                # movey1,movevy1 = nmovey1,nmovevy1
                                movex1,movevx1 = mp1.x+nmovevx1*(1-np.sqrt(distsq/overlap_dist)),nmovevx1
                                movey1,movevy1 = mp1.y+nmovevy1*(1--np.sqrt(distsq/overlap_dist)),nmovevy1
                                
                                
                                ## 
                                nmovex2,nmovevx2 = mp2.move(mp2.x, new_v2[0], mp2.radius, width)
                                nmovey2,nmovevy2 = mp2.move(mp2.y, new_v2[1], mp2.radius, height)
                                
                                movex2,movevx2 = mp2.x + nmovevx2*(1-np.sqrt(distsq/overlap_dist)),nmovevx2
                                movey2,movevy2 = mp2.y + nmovevy2*(1-np.sqrt(distsq/overlap_dist)),nmovevy2
                
            ### LAST STEP ###
            ## from within the first for loop i1, mp1 ##
            
            # updating mp class object
            # mp1.x,mp1.vx = nmovex1,nmovevx1
            # mp1.y,mp1.vy = nmovey1,nmovevy1
            
            # mp2.x,mp2.vx = nmovex2,nmovevx2
            # mp2.y,mp2.vy = nmovey2,nmovevy2
            
            # gravity!
            g = 0.02
            movevy1 += g
            # storing the moved particles into a list
            # ignore_list.append(mp1)
            # ignore_list.append(mp2)
            
            # now update each particle at the end of initial list loop
            mp1.update_move(movex1,movey1,movevx1,movevy1)
                           
        ignore_list = []
                     
            # pygame.draw.circle(window, mp2.color, (round(mp2.x), round(mp2.y)), mp2.radius, int(mp2.radius/8))
        
        for i, mp1 in enumerate(particle_list):
            pygame.draw.circle(window, mp1.color, (round(mp1.x), round(mp1.y)), mp1.radius, int(mp1.radius/8))
        # fps counter
        window.blit(fps_count, (10,0))
        # display everything
        pygame.display.flip()

game()
