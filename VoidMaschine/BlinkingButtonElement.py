import Live
import time
from _Framework.ButtonElement import ButtonElement
ON_VALUE = int(127)
OFF_VALUE = int(0)
class BlinkingButtonElement (ButtonElement):
    ' Class representing a button on the controller that can be set to blink '
    
    def __init__(self, is_momentary, msg_type, channel, identifier):
        ButtonElement.__init__(self, is_momentary, msg_type, channel, identifier)
        self._is_enabled = False


    def set_blinking(self, blink):
        self._ButtonElement__is_blinking = blink

    def turn_on(self):
        if (self._is_blinking):
            self.set_blinking(True)
        else:
            self.send_value(ON_VALUE)


    def turn_off(self):
        if (self._is_enabled):
            self.send_value(ON_VALUE)
        else:
            self.send_value(OFF_VALUE)
            
    def blink(self):
        pass
        
    def set_enabled(self, enable):
        self._is_enabled = enable