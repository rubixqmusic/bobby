from settings import *

menus = {

            "settings": [
                        {"name" : "display",    "text" : "Display Settings",        "position" : [SCREEN_WIDTH/2, 80]},
                        {"name" : "input",      "text" : "Input Settings",          "position" : [SCREEN_WIDTH/2, 120]},
                        {"name" : "back",       "text" : "Back To Title Screen",    "position" : [SCREEN_WIDTH/2, 160]}
                        ],

            "display_settings": [
                        {"name" : "fullscreen",    "text" : "Fullscreen",               "position" : [SCREEN_WIDTH/2, 80]},
                        {"name" : "mode_1",        "text" : "2048 x 1152",             "position" : [SCREEN_WIDTH/2, 120]},
                        {"name" : "mode_2",        "text" : "1024 x 576",              "position" : [SCREEN_WIDTH/2, 160]},
                        {"name" : "mode_3",        "text" : "512 x 288",               "position" : [SCREEN_WIDTH/2, 200]},
                        {"name" : "back",          "text" : "Back To Title Screen",     "position" : [SCREEN_WIDTH/2, 240]}
                        ],

            "title_screen" :    [
                                {"name" : "start_game",     "text" : "Start Game",          "position" : [SCREEN_WIDTH/2, 170]},
                                {"name" : "settings",       "text" : "Display Settings",    "position" : [SCREEN_WIDTH/2, 200]},
                                {"name" : "quit_game",      "text" : "Quit Game",           "position" : [SCREEN_WIDTH/2, 230]}
                                ],
            
            "pick_game_mode" :  [
                                {"name" : "story_mode",     "text" : "Story Mode",  "position" : [SCREEN_WIDTH/2, 170]},
                                {"name" : "2_player",       "text" : "2 Player",    "position" : [SCREEN_WIDTH/2, 200]},
                                {"name" : "back",           "text" : "Back",        "position" : [SCREEN_WIDTH/2, 230]}
                                ]
        }