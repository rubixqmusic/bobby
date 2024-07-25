from src.screens.videocallcutscene.states.choice import Choice
from src.screens.videocallcutscene.states.endcall import EndCall
from src.screens.videocallcutscene.states.goto import GoTo
from src.screens.videocallcutscene.states.playmusic import PlayMusic
from src.screens.videocallcutscene.states.playsound import PlaySound
from src.screens.videocallcutscene.states.setbackgroundimage import SetBackgroundImage
from src.screens.videocallcutscene.states.setcharacteranimation import SetCharacterAnimation
from src.screens.videocallcutscene.states.videocallringing import VideoCallRinging
from src.screens.videocallcutscene.states.wait import Wait
from src.screens.videocallcutscene.states.showdialog import ShowDialog

from src.screens.videocallcutscene.resources import *

cutscenes = {
                "intro_1" : [
                            (VideoCallRinging, {}),
                            (PlayMusic, (BACKGROUND_MUSIC, MUSIC_VOLUME, {})),
                            (SetBackgroundImage, (1,BEACH_BACKGROUND_PATH, {})),
                            (SetBackgroundImage, (2,OFFICE_BACKGROUND_PATH, {})),
                            (SetCharacterAnimation, (1, BOSS_VIDEO_CALL_SPRITESHEET_PATH, BOSS_VIDEO_CALL_ANIMATION_PATH, "idle", {})),
                            (SetCharacterAnimation, (2, BOBBY_OFFICE_SPRITESHEET_PATH, BOBBY_OFFICE_ANIMATION_PATH, "idle", {})),
                            (Wait, (80, {})),
                            # (ShowDialog, ("This is a test string to test how long we can print text before a fuck up happens", {})),
                            (ShowDialog, ("Bobby, my man", {})),
                            (ShowDialog, ("what's good, brother?", {})),
                            (ShowDialog, ("just wanted to hop on a quick call to say welcome to The Team!", {})),
                            (ShowDialog, ("we're excited to have you on board.", {})),
                            (ShowDialog, ("Everyone on The Team is a KILLER,", {})),
                            (ShowDialog, ("and we know you're gonna be one too", {})),
                            (Wait, (80, {})),
                            (ShowDialog, ("Alright, Bobby, Let's cut to the chase,", {})),
                            (GoTo, ("intro_explanation", {}))
                            ],
      "intro_explanation" : [
                            (ShowDialog, ("here's how it works around here:", {})),
                            (ShowDialog, ("Your #1 priority is getting money.", {})),
                            (ShowDialog, ("We're giving you a territory", {})),
                            (ShowDialog, ("We're giving you powerups", {})),
                            (ShowDialog, ("We're giving you weapons to take out the competition", {})),
                            (ShowDialog, ("it's very simple, Bobby:", {})),
                            (ShowDialog, ("Do whatever it takes to hit your number,", {})),
                            (ShowDialog, ("or you're a dead motherfucker.", {})),
                            (Wait, (80, {})),
                            (ShowDialog, ("Oh, and one more thing...", {})),
                            (ShowDialog, ("Please try not to destroy too much stuff,", {})),
                            (ShowDialog, ("and that includes innocent bystanders.", {})),
                            (ShowDialog, ("We've been getting tons of complaints to HR,", {})),
                            (ShowDialog, ("and thats bad", {})),
                            (Choice, ("Got it?", [["Yes", "intro_end"], ["No", "intro_no"]], {}))
                            ],
              "intro_no" :  [
                            (PlaySound, (DENY_SOUND,{})),
                            (Wait, (60, {})),
                            (ShowDialog, ("Goddammit, Bobby, I need you to pay attention.", {})),
                            (GoTo, ("intro_explanation", {}))
                            ],
              "intro_end" : [
                            (PlaySound, (COIN_SOUND,{})),
                            (Wait, (80, {})),
                            (ShowDialog, ("Alright, Bobby,", {})),
                            (ShowDialog, ("we're gonna have you complete a quick orientation.", {})),
                            (ShowDialog, ("After that, it's all you.", {})),
                            (ShowDialog, ("Get out there and make it happen...", {})),
                            (Wait, (80, {})),
                            (ShowDialog, ("...or I'll fucking kill you", {})),
                            (Wait, (80, {})),
                            (EndCall,("world_map", {}))
                          ]
            }