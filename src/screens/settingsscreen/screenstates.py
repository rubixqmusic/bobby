from src.screens.settingsscreen.states.fadein import FadeIn
from src.screens.settingsscreen.states.gototitlescreen import GoToTitleScreen
from src.screens.settingsscreen.states.selectsetting import SelectSetting
from src.screens.settingsscreen.states.displaysettings import DisplaySettings

settings_screen_states = {
                            "fade_in" : FadeIn,
                            "go_to_title_screen" : GoToTitleScreen,
                            "select_setting" : SelectSetting,
                            "display_settings" : DisplaySettings
                        }