from src.screens.titlescreen.states.fadein import FadeIn
from src.screens.titlescreen.states.startgameorquit import StartGameOrQuit
from src.screens.titlescreen.states.pickgamemode import PickGameMode
from src.screens.titlescreen.states.gotofileselectscreen import GoToFileSelectScreen
from src.screens.titlescreen.states.gotosettingsscreen import GoToSettingsScreen
from src.screens.titlescreen.states.fadeoutandquit import FadeOutAndQuit

title_screen_states = {
                        "fade_in" : FadeIn,
                        "start_game_or_quit" : StartGameOrQuit,
                        "pick_game_mode" : PickGameMode,
                        "go_to_file_select_screen" : GoToFileSelectScreen,
                        "go_to_settings_screen" : GoToSettingsScreen,
                        "fade_out_and_quit" : FadeOutAndQuit
                        }