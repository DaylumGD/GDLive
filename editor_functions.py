import os

class unit_conversions:
    def __init__(self, units: int):
        self.stdunits = units * 100
    
    @property
    def to_stdunits(self):
        return self.stdunits / 30

class SavedObjectsFolder:
    def __init__(self): ...
    
    def save_object(self, objects: list[str], name: str, folder: str|None=None):
        if folder == None: directory = f'data/saved-objects/{name}.dat'
        else: directory = f'data/saved-objects/{folder}/{name}.dat'
        with open(directory, 'w') as file:
            file.write(','.join(objects))
    
    def delete_object(self, name: str, folder: str|None=None):
        if folder == None: directory = f'data/saved-objects/{name}.dat'
        else: directory = f'data/saved-objects/{folder}/{name}.dat'
        os.remove(directory)
    
    def save_folder(self, folder: str):
        os.mkdir(f'data/saved-objects/{folder}')
    
    def delete_folder(self, folder: str):
        for file in os.listdir(f'data/saved-objects/{folder}'):
            file = file.removesuffix('.dat')
            self.delete_object(file, folder)
        os.rmdir(f'data/saved-objects/{folder}')