import pygame
import pygame_gui
import tkinter
import atexit
import base64
import zlib
import devutils
import ctypes
import subprocess
import os

# constants
SCREEN_SIZE = (ctypes.windll.user32.GetSystemMetrics(0), ctypes.windll.user32.GetSystemMetrics(1))

class base_functions:
    def general_encryption(self, data: str) -> bytes:
        cc = base64.b64encode(data.encode())
        cc = zlib.compress(cc, wbits=zlib.MAX_WBITS)
        return cc
    
    def general_decryption(self, data: bytes) -> str:
        cc = zlib.decompress(data, wbits=zlib.MAX_WBITS)
        cc = base64.b64decode(cc)
        return cc.decode()
    
    def atexit_functions(self):
        fb_sdk = devutils.quick_read('json/firebase.json')
        devutils.quick_write('json/firebase.json', self.general_encryption(fb_sdk), 'wb')
    
    def livedecode(self):
        fb_sdk = devutils.quick_read('json/firebase.json', 'rb')
        devutils.quick_write('json/firebase.json', self.general_decryption(fb_sdk))

class window_functions:
    def ajust_coordinates(self, coordinates: list|tuple) -> tuple|list:
        if type(coordinates) == "<class 'tuple'>":
            return ((SCREEN_SIZE[0]/1536)*coordinates[0], (SCREEN_SIZE[1]/864)*coordinates[1])
        else:
            return [(SCREEN_SIZE[0]/1536)*coordinates[0], (SCREEN_SIZE[1]/864)*coordinates[1]]
    
    def ajust_rect(self, rect: tuple[tuple, tuple]|list[list, list]) -> tuple[tuple, tuple]|list[list, list]:
        if type(rect) == "<class 'tuple'>":
            return (self.ajust_coordinates(rect[0]), self.ajust_coordinates(rect[1]))
        else:
            return [self.ajust_coordinates(rect[0]), self.ajust_coordinates(rect[1])]

# init
base_functions().livedecode()
pygame.init()

import backend
import build
import defines
import settings
import textures
import random
import interface

base_functions().atexit_functions()

class functions:
    def sysquit(self):
        exit(0)
    
    def quit_and_launch(self):
        subprocess.call(f'{settings.settings.gd_settings.directory_main}/GeometryDash.exe')
        exit(0)
    
    def read_license(self):
        os.system('notepad "License.txt"')
    
    def read_readme(self):
        os.system('notepad "readme.rst"')
    
    def read_EULA(self):
        os.system('notepad "EULA.rst"')
    
    def read_security(self):
        os.system('notepad "security.md"')

# window
window = pygame.display.set_mode(SCREEN_SIZE)
clock = pygame.time.Clock()
runtime = True
page = 1

# values
random_background = str(random.randint(1, 59))
if int(random_background) < 10:
    random_background = f'0{random_background}'

def main_menu():
    background = pygame.image.load(textures.get_background_texture(f'game_bg_{random_background}_001'))
    title = pygame.image.load('assets/GDLive_Name.png')
    
    # blits
    window.blit(background, (0, 0))
    window.blit(title, window_functions().ajust_coordinates((500, 60)))
    

while runtime == True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            runtime = False
    
    if page == 1:
        main_menu()
    
    pygame.display.flip()
    clock.tick(60)