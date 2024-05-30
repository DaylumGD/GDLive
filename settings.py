import jsonapis
from dataclasses import dataclass

__json_build__settings__ = jsonapis.load_json_file('json/settings.json')
__json_build__usersettings__ = jsonapis.load_json_file('json/user-settings.json')

@dataclass
class settings:
    @dataclass
    class gd_settings:
        directory_appdata: str = __json_build__settings__['gd-settings']['directory-appdata']
        directory_main: str = __json_build__settings__['gd-settings']['directory-main']
        cclocallevels: str = __json_build__settings__['gd-settings']['local-levels']
    
    texture_res: str = __json_build__settings__['texture-res']

@dataclass
class user_settings:
    username: str = __json_build__usersettings__['username']
    password: str = __json_build__usersettings__['password']