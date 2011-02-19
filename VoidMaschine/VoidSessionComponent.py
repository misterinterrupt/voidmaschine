'''
Created on Nov 27, 2010

@author: matthewhowell
'''
import sys
import Live
from consts import *
from ConfigurableButtonElement import ConfigurableButtonElement 
from _Framework.ButtonElement import ButtonElement
from _Framework.ButtonMatrixElement import ButtonMatrixElement # Class representing a 2-dimensional set of buttons
from _Framework.SessionComponent import SessionComponent
from _Framework.InputControlElement import * # Base class for all classes representing control elements on a controller

class VoidSessionComponent(SessionComponent):
    '''
    Extension of _Framework.SessionComponent
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self.num_tracks = 4
        self.num_scenes = 4
        SessionComponent.__init__(self, self.num_tracks, self.num_scenes)
        
        self._setup_session_control()
        self._setup_clip_control()
        
    def _setup_session_control(self):
        is_momentary = True
        self.set_offsets(0, 0) #(track_offset, scene_offset) Sets the initial offset of the "red box" from top left
        right_button = ButtonElement(is_momentary, MIDI_NOTE_TYPE, TRANSPORT_CHANNEL, SESSION_NAVIGATE_RIGHT)
        left_button = ButtonElement(is_momentary, MIDI_NOTE_TYPE, TRANSPORT_CHANNEL, SESSION_NAVIGATE_LEFT)
        up_button = ButtonElement(is_momentary, MIDI_NOTE_TYPE, TRANSPORT_CHANNEL, SESSION_NAVIGATE_UP)
        down_button =  ButtonElement(is_momentary, MIDI_NOTE_TYPE, TRANSPORT_CHANNEL, SESSION_NAVIGATE_DOWN)
        prev_button = ButtonElement(is_momentary, MIDI_NOTE_TYPE, TRANSPORT_CHANNEL, SESSION_SCENE_PREVIOUS)
        next_button = ButtonElement(is_momentary, MIDI_NOTE_TYPE, TRANSPORT_CHANNEL, SESSION_SCENE_NEXT)
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
    
    def enable_clip_trigger(self, matrix):
        self._setup_clip_control()
        
    def _setup_clip_control(self):
        self.is_momentary = True
        self._matrix = ButtonMatrixElement() #was: matrix = ButtonMatrixElement()
        self._matrix.name = 'Button_Matrix' #was: matrix.name = 'Button_Matrix'
        clip_launch_buttons = [ ConfigurableButtonElement(self.is_momentary, MIDI_NOTE_TYPE, TRANSPORT_CHANNEL, (index + 48)) for index in range(16) ] #list comprehension to create scene launch buttons
        for index in range(len(clip_launch_buttons)):
            clip_launch_buttons[index].name = 'Scene_'+ str(index) + '_Launch_Button'
            #self.scene(index).set_launch_button(clip_launch_buttons[index])
            
    #def _on_timer(self):
        #SessionComponent._on_timer()
        
    