import sys,pycrt
from pycrt import RawOn
from pycrt import RawOff
from pycrt import PendKey
from pycrt import ReadKey
sys.stdout.write("Press a key!\n")
RawOn()
while (not PendKey()):
  sys.stdout.write(".") 
RawOff()
sys.stdout.write("Key Pressed! ")
sys.stdout.write(ReadKey())
