import logging

import pygame
import re

tJump = [
    [
        i - 1 if i != 0 else 0 for i in range(10)
    ]
]


class inputBox:

    def __init__(self, x, y, width, height, text=''):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = pygame.Color('dodgerblue2')
        self.text = text
        self.text_rendered = pygame.font.Font(None, 32).render(text, True, self.color)

    def handle_event(self, event):
        symbol = event.unicode
        if bool(re.search('[а-яА-Я]', symbol)):
            if self.text == 'Введите команду':
                self.text = ''
            self.text += symbol
            self.text_rendered = pygame.font.Font(None, 32).render(self.text, True, self.color)

    def draw(self, screen):
        surface = pygame.Surface((770, 50))
        surface.fill((0, 0, 0))
        screen.blit(surface, (30, 30))

        pygame.draw.rect(screen, self.color, self.rect, 2)
        screen.blit(self.text_rendered, (30, 30))

    def backspace(self):
        self.text = self.text[:-1]
        self.text_rendered = pygame.font.Font(None, 32).render(self.text, True, self.color)

    def clean(self):
        self.text = ''
        self.text_rendered = pygame.font.Font(None, 32).render(self.text, True, self.color)


class Robot:
    x = 5
    y = 5
    color = pygame.Color('dodgerblue2')
    current_cond = "вверх"

    fin = \
        {"влево": {  # действие
            "вверх": "влево",  # переход
            "вниз": "вправо",
            "вправо": "вверх",
            "влево": "вниз"
        },
            "вправо": {
                "вверх": "вправо",
                "вниз": "влево",
                "вправо": "вниз",
                "влево": "вверх"
            },
            "вниз": {
                "вверх": "вниз",
                "вниз": "вверх",
                "вправо": "влево",
                "влево": "вправо"
            },
            "вперед": {
                "вверх": (0, -1),
                "вниз": (0, 1),
                "вправо": (1, 0),
                "влево": (-1, 0)
            }
        }

    def move(self, text):
        cond = ''
        for sym in text:
            cond += sym

        if cond in self.fin.keys():
            self.proc_chain(cond)

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (782 + self.x * 108, self.y * 108 - 54), 20)
        x1 = (0, 0)
        x2 = (0, 0)
        x3 = (0, 0)
        if self.current_cond == "вверх":
            x1 = (728 + self.x * 108, self.y * 108)
            x2 = (836 + self.x * 108, self.y * 108)
            x3 = (782 + self.x * 108, self.y * 108 - 108)
        if self.current_cond == "вниз":
            x1 = (728 + self.x * 108, self.y * 108 - 108)
            x2 = (836 + self.x * 108, self.y * 108 - 108)
            x3 = (782 + self.x * 108, self.y * 108)

        if self.current_cond == "вправо":
            x1 = (728 + self.x * 108, self.y * 108 - 108)
            x2 = (728 + self.x * 108, self.y * 108)
            x3 = (836 + self.x * 108, self.y * 108-54)

        if self.current_cond == "влево":
            x1 = (836 + self.x * 108, self.y * 108 - 108)
            x2 = (836 + self.x * 108, self.y * 108)
            x3 = (728 + self.x * 108,self.y * 108-54)

        pygame.draw.polygon(screen, self.color, (x1, x2, x3))

    def proc_chain(self, cond):
        if cond == "вперед":
            move = self.fin["вперед"][self.current_cond]
            self.x += move[0]
            self.y += move[1]
        else:
            self.current_cond = self.fin[cond][self.current_cond]


def draw_field(screen):
    field = pygame.Rect(836, 0, 1080, 1080)
    pygame.draw.rect(screen, (255, 255, 255), field, 4)
    for i in range(10):
        pygame.draw.line(screen, (255, 255, 255), [836 + i * 108, 0], [836 + i * 108, 1080], 2)
        pygame.draw.line(screen, (255, 255, 255), [836, i * 108], [1920, i * 108], 1)
