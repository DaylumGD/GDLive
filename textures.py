import plistlib
import settings

def get_texture(gamesheet: str, sprite: str) -> tuple[str, list[list[int, int], list[int, int]]]:
    if settings.settings.texture_res == None:
        suffix = gamesheet
    else:
        suffix = f'{gamesheet}-{settings.settings.texture_res}'

    with open(f'{settings.settings.gd_settings.directory_main}/Resources/{suffix}.plist', 'rb') as file:
        plist_document = plistlib.load(file)
        textureRect = plist_document['frames'][sprite]['textureRect']
        textureRect = textureRect.split('},{')
        
        textureRect[0] = textureRect[0].removeprefix('{{').split(',')
        textureRect[1] = textureRect[1].removesuffix('}}').split(',')
        
        textureRect[0][0] = int(textureRect[0][0])
        textureRect[0][1] = int(textureRect[0][1])
        textureRect[1][0] = int(textureRect[1][0])
        textureRect[1][1] = int(textureRect[1][1])
        
        return (f'{suffix}.png', textureRect)

def get_animation_texture(gamesheet: str, sprite: str, config: dict) -> list[list[list[int, int], list[int, int]]]:
    animation_array = []
    animation_array.append(config)
    
    for i in range(1, config['frames']):
        frame = get_texture(gamesheet, f'{sprite}_00{str(i)}.png')
        animation_array.append(frame[1])
    return animation_array

def get_background_texture(background_img: str):
    return f'{settings.settings.gd_settings.directory_main}/Resources/{background_img}-{settings.settings.texture_res}.png'

def load_font(text: str, font: str, keering: int):
    def trim_data(data: str, cc: bool):
        if cc == True:
            return data.split('="', 1)[1].removesuffix('"')
        else:
            return data.split('=', 1)[1]
    
    text_array = []
    for i in text: text_array.append(i)
    
    infomation = {
        'font-image': '',
        'char-encoding': 'utf-8',
        
        'size': 0,
        'bold': False,
        'ilactic': False,
        
        'characters': 0,
        'offset': 0
    }
    
    with open(f'{settings.settings.gd_settings.directory_main}/Resources/{font}-{settings.settings.texture_res}.fnt') as ff:
        font_file: list[str] = ff.read().split('\n')
        
        # get data
        lnsplit = font_file[0].split(' ')
        infomation['size'] = trim_data(lnsplit[2], False)
        infomation['bold'] = trim_data(lnsplit[3], False)
        infomation['ilactic'] = trim_data(lnsplit[4], False)
        lnsplit = font_file[2].split(' ')
        infomation['font-image'] = trim_data(lnsplit[2], True)
        lnsplit = font_file[3].split(' ')
        infomation['characters'] = int(trim_data(lnsplit[1], False))
        
        font_file.pop(0)
        font_file.pop(0)
        font_file.pop(0)
        font_file.pop(0)
        
        return_array = []
        
        for char in text_array:
            for fc in range(0, infomation['characters']):
                c = font_file[fc].split(' ')
                for i in enumerate(c):
                    if i[1] == '':
                        c.pop(i[0])
                for i in enumerate(c):
                    if i[1] == '':
                        c.pop(i[0])
                for i in enumerate(c):
                    if i[1] == '':
                        c.pop(i[0])
                
                if c[11] == f'letter="{char.capitalize()}"':
                    return_array.append([[int(c[2].removeprefix('x=')), int(c[3].removeprefix('y='))], [int(c[4].removeprefix('width=')), int(c[5].removeprefix('height='))]])
        
        distance = (return_array[0][1][1] - return_array[0][1][0]) - keering
        infomation['offset'] = distance
        return_array.insert(0, infomation)
        
        print(return_array)