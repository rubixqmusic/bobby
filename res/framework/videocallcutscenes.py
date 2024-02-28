from res.framework.gamestates.videocallcutscenestates import VideoCallRinging, SetBackgroundImage, SetCharacterAnimation, ShowDialog, EndCall


cutscenes = {
                "intro" : [
                            (VideoCallRinging,), #1
                            (SetBackgroundImage, (1,"backgroundimagepath")),
                            (SetBackgroundImage, (2,"backgroundimagepath")),
                            (SetCharacterAnimation, (1, "spritesheetpath", "animationpath", "startinganimation")),
                            (SetCharacterAnimation, (2, "spritesheetpath", "animationpath", "startinganimation")),
                            (ShowDialog, ("How ya doin, Bobby?")),
                            (ShowDialog, ("Listen... I'm not going to sugar coat it...")),
                            (ShowDialog, ("The numbers are in, and...")),
                            (ShowDialog, ("it's not looking good")),
                            (ShowDialog, ("You're on thin fucking ice, Bobby")),
                            (ShowDialog, ("I NEED you to hit your fucking number")),
                            (ShowDialog, ("okay... so...")),
                            (ShowDialog, ("...here's what I'm thinking...")),
                            (ShowDialog, ("We're giving you a new territory")),
                            (ShowDialog, ("and plenty of weapons")),
                            (ShowDialog, ("it's very simple, Bobby")),
                            (ShowDialog, ("Do whatever it takes to hit your number")),
                            (ShowDialog, ("or you're a dead motherfucker.")),
                            (ShowDialog, ("Corporate wants us to get more investments, so I want you to really focus on those.")),
                            (ShowDialog, ("Oh, and one more thing...")),
                            (ShowDialog, ("Try to make sure you don't, uh...")),
                            (ShowDialog, ("injure too many bystanders")),
                            (ShowDialog, ("that tends to get us a lot of complaints from HR, and thats bad")),
                            (ShowDialog, ("Alright, Bobby")),
                            (ShowDialog, ("Get out there, and hit your fucking number")),
                            (EndCall,)


                          ]
            }