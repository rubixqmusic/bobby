from src.screens.settingsscreen.states.fadein import FadeIn
from src.screens.settingsscreen.states.gototitlescreen import GoToTitleScreen
from src.screens.settingsscreen.states.selectsetting import SelectSetting

settings_screen_states = {
                            "fade_in" : FadeIn,
                            "go_to_title_screen" : GoToTitleScreen,
                            "select_setting" : SelectSetting
                        }