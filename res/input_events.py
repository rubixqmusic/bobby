import pygame
from settings import *

input_map = {
                "K_a" : LEFT_BUTTON,
                "K_d" : RIGHT_BUTTON,
                "K_w" : UP_BUTTON,
                "K_s" : DOWN_BUTTON,
                
                "K_RETURN" : START_BUTTON,
                "K_BACKSPACE" : SELECT_BUTTON,
                "K_ESCAPE" : QUIT_KEY,
                "K_SPACE" : ACTION_BUTTON_1,
                "K_RALT" : ACTION_BUTTON_2,
                "K_RCTRL" : ACTION_BUTTON_3,
                "K_RSHIFT" : ACTION_BUTTON_4,

                "BUTTONS" : {
                                0 : ACTION_BUTTON_1,
                                7 : START_BUTTON,
                                8 : SELECT_BUTTON
                },

                # "HATS" :{
                #             0 : []
                #         }
            }



input_events = {
                pygame.K_0 : "K_0",
                pygame.K_1 : "K_1",
                pygame.K_2 : "K_2",
                pygame.K_3 : "K_3",
                pygame.K_4 : "K_4",
                pygame.K_5 : "K_5",
                pygame.K_6 : "K_6",
                pygame.K_7 : "K_7",
                pygame.K_8 : "K_8",
                pygame.K_9 : "K_9",

                pygame.K_a : "K_a",
                pygame.K_b : "K_b",
                pygame.K_c : "K_c",
                pygame.K_d : "K_d",
                pygame.K_e : "K_e",
                pygame.K_f : "K_f",
                pygame.K_g : "K_g",
                pygame.K_h : "K_h",
                pygame.K_i : "K_i",
                pygame.K_j : "K_j",
                pygame.K_k : "K_k",
                pygame.K_l : "K_l",
                pygame.K_m : "K_m",
                pygame.K_n : "K_n",
                pygame.K_o : "K_o",
                pygame.K_p : "K_p",
                pygame.K_q : "K_q",
                pygame.K_r : "K_r",
                pygame.K_s : "K_s",
                pygame.K_t : "K_t",
                pygame.K_u : "K_u",
                pygame.K_v : "K_v",
                pygame.K_w : "K_w",
                pygame.K_x : "K_x",
                pygame.K_y : "K_y",
                pygame.K_z : "K_z",
                
                pygame.K_ESCAPE: "K_ESCAPE",
                pygame.K_TAB : "K_TAB",
                pygame.K_RETURN : "K_RETURN",
                pygame.K_RALT : "K_RALT",
                pygame.K_LSHIFT : "K_LSHIFT",
                pygame.K_RSHIFT : "K_RSHIFT",
                pygame.K_CAPSLOCK : "K_CAPSLOCK",
                pygame.K_BACKSPACE : "K_BACKSPACE",
                pygame.K_LCTRL : "K_LCTRL",
                pygame.K_RCTRL : "K_RCTRL",
                pygame.K_SPACE : "K_SPACE",

                pygame.K_SEMICOLON : "K_SEMICOLON",
                pygame.K_QUOTE : "K_QUOTE",
                pygame.K_PERIOD: "K_PERIOD",
                pygame.K_COMMA : "K_COMMA",
                pygame.K_BACKSLASH : "K_BACKSLASH",
                pygame.K_SLASH : "K_SLASH",
                pygame.K_LEFTBRACKET : "K_LEFTBRACKET",
                pygame.K_RIGHTBRACKET : "K_RIGHTBRACKET",

                pygame.JOYAXISMOTION : "JOYAXISMOTION",
                pygame.JOYBALLMOTION : "JOYBALLMOTION",
                pygame.JOYBUTTONDOWN : "JOYBUTTONDOWN",
                pygame.JOYBUTTONUP : "JOYBUTTONUP",
                pygame.JOYDEVICEADDED : "JOYDEVICEADDED",
                pygame.JOYDEVICEREMOVED : "JOYDEVICEREMOVED",
                pygame.JOYHATMOTION : "JOYHATMOTION"
                }

controller_input = {
                    "up_button" : "up_button",
                    "down_button" : "down_button",
                    "right_button" : "right_button",
                    "left_button" : "left_button",

                    "x_axis" : "x_axis",
                    "y_axis" : "y_axis",

                    "start_button" : "start_button",
                    "select_button" : "select_button",

                    "action_button_1" : "action_button_1",
                    "action_button_2" : "action_button_2",
                    "action_button_3" : "action_button_3",
                    "action_button_4" : "action_button_4",

                    "l_shoulder" : "l_shoulder",
                    "r_shoulder" : "r_shoulder",

                    "l_trigger" : "l_trigger",
                    "r_trigger" : "r_trigger"

                    }