from settings import *
from src.menus.resources import *

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
                                ],
            
            "select_file" :     [
                                    {"name" : "file_1",     "text" : "NEW",                     "file_name" : FILE_1_NAME,          "bg_image" : FILE_SELECT_BACKGROUND,   "date_created" : "",    "last_saved": "EMPTY",      "percent_to_plan" : "0/100",    "position" : [SCREEN_WIDTH/2, 72]},
                                    {"name" : "file_2",     "text" : "NEW",                     "file_name" : FILE_2_NAME,          "bg_image" : FILE_SELECT_BACKGROUND,   "date_created" : "",    "last_saved": "EMPTY",      "percent_to_plan" : "0/100",    "position" : [SCREEN_WIDTH/2, 122]},
                                    {"name" : "file_3",     "text" : "NEW",                     "file_name" : FILE_3_NAME,          "bg_image" : FILE_SELECT_BACKGROUND,   "date_created" : "",    "last_saved": "EMPTY",      "percent_to_plan" : "0/100",    "position" : [SCREEN_WIDTH/2, 172]},
                                    {"name" : "back",       "text" : "Back To Title Screen",    "position" : [SCREEN_WIDTH/2, 220]},
                                    {"name" : "copy",       "text" : "Copy",                    "position" : [SCREEN_WIDTH/2, 240]},
                                    {"name" : "erase",      "text" : "Erase",                   "position" : [SCREEN_WIDTH/2, 260]}
                                ],

            "erase_file" :     [
                                    {"name" : "file_1",     "text" : "NEW",                     "file_name" : FILE_1_NAME,          "bg_image" : FILE_SELECT_BACKGROUND,   "date_created" : "",    "last_saved": "EMPTY",      "percent_to_plan" : "0/100",    "position" : [SCREEN_WIDTH/2, 72]},
                                    {"name" : "file_2",     "text" : "NEW",                     "file_name" : FILE_2_NAME,          "bg_image" : FILE_SELECT_BACKGROUND,   "date_created" : "",    "last_saved": "EMPTY",      "percent_to_plan" : "0/100",    "position" : [SCREEN_WIDTH/2, 122]},
                                    {"name" : "file_3",     "text" : "NEW",                     "file_name" : FILE_3_NAME,          "bg_image" : FILE_SELECT_BACKGROUND,   "date_created" : "",    "last_saved": "EMPTY",      "percent_to_plan" : "0/100",    "position" : [SCREEN_WIDTH/2, 172]},
                                    {"name" : "back",       "text" : "Cancel",    "position" : [SCREEN_WIDTH/2, 220]}
                                  
                                ],

            "confirm_erase" :   [
                                    {"name" : "yes",    "text" : "Yes, let's erase it",     "position" : [SCREEN_WIDTH/2, 100]},
                                    {"name" : "no",     "text" : "I'll think about it",     "position" : [SCREEN_WIDTH/2, 150]},
                                ],

            "select_source_file" :     [
                                    {"name" : "file_1",     "text" : "NEW",                     "file_name" : FILE_1_NAME,          "bg_image" : FILE_SELECT_BACKGROUND,   "date_created" : "",    "last_saved": "EMPTY",      "percent_to_plan" : "0/100",    "position" : [SCREEN_WIDTH/2, 72]},
                                    {"name" : "file_2",     "text" : "NEW",                     "file_name" : FILE_2_NAME,          "bg_image" : FILE_SELECT_BACKGROUND,   "date_created" : "",    "last_saved": "EMPTY",      "percent_to_plan" : "0/100",    "position" : [SCREEN_WIDTH/2, 122]},
                                    {"name" : "file_3",     "text" : "NEW",                     "file_name" : FILE_3_NAME,          "bg_image" : FILE_SELECT_BACKGROUND,   "date_created" : "",    "last_saved": "EMPTY",      "percent_to_plan" : "0/100",    "position" : [SCREEN_WIDTH/2, 172]},
                                    {"name" : "back",       "text" : "Cancel",    "position" : [SCREEN_WIDTH/2, 220]}
                                  
                                ],

            "select_destination_file" :     [
                                    {"name" : "file_1",     "text" : "NEW",                     "file_name" : FILE_1_NAME,          "bg_image" : FILE_SELECT_BACKGROUND,   "date_created" : "",    "last_saved": "EMPTY",      "percent_to_plan" : "0/100",    "position" : [SCREEN_WIDTH/2, 72]},
                                    {"name" : "file_2",     "text" : "NEW",                     "file_name" : FILE_2_NAME,          "bg_image" : FILE_SELECT_BACKGROUND,   "date_created" : "",    "last_saved": "EMPTY",      "percent_to_plan" : "0/100",    "position" : [SCREEN_WIDTH/2, 122]},
                                    {"name" : "file_3",     "text" : "NEW",                     "file_name" : FILE_3_NAME,          "bg_image" : FILE_SELECT_BACKGROUND,   "date_created" : "",    "last_saved": "EMPTY",      "percent_to_plan" : "0/100",    "position" : [SCREEN_WIDTH/2, 172]},
                                    {"name" : "back",       "text" : "Cancel",    "position" : [SCREEN_WIDTH/2, 220]}
                                  
                                ],

            "confirm_copy" :   [
                                    {"name" : "yes",    "text" : "Yes, let's copy it",     "position" : [SCREEN_WIDTH/2, 100]},
                                    {"name" : "no",     "text" : "I'll think about it",     "position" : [SCREEN_WIDTH/2, 150]},
                                ],
                        
                            
        }