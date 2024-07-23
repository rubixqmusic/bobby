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
                            (ShowDialog, ("Bobby, my man", {})),

                            # (EndCall,("world_map", {})),

                            # (Wait, (60, {})),
                            (ShowDialog, ("what's good, brother?", {})),
                            # (Wait, (60, {})),
                            (ShowDialog, ("just wanted to hop on a call real quick", {})),
                            (ShowDialog, ("so we could connect on a couple of things", {})),
                            (Wait, (80, {})),
                            (ShowDialog, ("...okay... so...", {})),
                            # (Wait, (60, {})),
                            (ShowDialog, ("Listen... I'm not going to sugar coat it...", {})),
                            # (Wait, (30, {})),
                            (ShowDialog, ("The numbers are in, and...", {})),
                            (Wait, (80, {})),
                            (ShowDialog, ("it's not looking good, okay?", {})),
                            # (Wait, (80, {})),
                            (ShowDialog, ("You're on thin fucking ice, Bobby", {})),
                            (ShowDialog, ("I NEED you to hit your fucking money quota", {})),
                            (Wait, (80, {})),
                            (GoTo, ("intro_explanation", {}))
                            ],
      "intro_explanation" : [
                            (ShowDialog, ("okay... so...", {})),
                            (Wait, (30, {})),
                            (ShowDialog, ("...here's what I'm thinking...", {})),
                            # (Wait, (80, {})),
                            (ShowDialog, ("We're giving you a new territory", {})),
                            (ShowDialog, ("and plenty of weapons, okay?", {})),
                            # (Wait, (80, {})),
                            (ShowDialog, ("it's very simple, Bobby", {})),
                            (ShowDialog, ("Do whatever it takes to hit your number", {})),
                            (Wait, (80, {})),
                            (ShowDialog, ("or you're a dead motherfucker.", {})),
                            (Wait, (60, {})),
                            (ShowDialog, ("Corporate is up my ass about getting more rare stones,", {})),
                            (ShowDialog, ("so try and collect as many of those as you can.", {})),
                            (Wait, (80, {})),
                            (ShowDialog, ("And for the love of god, Bobby...", {})),
                            # (Wait, (60, {})),
                            (ShowDialog, ("Please try not to destroy too much stuff", {})),
                            # (Wait, (60, {})),
                            (ShowDialog, ("and that includes innocent bystanders", {})),
                            (ShowDialog, ("we're getting tons of complaints to HR,", {})),
                            (ShowDialog, ("and thats bad", {})),
                            (Choice, ("Got it?", [["Yes", "intro_end"], ["No", "intro_no"]], {}))
                            ],
              "intro_no" :  [
                            (PlaySound, (DENY_SOUND,{})),
                            (Wait, (60, {})),
                            (ShowDialog, ("Goddammit, Bobby, I need you to pay attention", {})),
                            (GoTo, ("intro_explanation", {}))
                            ],
              "intro_end" : [
                            (PlaySound, (COIN_SOUND,{})),
                            (Wait, (80, {})),
                            (ShowDialog, ("Alright, Bobby", {})),
                            (ShowDialog, ("Gonna have a BIG day", {})),
                            # (Wait, (20, {})),
                            (ShowDialog, ("Time is money", {})),
                            # (Wait, (80, {})),
                            (ShowDialog, ("Get out there and make it happen", {})),
                            (Wait, (80, {})),
                            (ShowDialog, ("...", {})),
                            (Wait, (80, {})),
                            (ShowDialog, ("...or I'll fucking kill you", {})),
                            (Wait, (80, {})),
                            (EndCall,("world_map", {}))
                          ]
            }