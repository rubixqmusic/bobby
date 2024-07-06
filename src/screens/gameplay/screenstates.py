from src.screens.gameplay.states.loadscene import LoadScene
from src.screens.gameplay.states.moneyintransition import MoneyInTransition
from src.screens.gameplay.states.levelactive import LevelActive

level_states = {
                "load_scene" : LoadScene,
                "money_in_transition" : MoneyInTransition,
                "level_active" : LevelActive
                }