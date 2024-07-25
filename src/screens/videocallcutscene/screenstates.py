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

cutscenes = {}
