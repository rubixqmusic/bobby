
from src.screens import worldmap, playinglevel
from src.screens.videocallcutscene import videocallcutscene
from src.screens.fileselectscreen import fileselectscreen
from src.screens.initscreen import init
from src.screens.settingsscreen import settingsscreen
from src.screens.splashscreen import splashscreen
from src.screens.titlescreen import titlescreen


screens = {
                "init" : init.Init,
                "splashscreen" : splashscreen.Splashscreen,
                "title_screen" : titlescreen.TitleScreen,
                "settings_screen" : settingsscreen.SettingsScreen,
                "file_select_screen" : fileselectscreen.FileSelectScreen,
                "video_call_cutscene" : videocallcutscene.VideoCallCutscene,
                "world_map" : worldmap.WorldMap,
                "playing_level" : playinglevel.PlayingLevel,
                }