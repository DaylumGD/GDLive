import pygame
import jsonapis
from typing import Any

def draw_hitbox(x: int, y: int, endx: int, endy: int, event, callback):
    rect = pygame.Rect(x, y, endx, endy)
    if rect.collidepoint(pygame.mouse.get_pos()) == True:
        if event.type == pygame.MOUSEBUTTONDOWN:
            callback()

def get_editor_object(objectid: str) -> dict[str]:
    return jsonapis.load_json_file('interface/editor-objects.json')[objectid]

def get_ui_setting(catagory: str, setting: str) -> Any:
    return jsonapis.load_json_file('interface/ui-settings.json')[catagory][setting]