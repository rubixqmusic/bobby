from src.entities.bobby.states.idle import Idle
from src.entities.bobby.states.falling import Falling
from src.entities.bobby.states.running import Running
from src.entities.bobby.states.wallslide import WallSlide
from src.entities.bobby.states.jumping import Jumping
from src.entities.bobby.states.pivot import Pivot

player_states = {
                    "idle" : Idle,
                    "falling" : Falling,
                    "running" : Running,
                    "wall_slide" : WallSlide,
                    "jumping" : Jumping,
                    "pivot" : Pivot   
}