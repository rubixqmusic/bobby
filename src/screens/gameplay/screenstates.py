from src.screens.gameplay.states.loadscene import LoadScene
from src.screens.gameplay.states.moneyintransition import MoneyInTransition
from src.screens.gameplay.states.levelactive import LevelActive
from src.screens.gameplay.states.pausemenu import PauseMenu
from src.screens.gameplay.states.returntotitlescreen import ReturnToTitleScreen
from src.screens.gameplay.states.returntoworldmap import ReturnToWorldMap

level_states = {
                "load_scene" : LoadScene,
                "money_in_transition" : MoneyInTransition,
                "level_active" : LevelActive,
                "pause_menu" : PauseMenu,
                "return_to_title_screen" : ReturnToTitleScreen,
                "return_to_world_map" : ReturnToWorldMap
                }