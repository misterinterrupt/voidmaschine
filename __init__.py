import Live
from VoidMaschine.VoidMaschine import VoidMaschine
def create_instance(c_instance):
    '\n    Called by Live when the device is selected from the menu.\n    We create and return an object which handles the communication between our code and Live.  \n    '
    return VoidMaschine(c_instance)
#    for name in dir(Live):
#      c_instance.log_message(name)
#    return None
