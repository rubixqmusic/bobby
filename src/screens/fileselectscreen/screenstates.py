from src.screens.fileselectscreen.states import confirmcopy, confirmerase, erasefile, fadein, filecopied, fileerased, gototitlescreen, loadsavedgame, selectdestinationfile, selectfile,selectsourcefile, startnewgame

file_select_screen_states = {
                        "fade_in" : fadein.FadeIn,
                        "select_file" : selectfile.SelectFile,
                        "go_to_title_screen" : gototitlescreen.GoToTitleScreen,
                        "start_new_game" : startnewgame.StartNewGame,
                        "load_saved_game" : loadsavedgame.LoadSavedGame,
                        "erase_file" : erasefile.EraseFile,
                        "confirm_erase" : confirmerase.ConfirmErase,
                        "file_erased" : fileerased.FileErased,
                        "select_source_file" : selectsourcefile.SelectSourceFile,
                        "select_destination_file" : selectdestinationfile.SelectDestinationFile,
                        "confirm_copy" : confirmcopy.ConfirmCopy,
                        "file_copied" : filecopied.FileCopied
                        }