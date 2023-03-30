def import_main_contr():
    from yourmeals.controllers.main_controller import MainController as MainController
    return MainController()

MainContr = import_main_contr
