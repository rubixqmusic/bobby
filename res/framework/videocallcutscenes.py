from res.framework.gamestates.videocallcutscenestates import VideoCallRinging, SetBackgroundImage, SetCharacterAnimation, Choice, ShowDialog, GoTo, EndCall

BLANK_BACKGROUND_PATH = f"backgrounds/video_call_blank_background.png"

cutscenes = {
                "intro_1" : [
                            (VideoCallRinging,""),
                            (SetBackgroundImage, (1,BLANK_BACKGROUND_PATH)),
                            (SetBackgroundImage, (2,BLANK_BACKGROUND_PATH)),
                            (SetCharacterAnimation, (1, "spritesheetpath", "animationpath", "startinganimation")),
                            (SetCharacterAnimation, (2, "spritesheetpath", "animationpath", "startinganimation")),
                            (ShowDialog, ("How ya doin, Bobby?")),
                            (ShowDialog, ("Listen... I'm not going to sugar coat it...")),
                            (ShowDialog, ("The numbers are in, and...")),
                            (ShowDialog, ("it's not looking good")),
                            (ShowDialog, ("You're on thin fucking ice, Bobby")),
                            (ShowDialog, ("I NEED you to hit your fucking number")),
                            (GoTo, ("intro_explanation"))
                            ],
      "intro_explanation" : [
                            (ShowDialog, ("okay... so...")),
                            (ShowDialog, ("...here's what I'm thinking...")),
                            (ShowDialog, ("We're giving you a new territory")),
                            (ShowDialog, ("and plenty of weapons")),
                            (ShowDialog, ("it's very simple, Bobby")),
                            (ShowDialog, ("Do whatever it takes to hit your number")),
                            (ShowDialog, ("or you're a dead motherfucker.")),
                            (ShowDialog, ("Corporate wants us to get more rare stones, so I want you to really focus on those.")),
                            (ShowDialog, ("Oh, and one more thing...")),
                            (ShowDialog, ("Try to make sure you don't, uh...")),
                            (ShowDialog, ("injure too many bystanders")),
                            (ShowDialog, ("that tends to get us a lot of complaints from HR, and thats bad")),
                            (Choice, ("Do you understand?", [["Yes", "intro_end"], ["No", "intro_no"]]))
                            ],
              "intro_no" :  [
                            (ShowDialog, ("Goddammit, Bobby, I need you to pay attention")),
                            (GoTo, ("intro_explanation"))
                            ],
              "intro_end" : [
                            (ShowDialog, ("Alright, Bobby")),
                            (ShowDialog, ("Get out there, and hit your fucking number")),
                            (EndCall,"level_select")
                          ]
            }
            