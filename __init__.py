import Live
import sys, StringIO, socket, code


has_remote_scripts = False
has_real_python = False

for path in sys.path:
  if path == '/System/Library/Frameworks/Python.framework/Versions/2.5/lib/python2.5/':
    has_real_python = True
  if path == '/Applications/Live 8.2.7b1/Live.app/Contents/App-Resources/MIDI Remote Scripts/':
    has_remote_scripts = True

if not has_real_python:
  sys.path.append('/System/Library/Frameworks/Python.framework/Versions/2.5/lib/python2.5/')

if not has_remote_scripts:
  sys.path.append('/Applications/Live 8.2.7b1/Live.app/Contents/App-Resources/MIDI Remote Scripts/')

import types
from VoidMaschine.VoidMaschine import VoidMaschine

def trace(f):
  def new_f(*args, **kwargs):
    self.log_message("Entering " + f.__name__)
    if args and kwargs:
      apply(f, args, keyword=kwargs)
    elif kwargs:
      apply(f, keyword=kwargs)
    elif args:
      apply(f, args)
    else:
      f()
  return new_f

def make_traceable(log_message, cls):
  """iterate the methods of a class and decorate the methods with our trace function"""
  for name, method in cls.__dict__.iteritems():
    m = method
    log_message(':2 ' + name[:2])
    log_message('2: ' + name[-2:])
    if name[:2] == "__" and name[-2:] == "__" and name != "__init__":
      log_message(name + ' will not be traced.')
    elif hasattr(method, '__call__' ):
      setattr(cls, name, types.MethodType(trace(m), cls))
      log_message(name + ' will be traced.')
  return cls

def create_instance(c_instance):
    """Called by Live when the device is selected from the menu.
    We create and return an object which handles the 
    communication between our code and Live."""
    
    for dude in sys.path:
      c_instance.log_message(dude)
    
    TraceableVoidMaschine = make_traceable(c_instance.log_message, VoidMaschine)
    return TraceableVoidMaschine(c_instance)

#    for name in dir(Live):
#      c_instance.log_message(name)
#    return None
