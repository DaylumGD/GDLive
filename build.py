import os
import devutils
import atexit
import jsonapis
import xmltodict
import shutil

import zlib
import base64

appdata_directory: None
local_levels: None

class Decrypt:
    def Xor(path, key):
        data = devutils.quick_read(path, 'rb')
        res = []
        for i in data:
            res.append(i^key)
        return bytearray(res).decode()
 
    def Decrypt(data):
        return zlib.decompress(base64.b64decode(data.replace('-','+').replace('_','/').encode())[10:], -zlib.MAX_WBITS)

def define_settings():
    global appdata_directory, local_levels
    jsonfile = jsonapis.load_json_file('json/settings.json')['gd-settings']
    appdata_directory = jsonfile['directory-appdata']
    local_levels = jsonfile['local-levels']

def parse_savefile(file: str) -> dict:
    shutil.copyfile(file, 'cclocallevels.dat')
    
    res = Decrypt.Xor('cclocallevels.dat', 11)
    fin = Decrypt.Decrypt(res)
    devutils.quick_write('cclocallevels.dat', fin, 'wb')
    
    xml_file = devutils.quick_read('cclocallevels.dat')
    return xmltodict.parse(xml_file)

def build_collab(level: str, build: str):
    load_collab = devutils.quick_read(f'collabs/{level}.dat')
    savefile_json = parse_savefile(f'{appdata_directory}/{local_levels}')
    
    for i in range(0, len(savefile_json['plist']['dict']['d'][0]['d'])):
        if savefile_json['plist']['dict']['d'][0]['d'][i]['s'][0] == build:
            savefile_json['plist']['dict']['d'][0]['d'][i]['s'][1] = load_collab
            break
    devutils.quick_write(f'{appdata_directory}/{local_levels}', xmltodict.unparse(savefile_json))
    os.remove('cclocallevels.dat')

def encode_level(data: bytes) -> bytes:
    compressed_data = zlib.compress(data, level=zlib.Z_BEST_COMPRESSION)
    prefixed_data = b'\x00' * 10 + compressed_data
    base64_encoded = base64.b64encode(prefixed_data)
    modified_base64_encoded = base64_encoded.decode().replace('+', '-').replace('/', '_')
    return modified_base64_encoded