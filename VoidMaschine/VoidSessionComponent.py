"""
Created on Nov 27, 2010

@author: matthewhowell
"""
import sys
import Live
from consts import *
from _Framework.ButtonElement import ButtonElement
from _Framework.ButtonMatrixElement import ButtonMatrixElement # Class representing a 2-dimensional set of buttons
from _Framework.SessionComponent import SessionComponent
from _Framework.InputControlElement import * # Base class for all classes representing control elements on a controller

from BlinkingButtonElement import BlinkingButtonElement

class VoidSessionComponent(SessionComponent):
    """
    Extension of _Framework.SessionComponent
    """

    def __init__(self, c_instance):
        self._c_instance = c_instance
        self.is_momentary = True
        self.num_tracks = 4
        self.num_scenes = 4
        self._matrix = None
        self._linked_session_instances = None
        SessionComponent.__init__(self, self.num_tracks, self.num_scenes)
        self._setup_session_control()
        self.setup_clip_control_matrix()
        
    def _setup_session_control(self):
        self.set_offsets(0, 0) #(track_offset, scene_offset) Sets the initial offset of the "red box" from top left
        right_button = ButtonElement(self.is_momentary, MIDI_NOTE_TYPE, TRANSPORT_CHANNEL, SESSION_NAVIGATE_RIGHT)
        left_button = ButtonElement(self.is_momentary, MIDI_NOTE_TYPE, TRANSPORT_CHANNEL, SESSION_NAVIGATE_LEFT)
        up_button = ButtonElement(self.is_momentary, MIDI_NOTE_TYPE, TRANSPORT_CHANNEL, SESSION_NAVIGATE_UP)
        down_button =  ButtonElement(self.is_momentary, MIDI_NOTE_TYPE, TRANSPORT_CHANNEL, SESSION_NAVIGATE_DOWN)
        prev_button = ButtonElement(self.is_momentary, MIDI_NOTE_TYPE, TRANSPORT_CHANNEL, SESSION_SCENE_PREVIOUS)
        next_button = ButtonElement(self.is_momentary, MIDI_NOTE_TYPE, TRANSPORT_CHANNEL, SESSION_SCENE_NEXT)
        right_button.name = 'Bank_Select_Right_Button'
        left_button.name = 'Bank_Select_Left_Button'
        up_button.name = 'Bank_Select_Up_Button'
        down_button.name = 'Bank_Select_Down_Button'
        next_button.name = 'Bank_Select_Next_Button'
        prev_button.name = 'Bank_Select_Previous_Button'
        
        """set up the session navigation buttons"""
        self.set_select_buttons(next_button, prev_button) # (next_button, prev_button) Scene select buttons - up & down
        self.set_scene_bank_buttons(down_button, up_button) # (down_button, up_button) This is to move the "red box" up or down (increment track up or down, not screen up or down, so they are inversed)
        self.set_track_bank_buttons(right_button, left_button) # (right_button, left_button) This moves the "red box" selection set left & right. We'll put our track selection in Part B of the script, rather than here...
        self.selected_scene().name = 'Selected_Scene'
        self.selected_scene().set_launch_button(ButtonElement(True, MIDI_NOTE_TYPE, TRANSPORT_CHANNEL, SESSION_SCENE_LAUNCH))
        
    def setup_clip_control_matrix(self):
        self._matrix = ButtonMatrixElement() #was: matrix = ButtonMatrixElement()
        self._matrix.name = 'Button_Matrix' #was: matrix.name = 'Button_Matrix'
        clip_launch_buttons = [ BlinkingButtonElement(self.is_momentary, MIDI_NOTE_TYPE, TRANSPORT_CHANNEL, (51 - index)) for index in range(16) ] #list comprehension to create scene launch buttons
        
        for scene_index in range(self.num_scenes):
            scene = self.scene(scene_index)
            scene.name = 'Scene_' + str(scene_index+1)
            button_row = []
            for track_index in range(self.num_tracks):
                button_index = (self.num_scenes*(scene_index)) + (self.num_tracks - track_index)
                clip_launch_buttons[button_index - 1].name = 'Clip_Launch_Button' + str(button_index)
                clip_launch_buttons[button_index - 1].set_enabled = True
                slot = scene.clip_slot(track_index)
                slot.name = 'Scene_' + str(scene_index) + 'Clip_Slot_' + str(track_index)
                slot.set_launch_button(clip_launch_buttons[button_index - 1])
                slot.set_enabled(True)
                button_row.append(clip_launch_buttons[button_index - 1])
            self._matrix.add_row(tuple(button_row))
            
        return None
    
    def update(self):
        SessionComponent.update(self)
        # run all callbacks
    
    #def _on_timer(self):
        #SessionComponent._on_timer()
        
    