import math
import pygame
import os
import sys
from Objects import *
from MyFunctions import *
from Configs import *
import copy

class Pane():
    def __init__(self, area, grid=None):
        #для выбранного type высчитывает область: левый-верхний, правый-нижний угол
        PANE_LIST.append(self)
        self.pane = area
        self.grid_area = grid
        self.pane_type = type
        self.img = None
        self.screen = None
        self.user_map_place = None

    def Button_Init(self, button_list, NxNy, size = [100, 150], gap = [10,10]):
        self.button_list = button_list

        def Grid(size_x, size_y, Nx, Ny, gap_x, gap_y, grid_area):
            total_x = size[0]*NxNy[0] + gap[0]*(NxNy[0]-1)
            total_y = size[1]*NxNy[1] + gap[1]*(NxNy[1]-1)
            pane_x =  grid_area[1][0] - grid_area[0][0]
            pane_y =  grid_area[1][1] - grid_area[0][1]
            start_x = grid_area[0][0] + (pane_x/2 - total_x/2)
            start_y = grid_area[0][1] + (pane_y/2 - total_y/2)

            #Матрица Nx на Ny по центру области win_size,
            #где элементы - [Y][X][x,y] левого верхнего угла распологаемого объекта для позиции X, Y в матрице
            Grid = [[[start_x + i*(size[0] + gap[0]),start_y + j*(size[1]+gap[1])] \
            for i in range(NxNy[0])] for j in range(NxNy[1])]

            pos_x = Grid[grid_y][grid_x][0]
            pos_y = Grid[grid_y][grid_x][1]
            return [pos_x, pos_y]

        #Записываем в кнопки их координаты
        grid_x = 0
        grid_y = 0
        for button in button_list:
            i = button_list.index(button)
            if ((i+1)-(grid_y*NxNy[0])) > NxNy[0]:
                grid_x = 0
                grid_y += 1
            button.pos_x, button.pos_y = Grid(size[0], size[1], NxNy[0], NxNy[1], gap[0], gap[1], self.grid_area)
            button.pane = self.pane_type
            button.width = size[0]
            button.height = size[1]
            Append_To_Dict(BUTTON_DICT, self.pane_type, button)
            grid_x += 1

    def draw_Button(self):
        for button in self.button_list:
            button.draw()

    def draw_pane(self):
        Img_Fill(self.img, self.pane, self.screen)

    def IsOn (self, mouse_pos):
        if (self.pane[0][0] < mouse_pos[0] < self.pane[1][0]) :
            if (self.pane[0][1] < mouse_pos[1] < self.pane[1][1]):
                return True
        return False

    def get_size(self):
        return(self.pane)




class Pane_Map():
    def __init__():
        pass
    def Building_init(self):
        '''
        if self.pane_type == 'map':
            self.pane_width = self.grid_area[1][0] - self.grid_area[0][0]
            self.pane_height = self.grid_area[1][1] - self.grid_area[0][1]
            Nx = 8
            Ny = 6
            self.width = self.pane_width/Nx
            self.height = self.pane_height/Ny
            start_x = self.grid_area[0][0]
            start_y = self.grid_area[0][1]

            self.Map_Grid = [[[start_x + i*self.width, start_y + j*self.height]
            for i in range(Nx+1)] for j in range(Ny+1)]
            pos_x = None
            pos_y = None
            print(self.pane, self.Map_Grid)
            for i in range(1,Nx+1):
                if self.user_map_place[0] < self.Map_Grid[0][i][0]:
                    pos_x = self.Map_Grid[0][i-1][0]
                    break

            for j in range(1,Ny+1):
                if self.user_map_place[1] < self.Map_Grid[j][0][1]:
                    pos_y = self.Map_Grid[j-1][0][1]
                    break


            #инициализация кнопки
            for button in button_list:
                button.pos_x, button.pos_y = pos_x, pos_y
                button.pane = self.pane_type
                button.width = self.width
                button.height = self.height
                Append_To_Dict(BUTTON_DICT, self.pane_type, button)
        '''
        pass

    def Move():
        pass
    def Buildinf_draw(self):
        pass
    def bg_draw(self):
        pass


class Building():
    def __init__():
        pass
    def IsOn():
        pass
    def draw():
        pass
    def Activate():
        pass
    def size():
        pass
    def pos():
        pass

class Button():
    #Кнопки с любыми шрифтами, размерами, положением.
    def __init__(self, name, worker_act, item = ''):
        self.worker_act = worker_act
        self.name = name
        self.item = item
        self.state = 'off'
        self.img = None
        self.pos_x = None
        self.pos_y = None
        self.pane = None
        self.width = None
        self.height = None
        self.screen = None
        self.font = None

    def IsOn (self, mouse_pos):
        if (self.pos_x < mouse_pos[0] < self.pos_x + self.width) :
            if (self.pos_y < mouse_pos[1] < self.pos_y + self.height):
                self.state = 'on'
                return True
        self.state = 'off'
        return False

    def draw (self):
        text = self.font.render(self.name, True, [0,0,0])
        self.img.draw_Button(self.pos_x, self.pos_y, self.state)
        #Img_Fill(self.bg_draw,[[self.pos_x,self.pos_y],[self.pos_x+self.width, self.pos_y+self.height]], self.screen)
        self.screen.blit(text, (self.pos_x + (self.width/2 - text.get_width()/2), self.pos_y +(self.height/2 - text.get_height()/2)))

    def Activate(self):
        return self.worker_act(self)

    def size(self):
        return [self.width, self.height]

    def pos(self):
        return [self.pos_x, self.pos_y]


class Image():
    def __init__(self, image, object_list = [], folder = 'images'):
        IMAGE_LIST.append(self)
        self.img = pygame.image.load(os.path.join(folder,image))
        self.width = self.img.get_width()
        self.height = self.img.get_height()
        self.screen = None
        for obj in object_list:
            obj.img = self

    def draw(self, pos_x, pos_y, Nxy = [1,1], elem = [0,0]):
        crop_width = self.width/Nxy[0]
        crop_height = self.height/Nxy[1]
        crop_pos_x = crop_width*elem[0]
        crop_pos_y = crop_height*elem[1]
        self.screen.blit(self.img, [pos_x, pos_y],(crop_pos_x,crop_pos_y,crop_width,crop_height))


    def draw_Button(self, pos_x, pos_y, state):
        if state == 'off':
            elem = [0,0]
        elif state == 'on':
            elem = [0,1]
        self.draw(pos_x, pos_y, [1,2], elem)


    def fill(self, area):
        Img_Fill(area, self.screen)


class Actor ():
    def __init__(self):
        self.item = 'None'
        self.interface_group = 'None'
        self.map_mode = 'base'
        self.map_mode_switch = 'building'

    def switch(self, button):
        self.interface_group ="menu:" + button.pane
        self.item = button.item
        return self.interface_group

    def switch_map(self, button=None):
        self.map_mode,self.map_mode_switch = self.map_mode_switch, self.map_mode

    def buy(self, button):
        self.item.buy()

    def nothing(self, item=''):
        return


class Text():
    def __init__(self, font, pos_list, type = None):
        #либо указываем напрямую список позиций pos_list,
        #либо передаём список объектов и указываем их тип (для типов тут прописаны специфики расположения)
        TEXT_LIST.append(self)
        self.font = font
        self.screen = None

        self.obj_pos_list = [obj.pos() for obj in pos_list]
        self.obj_size_list = [obj.size() for obj in pos_list]

    def draw(self, text_list, event = None, duration = None):

        self.text_list = [self.font.render(text, True, [0,0,0]) for text in text_list]

        if type is None:
            self.pos_list = pos_list
        else:
            self.pos_list = []
            if type == 'head':
                pass
            elif type is not None:
                #Для любого указанного, но непрописанного type ставим по центру
                for i in range(len(self.text_list)):
                    self.pos_list.append([
                        self.obj_pos_list[i][0] + (self.obj_size_list[i][0]/2 - self.text_list[i].get_width()/2),
                        self.obj_pos_list[i][1] +(self.obj_size_list[i][1]/2 - self.text_list[i].get_height()/2)
                        ])

        for i in range(len(self.text_list)):
            self.screen.blit(self.text_list[i], self.pos_list[i])
        #for ... pos_list ... blit..
