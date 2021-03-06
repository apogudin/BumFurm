from MyFunctions import *

#Майнер бомжей
class BusStation():
    def __init__(self, user):
        self.user = user
        self.tile_to_default()
        self.objects_dict = {}
        self.NxNy = [12,8]  #на сколько столбцов и строк резать изображение
        self.img = None
        self.lvl_list = [
        {'lvl': 1, 'cost': 0, 'bums':0, 'limit': 10, 'bps': 0.3, 'bum_cash': 0, 'draw_frame': 2, 'draw_col': 0},  #draw_col = номер группы из четырёх колонок для изменения изображения с уровнем
        {'lvl': 2, 'cost': 100, 'limit': 50, 'bps': 1, 'draw_col': 1},
        {'lvl': 3, 'cost': 1000, 'limit': 100, 'bps': 5, 'draw_col': 2},
        ]
        self.button_dict = [
            {
                'name': 'LEVEL',
                'action': self.lvl,
                'item': self,
            },
            {
                'name': 'GRAB',
                'action': self.GrabBums,
                'item': self,
            },
            ]
        self.button_dict_limited = [
            {
                'name': 'GRAB',
                'action': self.GrabBums,
                'item': self,
            },
            ]
        self.text_dict = {
            'info_screen': {
                'body': {
                    'alignment': 'left',
                    'text': ['Уровень: ', 'Бомжи: ', 'Предел бомжей: ']
                },
                'body_val': {
                    'alignment': 'right',
                    'attr': ['lvl', 'bums', 'limit']
                }
            },
            'info_annotation': {
                'header': {
                    'alignment': 'center',
                    'text': 'Остановка'
                },
                'text': {
                    'alignment': 'left',
                    'text': ['Место респауна бомжей. Прибывают до тех пор, пока не закончится место.']
                },
            },
            'shop_annotation': {
                'text': {
                    'alignment': 'left',
                    'text': ['Обычная такая автобусная остановка в трущобах, на которой любят скапливаться бомжи и обблёвывать всё вокруг.']
                },
            },
        }
        '''
        self.info_screen = [
        {'display_name': 'Уровень: ',
        'attr': 'lvl'},
        {'display_name': 'Бомжи: ',
        'attr': 'bums'},
        {'display_name': 'Предел бомжей: ',
        'attr': 'limit'},
        ]'''

    def tile_to_default(self):
        self.tile = [
        [1, 1, 1],
        [1, 1, 1],
        [0, 0, 0]
        ]
        self.pivot = [1,1]

    def SetNewID(self, item_id):
        self.objects_dict[item_id].update(self.lvl_list[0])
        if self not in self.user.property_list['EUR']:
            self.user.property_list['EUR'].append(self)

    def GrabBums(self, item_state):
        item_id = item_state['item_id']
        self.user.resources['bums'] += self.objects_dict[item_id]['bums']
        self.objects_dict[item_id]['bums'] = 0

    def lvl(self, item_state):
        new_lvl = self.objects_dict[item_state['item_id']]['lvl']
        self.objects_dict[item_state['item_id']].update(self.lvl_list[new_lvl])

    #Проходится по всем своим объектам, считает прибыль
    def resources_update(self):
        for ID in self.objects_dict:
            #По бомжам
            if self.objects_dict[ID]['bums'] < (self.objects_dict[ID]['limit'] - self.objects_dict[ID]['bum_cash'] - self.objects_dict[ID]['bps']):
                self.objects_dict[ID]['bum_cash'] += self.objects_dict[ID]['bps']
                self.objects_dict[ID]['bums'] += int((self.objects_dict[ID]['bum_cash'] // 1))
                self.user.resources['total_bums'] -= int((self.objects_dict[ID]['bum_cash'] // 1))
                self.objects_dict[ID]['bum_cash'] = self.objects_dict[ID]['bum_cash'] % 1
            elif self.objects_dict[ID]['bums'] < self.objects_dict[ID]['limit']:
                self.user.resources['total_bums'] -= int(self.objects_dict[ID]['limit'] - self.objects_dict[ID]['bums'])
                self.objects_dict[ID]['bums'] = self.objects_dict[ID]['limit']

            self.objects_dict[ID]['draw_frame'] = 2 + int(self.objects_dict[ID]['bums'] * 5 / self.objects_dict[ID]['limit'])


#Потребитель бомжей, майнер денег
class ShootingRange():
    def __init__(self, user):
        self.user = user
        self.tile_to_default()
        self.objects_dict = {}
        self.img = None
        self.lvl_list = [
        {'lvl': 1, 'cost': 0, 'bums':0, 'cps': 10, 'bps': 3, 'draw_frame': 2},
        {'lvl': 2, 'cost': 100, 'cps': 50, 'bps': 1},
        {'lvl': 3, 'cost': 1000, 'cps': 100, 'bps': 5},
        ]
        self.button_dict = [
            {
                'name': 'LEVEL',
                'action': self.lvl,
                'item': self,
            }
            ]
        self.button_dict_limited = []
        self.info_screen = [
        {'display_name': 'Уровень: ',
        'attr': 'lvl'},
        {'display_name': 'Прибыль: ',
        'attr': 'cps'},
        ]

        self.text_dict = {
            'info_screen': {
                'body': {
                    'alignment': 'left',
                    'text': ['Уровень: ', 'Прибыль: ']
                },
                'body_val': {
                    'alignment': 'right',
                    'attr': ['lvl', 'cps']
                }
            },
            'info_annotation': {
                'header': {
                    'alignment': 'center',
                    'text': 'Бомжетир'
                },
                'text': {
                    'alignment': 'left',
                    'text': ['Место потребления бомжей. Производим деньги, уменьшаем запас бомжей']
                },
            },
            'shop_annotation': {
                'text': {
                    'alignment': 'left',
                    'text': ['Короче, здесь запускаем в лес бомжей, а олигархи их отстреливают. Бомжей - меньше, олигархи - счатсливы и дают денег.']
                },
            },
        }

    def tile_to_default(self):
        self.tile = [
        [1, 1, 1],
        [0, 1, 1],
        [0, 0, 1]
        ]
        self.pivot = [1,1]

    def SetNewID(self, item_id):
        self.objects_dict[item_id].update(self.lvl_list[0])
        if self not in self.user.property_list['EUR']:
            self.user.property_list['EUR'].append(self)

    def lvl(self, item_state):
        new_lvl = self.objects_dict[item_state['item_id']]['lvl']
        self.objects_dict[item_state['item_id']].update(self.lvl_list[new_lvl])

    #Проходится по всем своим объектам, считает прибыль
    def resources_update(self):
        for ID in self.objects_dict:
            #По бомжам
            if self.user.resources['bums'] >= self.objects_dict[ID]['bps']:
                self.user.resources['coins'] += self.objects_dict[ID]['cps']
                self.user.resources['bums'] -= self.objects_dict[ID]['bps']

                #Сдвиг кадра в зависимости от наполнения
                self.objects_dict[ID]['draw_frame'] = 5

            else:
                self.objects_dict[ID]['draw_frame'] = 2




class Bum():
    #Все существующие бомжи#
    def __init__(self):
        self.cost = 10          #Цена одного бомжа
        self.amount = 0         #Количество свободных бомжей
        self.efficiency = 1     #Эффективность бомжей
        self.trash = 0          #Счётчик отработанных бомжей
    def buy(self):
        self.amount += 1
    def set(self):
        self.amount -= 1

class Coins():
    #Деньги игрока
    def __init__(self):
        self.amount = 20
    def income(self, sum):      #Прибыль
        self.amount += sum
    def outgo(self, sum):       #Расход
        self.amount -= sum

#Игровой процесс пользователя
class User():
    def __init__(self):
        self.population = 7444443881
        self.resources = {
            'total_bums': self.population,
            'coins': 0,
            'reputation': 0,
            'bums': 0,
            'text_list': ['coins', 'bums', 'reputation', 'total_bums'],
        }

        self.sum_coins = 0
        self.sum_bums_news_step = 10
        self.sum_coins_news_step = 10

        self.property_list = {
            'EUR': [],
        }

        self.text_dict = {
            'res_annotation': {
                'text': {
                    'alignment': 'left',
                    'text': []
                },
            },
        }

        self.texts = {
        'coins': ['Собственно, честно заработанные деньги. Можно тратить ни на что. Они просто есть. А у бомжей нет. Ха-ха.'],
        'bums': ['Это ваши честно заработанные бомжи. Можете распоряжаться ими, как обычными игровыми ресурсами. Вот типа есть мясо-золото-дерево, а это - бомжи.'],
        'reputation': ['Репутация. Неизвестно, зачем она сейчас нужна. Просто есть, чего бы нет. Пусть и нулевая.'],
        'total_bums': ['Население планеты, не являющееся бомжами. Задача - сделать бомжами всех. Для этого нужно много водки и автобусных остановок.'],
        }

    def get_news(self, news_obj):
        if self.population - self.resources['total_bums'] > self.sum_bums_news_step:
            news_obj.add_jobs('event2')
            #self.Worker.interface_state['news_event'] = 'event2'
            self.sum_bums_news_step += 50
        if self.sum_coins > self.sum_coins_news_step:
            #self.Worker.interface_state['news_event'] = 'event1'
            news_obj.add_jobs('event1')
            self.sum_coins_news_step += 50

#Просит все свои объекты посчитать поступления
    def resources_update(self):
        for country in self.property_list:
            for obj in self.property_list[country]:
                obj.resources_update()
