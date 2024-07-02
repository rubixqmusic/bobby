from src.screens.videocallcutscenestates import VideoCallRinging, PlayMusic, SetBackgroundImage, PlaySound, Wait, SetCharacterAnimation, Choice, ShowDialog, GoTo, EndCall

BLANK_BACKGROUND_PATH = f"backgrounds/video_call_blank_background.png"
BEACH_BACKGROUND_PATH = f"backgrounds/video_call_beach_background.png"
OFFICE_BACKGROUND_PATH = f"backgrounds/video_call_office_background.png"

BOBBY_OFFICE_SPRITESHEET_PATH = f"video_call_cutscenes/bobby_in_office.png"
BOBBY_OFFICE_ANIMATION_PATH = f"bobby_in_office.json"

BOSS_VIDEO_CALL_SPRITESHEET_PATH = f"video_call_cutscenes/boss_video_call.png"
BOSS_VIDEO_CALL_ANIMATION_PATH = f"boss_video_call.json"

DENY_SOUND = f"deny.wav"
COIN_SOUND = f"coin.wav"

BACKGROUND_MUSIC = f"video_call.mp3"
MUSIC_VOLUME = 0.5

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

                            (EndCall,("world_map", {})),

                            (Wait, (60, {})),
                            (ShowDialog, ("what's good, brother?", {})),
                            (Wait, (60, {})),
                            (ShowDialog, ("just wanted to hop on a call real quick", {})),
                            (Wait, (60, {})),
                            (ShowDialog, ("so we could connect on a couple of things", {})),
                            (Wait, (80, {})),
                            (ShowDialog, ("...okay... so...", {})),
                            (Wait, (60, {})),
                            (ShowDialog, ("Listen... I'm not going to sugar coat it...", {})),
                            (Wait, (30, {})),
                            (ShowDialog, ("The numbers are in, and...", {})),
                            (Wait, (80, {})),
                            (ShowDialog, ("it's not looking good", {})),
                            (Wait, (80, {})),
                            (ShowDialog, ("You're on thin fucking ice, Bobby", {})),
                            (ShowDialog, ("I NEED you to hit your fucking money quota", {})),
                            (Wait, (80, {})),
                            (GoTo, ("intro_explanation", {}))
                            ],
      "intro_explanation" : [
                            (ShowDialog, ("okay... so...", {})),
                            (Wait, (30, {})),
                            (ShowDialog, ("...here's what I'm thinking...", {})),
                            (Wait, (80, {})),
                            (ShowDialog, ("We're giving you a new territory", {})),
                            (ShowDialog, ("and plenty of weapons", {})),
                            (Wait, (80, {})),
                            (ShowDialog, ("it's very simple, Bobby", {})),
                            (ShowDialog, ("Do whatever it takes to hit your number", {})),
                            (Wait, (80, {})),
                            (ShowDialog, ("or you're a dead motherfucker.", {})),
                            (Wait, (60, {})),
                            (ShowDialog, ("Corporate wants us to get more rare stones,", {})),
                            (ShowDialog, ("so I want you to really focus on those.", {})),
                            (Wait, (80, {})),
                            (ShowDialog, ("Oh, and one more thing...", {})),
                            (Wait, (60, {})),
                            (ShowDialog, ("Try to make sure you don't, uh...", {})),
                            (Wait, (60, {})),
                            (ShowDialog, ("injure too many bystanders", {})),
                            (ShowDialog, ("that gets us a lot of complaints from HR,", {})),
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
                            (Wait, (20, {})),
                            (ShowDialog, ("Time is money", {})),
                            (Wait, (80, {})),
                            (ShowDialog, ("Get out there and make it happen", {})),
                            (Wait, (80, {})),
                            (ShowDialog, ("...", {})),
                            (Wait, (80, {})),
                            (ShowDialog, ("...or I'll fucking kill you", {})),
                            (Wait, (80, {})),
                            (EndCall,("world_map", {}))
                          ]
            }
            