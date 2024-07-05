from src.screens.worldmap.states.fadein import FadeIn
from src.screens.worldmap.states.loadmap import LoadMap
from src.screens.worldmap.states.mapactive import MapActive
from src.screens.worldmap.states.quitmenu import QuitMenu
from src.screens.worldmap.states.startlevel import StartLevel
from src.screens.worldmap.states.quittomainmenu import QuitToMainMenu

world_map_states = {
                    "fade_in" : FadeIn,
                    "load_map" : LoadMap,
                    "map_active" : MapActive,
                    "quit_menu" : QuitMenu,
                    "start_level" : StartLevel,
                    "quit_to_main_menu" : QuitToMainMenu
                    }