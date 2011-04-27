import sys
import Live
import time
from consts import *

from _Framework.ControlSurface import ControlSurface # Central base class for scripts based on the new Framework
""" All of the Framework files are listed below, but we are only using using some of them in this script (the rest are commented out) """
#from ConfigurableButtonElement import ConfigurableButtonElement 
from _Framework.ButtonElement import ButtonElement # Class representing a button a the controller
from _Framework.ButtonMatrixElement import ButtonMatrixElement # Class representing a 2-dimensional set of buttons
#from _Framework.ButtonSliderElement import ButtonSliderElement # Class representing a set of buttons used as a slider
#from _Framework.ChannelStripComponent import ChannelStripComponent # Class attaching to the mixer of a given track
#from _Framework.ChannelTranslationSelector import ChannelTranslationSelector # Class switches modes by translating the given controls' message channel
from _Framework.ClipSlotComponent import ClipSlotComponent # Class representing a ClipSlot within Live
#from _Framework.CompoundComponent import CompoundComponent # Base class for classes encompasing other components to form complex components
from _Framework.ControlElement import ControlElement # Base class for all classes representing control elements on a controller
from _Framework.ControlSurface import ControlSurface # Central base class for scripts based on the new Framework
#from _Framework.ControlSurfaceComponent import ControlSurfaceComponent # Base class for all classes encapsulating functions in Live
#from _Framework.DeviceComponent import DeviceComponent # Class representing a device in Live
#from _Framework.DisplayDataSource import DisplayDataSource # Data object that is fed with a specific string and notifies its observers
from _Framework.EncoderElement import EncoderElement # Class representing a continuous control on the controller
from _Framework.InputControlElement import * # Base class for all classes representing control elements on a controller
#from _Framework.LogicalDisplaySegment import LogicalDisplaySegment # Class representing a specific segment of a display on the controller
from _Framework.MixerComponent import MixerComponent # Class encompassing several channel strips to form a mixer
#from _Framework.ModeSelectorComponent import ModeSelectorComponent # Class for switching between modes, handle several functions with few controls
#from _Framework.NotifyingControlElement import NotifyingControlElement # Class representing control elements that can send values
from _Framework.PhysicalDisplayElement import PhysicalDisplayElement # Class representing a display on the controller
from _Framework.SceneComponent import SceneComponent # Class representing a scene in Live
from _Framework.SessionComponent import SessionComponent # Class encompassing several scene to cover a defined section of Live's session
from _Framework.SessionZoomingComponent import SessionZoomingComponent # Class using a matrix of buttons to choose blocks of clips in the session
#from _Framework.SliderElement import SliderElement # Class representing a slider on the controller
#from _Framework.TrackEQComponent import TrackEQComponent # Class representing a track's EQ, it attaches to the last EQ device in the track
#from _Framework.TrackFilterComponent import TrackFilterComponent # Class representing a track's filter, attaches to the last filter in the track
from _Framework.TransportComponent import TransportComponent # Class encapsulating all functions in Live's transport section
from VoidSessionComponent import VoidSessionComponent
#from ShiftableTransportComponent import ShiftableTransportComponent

"""
Originally Created on Nov 7, 2010  :: Matt Howell
Thanks to Hanz Petrov, Native Instruments, Ableton, Liine
"""
class VoidMaschine(ControlSurface):
    """
    classdocs
    """
    
    def __init__(self, c_instance):
        """
        Constructor
        """
        ControlSurface.__init__(self, c_instance)
        self.log_message(time.strftime("%d.%m.%Y %H:%M:%S", time.localtime()) + "--------------= VoidMaschine opened =--------------")
        self.name = 'VoidMaschine'
        self.log_message(('::::::: ' + self.name))
        self.show_message((self.name + ' loaded'));
        self.set_suppress_rebuild_requests(True)
        self._suppress_session_highlight = True
        self._suppress_send_midi = True
        self._suggested_input_port = MASCHINE_DEVICE_PORT_NAME
        self._suggested_output_port = MASCHINE_DEVICE_PORT_NAME
        self._shift_button = None
        self.transport = TransportComponent()
        self.transport.name = 'Transport'
        self.session = None
        self.session_zoom = None
        self.mixer = None
        self.back_to_arranger_button = None
        self.is_momentary = True
        self._LAST_BEAT = 0
        self._tempo_light_state = 0
        self._LAST_TEMPO_STATE = 0

        self._setup_transport_control()
        self._session = VoidSessionComponent(c_instance)
        self._session.name = 'Session_Control'
        
        self._setup_mixer_control()
        
        #self._session_zoom = SessionZoomingComponent(self._session)
        #self._session_zoom.name = 'Session_Overview'
        #self._session_zoom.set_button_matrix(self._session._matrix)
        
        
        self._set_back_to_arranger_button(ButtonElement(True, MIDI_NOTE_TYPE, TRANSPORT_CHANNEL, TRANSPORT_BACK_TO_ARRANGER))
        self.set_suppress_rebuild_requests(False)
        self._display = PhysicalDisplayElement(56, 8)
        self._void_message()
        
    def _void_message(self):
        self.sendScreenSysex(self.translateString((SYSEX_SCREEN_BUFFER_15 + 'VoidMaschine' + SYSEX_SCREEN_BUFFER_15)), 1)
        self.sendScreenSysex(self.translateString(('Voidrunner.com' + SYSEX_SCREEN_BUFFER_15 + '    maschine/ableton')), 2)
        
    def _setup_mixer_control(self):
        self.mixer = MixerComponent(0, 0, with_eqs=False, with_filters=False)
        master_volume_control = EncoderElement(MIDI_CC_TYPE, MIXER_CHANNEL, MASTER_VOLUME, Live.MidiMap.MapMode.absolute)
        booth_volume_control = EncoderElement(MIDI_CC_TYPE, MIXER_CHANNEL, MASTER_BOOTH, Live.MidiMap.MapMode.absolute)
        self.mixer.set_prehear_volume_control(booth_volume_control)
        self.mixer.master_strip().set_volume_control(master_volume_control)
        
        
    def _setup_transport_control(self):
        play_button = ButtonElement(self.is_momentary, MIDI_NOTE_TYPE, TRANSPORT_CHANNEL, TRANSPORT_PLAY)
        stop_button = ButtonElement(self.is_momentary, MIDI_NOTE_TYPE, TRANSPORT_CHANNEL, TRANSPORT_STOP)
        record_button = ButtonElement(self.is_momentary, MIDI_NOTE_TYPE, TRANSPORT_CHANNEL, TRANSPORT_RECORD)
        seek_ffwd_button = ButtonElement(self.is_momentary, MIDI_NOTE_TYPE, TRANSPORT_CHANNEL, TRANSPORT_SEEK_FFWD)
        seek_rwd_button = ButtonElement(self.is_momentary, MIDI_NOTE_TYPE, TRANSPORT_CHANNEL, TRANSPORT_SEEK_RWD)
        tap_tempo_button = ButtonElement(self.is_momentary, MIDI_NOTE_TYPE, TRANSPORT_CHANNEL, TRANSPORT_TAP_TEMPO)
        play_button.name = 'Play_Button'
        stop_button.name = 'Stop_Button'
        record_button.name = 'Record_Button'
        seek_ffwd_button.name = 'Seek_FFWD_Button'
        seek_rwd_button.name = 'Seek_RWD_Button'
        tap_tempo_button.name = 'Tap_Tempo_Button'
        self.transport.set_play_button(play_button)
        self.transport.set_stop_button(stop_button)
        self.transport.set_record_button(record_button)
        self.transport.set_tap_tempo_button(tap_tempo_button)
        self.transport.set_seek_buttons(seek_ffwd_button, seek_rwd_button)
    
    def _set_back_to_arranger_button(self, button):
        button.add_value_listener(self.back_to_arranger)
        self.back_to_arranger_button = button
    
    def disconnect(self):
        self.send_midi((240, 0, 66, 89, 69, 247)) #goodbye message in sysex stream
        
    def send_midi(self, midi_event_bytes):
        """
        Use this function to send MIDI events through Live to the _real_ MIDI devices
        that this script is assigned to.
        """
        assert isinstance(midi_event_bytes, tuple)
        self._send_midi(midi_event_bytes)
        return True
        
    def translateString(self, text):
        """
        Convert a string into a sysex safe string
        """
        result = ()
        length = len(text)
        for i in range(0, length):
            charCode = ord(text[i])
            if (charCode < 32):
                charCode = 32
            elif (charCode > 127):
                charCode = 127
            result = (result + (charCode,))
    
        return result

    def sendScreenSysex(self, data, line=1):
        """
        Data must be a tuple of bytes, remember only 7-bit data is allowed for sysex
        """
        pass
        if(line==1):
            self._send_midi(((SYSEX_SCREEN_BEGIN_LINE_1 + data) + SYSEX_SCREEN_END))
        else:
            if(line==2):
                self._send_midi(((SYSEX_SCREEN_BEGIN_LINE_2 + data) + SYSEX_SCREEN_END))
    
    def send_value(self, msg_type, channel, id, value, force_send = False):
        assert (value != None)
        assert isinstance(value, int)
        assert (value in range(128))
        
        data_byte1 = id
        data_byte2 = value
        status_byte = channel
        if (msg_type == MIDI_NOTE_TYPE):
            status_byte += MIDI_NOTE_ON_STATUS
        elif (msg_type == MIDI_CC_TYPE):
            status_byte += MIDI_CC_STATUS
        else:
            assert False
        self._send_midi((status_byte, data_byte1, data_byte2))
    
    def back_to_arranger(self, *args, **kwargs):
        self.song().back_to_arranger = False
    
    def update_display(self):
        """
        modified this from NI Maschine script ::: This function is run every 100ms, 
        we use it to initiate our Song.current_song_time listener to allow us to process 
        incoming OSC commands as quickly as possible under the current listener scheme.
        """
        self.displayTempo()
        

    def register_timer_callback(self, ):
        pass
    
    def _update_registered_timer_callbacks():
        """
        trigger registered callbacks for any classes that need timers 
        but do not inherit from ControlSurface
        """
        pass

    def displayTempo(self):
        bpmBeatTime = self.song().get_current_beats_song_time()
        
        if self.song().is_playing:
            if (bpmBeatTime.beats != self._LAST_BEAT):
                self._tempo_light_state = 1
            else:
                self._tempo_light_state = 0
        
        # when the tempo state changes, change the light
        if (self._tempo_light_state != self._LAST_TEMPO_STATE):
            if (self._tempo_light_state == 0):
                self.updateBPMLightOff()
                
            if (self._tempo_light_state == 1):
                self.updateBPMLightOn()
        
        self._LAST_BEAT = bpmBeatTime.beats
        self._LAST_TEMPO_STATE = self._tempo_light_state
            
    def updateBPMLightOn(self):
        self.transport._play_button.turn_on()
        #self.send_value(MIDI_NOTE_TYPE, TRANSPORT_CHANNEL, TRANSPORT_TEMPO, MASCHINE_DISPLAY_BPM)
        
    def updateBPMLightOff(self):
        self.transport._play_button.turn_off()
        #self.send_value(MIDI_NOTE_TYPE, TRANSPORT_CHANNEL, TRANSPORT_TEMPO, 0)
    