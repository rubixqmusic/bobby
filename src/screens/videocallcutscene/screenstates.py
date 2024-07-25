import json

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
# from src.bob import bob

def load_video_call_cutscenes(cutscene_file_data, resource_file_data):
    video_call_cutscenes = {}
    for cutscene_name in cutscene_file_data:
        cutscene_events = []
        for cutscene_event in cutscene_file_data[cutscene_name]:
            if cutscene_event[0] == "VideoCallRinging":
                cutscene_events.append((VideoCallRinging, cutscene_event[1]))
            if cutscene_event[0] == "PlayMusic":
                cutscene_events.append((PlayMusic, (resource_file_data[cutscene_event[1][0]], resource_file_data[cutscene_event[1][1]], cutscene_event[1][2])))
            if cutscene_event[0] == "SetBackgroundImage":
                cutscene_events.append((SetBackgroundImage, (cutscene_event[1][0], resource_file_data[cutscene_event[1][1]], cutscene_event[1][2])))
            if cutscene_event[0] == "SetCharacterAnimation":
                cutscene_events.append((SetCharacterAnimation, (cutscene_event[1][0], resource_file_data[cutscene_event[1][1]], resource_file_data[cutscene_event[1][2]], cutscene_event[1][3], cutscene_event[1][4])))
            if cutscene_event[0] == "Wait":
                cutscene_events.append((Wait, (cutscene_event[1][0], cutscene_event[1][1] )))
            if cutscene_event[0] == "ShowDialog":
                cutscene_events.append((ShowDialog, (cutscene_event[1][0], cutscene_event[1][1] )))
            if cutscene_event[0] == "GoTo":
                cutscene_events.append((GoTo, (cutscene_event[1][0], cutscene_event[1][1] )))
            if cutscene_event[0] == "Choice":
                cutscene_events.append((Choice, (cutscene_event[1][0], cutscene_event[1][1], cutscene_event[1][2] )))
            if cutscene_event[0] == "PlaySound":
                cutscene_events.append((PlaySound, (resource_file_data[cutscene_event[1][0]], cutscene_event[1][1] )))
            if cutscene_event[0] == "EndCall":
                cutscene_events.append((EndCall, (cutscene_event[1][0], cutscene_event[1][1] )))
            video_call_cutscenes[cutscene_name] = cutscene_events
    return video_call_cutscenes

# cutscene_file = json.load(bob.load_resource(CUTSCENES_FILE))
# cutscene_resources = json.load(bob.load_resource(CUTSCENES_RESOURCES))

cutscenes = {}


# {
#                 "intro_1" : [
#                             (VideoCallRinging, {}),
#                             (PlayMusic, (BACKGROUND_MUSIC, MUSIC_VOLUME, {})),
#                             (SetBackgroundImage, (1,BEACH_BACKGROUND_PATH, {})),
#                             (SetBackgroundImage, (2,OFFICE_BACKGROUND_PATH, {})),
#                             (SetCharacterAnimation, (1, BOSS_VIDEO_CALL_SPRITESHEET_PATH, BOSS_VIDEO_CALL_ANIMATION_PATH, "idle", {})),
#                             (SetCharacterAnimation, (2, BOBBY_OFFICE_SPRITESHEET_PATH, BOBBY_OFFICE_ANIMATION_PATH, "idle", {})),
#                             (Wait, (80, {})),
#                             # (ShowDialog, ("This is a test string to test how long we can print text before a fuck up happens", {})),
#                             (ShowDialog, ("Bobby, my man", {})),
#                             (ShowDialog, ("what's good, brother?", {})),
#                             (ShowDialog, ("just wanted to hop on a quick call to say welcome to The Team!", {})),
#                             (ShowDialog, ("we're excited to have you on board.", {})),
#                             (ShowDialog, ("Everyone on The Team is a KILLER,", {})),
#                             (ShowDialog, ("and we know you're gonna be one too", {})),
#                             (Wait, (80, {})),
#                             (ShowDialog, ("Alright, Bobby, Let's cut to the chase,", {})),
#                             (GoTo, ("intro_explanation", {}))
#                             ],
#       "intro_explanation" : [
#                             (ShowDialog, ("here's how it works around here:", {})),
#                             (ShowDialog, ("Your #1 priority is getting money.", {})),
#                             (ShowDialog, ("We're giving you a territory.", {})),
#                             (ShowDialog, ("We're giving you powerups.", {})),
#                             (ShowDialog, ("We're giving you weapons to take out the competition.", {})),
#                             (ShowDialog, ("We're giving you everything you need to succeed.", {})),
#                             (ShowDialog, ("As long as you do what we say, there's no way you can fail!", {})),
#                             (ShowDialog, ("You see, it's very simple, Bobby:", {})),
#                             (ShowDialog, ("Do whatever it takes to hit your number,", {})),
#                             (ShowDialog, ("or you're a dead motherfucker.", {})),
#                             (Wait, (80, {})),
#                             (ShowDialog, ("Oh, and one more thing...", {})),
#                             (ShowDialog, ("Please try not to destroy too much stuff,", {})),
#                             (ShowDialog, ("and that includes innocent bystanders.", {})),
#                             (ShowDialog, ("We've been getting tons of complaints to HR,", {})),
#                             (ShowDialog, ("and thats bad", {})),
#                             (Choice, ("Got it?", [["Yes", "intro_end"], ["No", "intro_no"]], {}))
#                             ],
#               "intro_no" :  [
#                             (PlaySound, (DENY_SOUND,{})),
#                             (Wait, (60, {})),
#                             (ShowDialog, ("Goddammit, Bobby, I need you to pay attention.", {})),
#                             (GoTo, ("intro_explanation", {}))
#                             ],
#               "intro_end" : [
#                             (PlaySound, (COIN_SOUND,{})),
#                             (Wait, (80, {})),
#                             (ShowDialog, ("Alright, Bobby,", {})),
#                             (ShowDialog, ("we're gonna have you complete a quick orientation.", {})),
#                             (ShowDialog, ("After that, it's all you.", {})),
#                             (ShowDialog, ("Get out there and make it happen...", {})),
#                             (Wait, (80, {})),
#                             (ShowDialog, ("...or I'll fucking kill you", {})),
#                             (Wait, (80, {})),
#                             (EndCall,("world_map", {}))
#                           ]
#             }