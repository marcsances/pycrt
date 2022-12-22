# Python Console Resource Toolkit
# Copyright (c) 2022, Marc Sances
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
# 3. Neither the name of copyright holders nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# ''AS IS'' AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED
# TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE ARE DISCLAIMED.  IN NO EVENT SHALL COPYRIGHT HOLDERS OR CONTRIBUTORS
# BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#

""" Python Console Resource Toolkit (pycrt) main module """

# Main CRT module (pycrt.py)
# Import section
import sys
import termios
import time
import tty
from enum import IntEnum

from select import select


# Global enum declarations
class Color(IntEnum):
    """ Defines the colors used for the textcolor and textbackground functions """
    DEFAULT = -1
    BLACK = 0
    RED = 1
    GREEN = 2
    BROWN = 3
    BLUE = 4
    MAGENTA = 5
    CYAN = 6
    WHITE = 7


# Variable declaration section
# Storage for SGR parameters
__PYCRT_TEXTCOLOR = Color.DEFAULT  # default console text color
__PYCRT_TEXTBACKGROUND = Color.DEFAULT  # default console text __PYCRT_TEXTBACKGROUND
__PYCRT_BOLD = 0
__PYCRT_ITALIC = 0
__PYCRT_UNDERLINE = 0
__PYCRT_STRIKETHROUGH = 0
# Storage for terminal status parameters
__PYCRT_RAW_MODE = 0  # raw mode on or off
__PYCRT_RAW_FD = sys.stdin.fileno()  # file descriptor for stdin
__PYCRT_RAW_CNF = termios.tcgetattr(__PYCRT_RAW_FD)  # current console status
__PYCRT_CURSOR_STATUS = 1  # cursor visible by default


# Main functions
# Cursor control functions
def goto_xy(x, y):
    """ Sets cursor position to the given X, Y coordinates. """
    sys.stdout.write("\033[%d;%dH" % (y, x))


def __whererc():
    """ Internal. Returns a tuple containing the row and column of the cursor. """
    __unraw = 0
    __fd = None
    __tcnf = None
    if __PYCRT_RAW_MODE == 0:
        __fd = sys.stdin.fileno()
        __tcnf = termios.tcgetattr(__fd)
        __unraw = 1
        tty.setraw(__fd)
    sys.stdout.write("\033[6n")
    output = ""
    char = ""
    try:
        while char != "R":
            output = output + char
            char = sys.stdin.read(1)
    finally:
        if __unraw == 1:
            termios.tcsetattr(__fd, termios.TCSADRAIN, __tcnf)
    return tuple([int(i) for i in output[2:].split(';')])


def where_x():
    """ Returns the X (column) coordinate of the cursor. """
    return __whererc()[1]


def where_y():
    """ Returns the Y (row) coordinate of the cursor. """
    return __whererc()[0]


def where_xy():
    """ Returns a tuple containing both the X and Y coordinates of the cursor. """
    return __whererc[::-1]


def hide_cursor():
    """ Hides console cursor. """
    global __PYCRT_CURSOR_STATUS
    sys.stdout.write("\033[?25l")
    __PYCRT_CURSOR_STATUS = 0


def show_cursor():
    """	Shows console cursor. """
    global __PYCRT_CURSOR_STATUS
    sys.stdout.write("\033[?25h")
    __PYCRT_CURSOR_STATUS = 1


def cursor_status():
    """ Returns 1 if the cursor is visible, 0 otherwise. """
    return __PYCRT_CURSOR_STATUS


# Line manipulation functions

def clrscr():
    """ Clears the terminal screen. """
    sys.stdout.write("\033[2J")
    sys.stdout.write("\033[1;1H")  # move cursor to 0,0. Should be done by default by terminal.


def clreol():
    """ Clears from cursor position to end of line. """
    sys.stdout.write("\033[0K")


# Terminal status manipulation functions

def raw_on():
    """ Enters RAW terminal mode. Necessary for PendKey and ReadKey functions to work. """
    global __PYCRT_RAW_FD
    global __PYCRT_RAW_CNF
    global __PYCRT_RAW_MODE
    global __PYCRT_RAW_MODE
    if __PYCRT_RAW_MODE == 1:
        return  # Terminal is already in RAW mode.
    __PYCRT_RAW_FD = sys.stdin.fileno()  # it should still remain the same. Grab it anyway.
    __PYCRT_RAW_CNF = termios.tcgetattr(
        __PYCRT_RAW_FD)  # get current terminal configuration and store it until raw mode is left.
    tty.setraw(__PYCRT_RAW_FD)  # enable RAW mode
    __PYCRT_RAW_MODE = 1  # set RAW flag


def raw_off():
    """ Leaves RAW terminal mode, restoring back the previous terminal status. """
    if __PYCRT_RAW_MODE == 0:
        return
    termios.tcsetattr(__PYCRT_RAW_FD, termios.TCSADRAIN, __PYCRT_RAW_CNF)


def is_raw():
    """ Checks whether RAW mode is on or not. """
    return __PYCRT_RAW_MODE == 1


# Color and format manipulation functions

def __setformat(textbackground, textcolor, formatflags):
    """ Internal. Sets text background, color and ANSI-formatted SGR format flags """
    bgrstr = str(textbackground) if textbackground != -1 else ""
    clstr = str(textcolor) if textcolor != -1 else ""
    sys.stdout.write("\033[%s;%s%s" % (bgrstr, clstr, str(formatflags) + "m"))


def __get_format_flags():
    """
    Internal. Gets the format flags that will be sent as ANSI-formatted SGR flags. Not all terminals support these flags
    """
    flags = ";"
    if __PYCRT_BOLD == 1:
        flags = flags + "1;"
    if __PYCRT_ITALIC == 1:
        flags = flags + "3;"
    if __PYCRT_UNDERLINE == 1:
        flags = flags + "4;"
    if __PYCRT_CONCEAL == 1:
        flags = flags + "8;"
    if __PYCRT_STRIKETHROUGH == 1:
        flags = flags + "9;"
    return flags[:-1]


def __update_format():
    """ Internal. Set format with current variable values. """
    bgcl = (__PYCRT_TEXTBACKGROUND + 40, -1)[__PYCRT_TEXTBACKGROUND == -1]
    fgcl = (__PYCRT_TEXTCOLOR + 30, -1)[__PYCRT_TEXTCOLOR == -1]
    __setformat(bgcl, fgcl, __get_format_flags())


def text_background(textbackground):
    """ Changes the text background in the console. """
    global __PYCRT_TEXTBACKGROUND
    __PYCRT_TEXTBACKGROUND = textbackground
    __update_format()


def text_color(textcolor):
    """ Changes the text color in the console. """
    global __PYCRT_TEXTCOLOR
    __PYCRT_TEXTCOLOR = textcolor
    __update_format()


def set_bold(value):
    """ Sets the font bold or not, depending whether value is 1 or 0. Not all terminals support this. """
    global __PYCRT_BOLD
    __PYCRT_BOLD = value
    __update_format()


def set_italic(value):
    """ Sets the font italic or not, depending whether value is 1 or 0. Not all terminals support this. """
    global __PYCRT_ITALIC
    __PYCRT_ITALIC = value
    __update_format()


def set_underline(value):
    """ Sets the font underlined or not, depending whether value is 1 or 0. Not all terminals support this. """
    global __PYCRT_UNDERLINE
    __PYCRT_UNDERLINE = value
    __update_format()


def set_conceal(value):
    """ Sets the font concealed or not, depending whether value is 1 or 0. Not all terminals support this. """
    global __PYCRT_CONCEAL
    __PYCRT_CONCEAL = value
    __update_format()


def get_strike(value):
    """ Sets the font strikethrough or not, depending whether value is 1 or 0. Not all terminals support this. """
    global __PYCRT_STRIKETHROUGH
    __PYCRT_STRIKETHROUGH = value
    __update_format()


def format_reset():
    """ Resets all format, and recovers default terminal colors. """
    sys.stdout.write("\033[0m")


# Keyboard manipulation functions

class RawModeOffException(Exception):
    pass


def pend_key():
    """
    Boolean. Returns true if there is a key in the keyboard buffer ready to be read.
    Throws RawModeOffException if terminal was not set to RAW mode.
    """
    if __PYCRT_RAW_MODE == 0:
        raise RawModeOffException()
    ret = select([sys.stdin], [], [], 0.001)
    return len(ret[0]) > 0


def read_key():
    """
    Char. Returns the next key value in the keyboard buffer.
    Throws RawModeOffException if terminal was not set to RAW mode.
    """
    if __PYCRT_RAW_MODE == 0:
        raise RawModeOffException()
    return sys.stdin.read(1)


# Misc functions

def oflush():
    """ Flushes stdout. Necessary in some real-time applications to avoid graphic lag. """
    sys.stdout.flush()


def delay(ms):
    """ Shortcut to time.sleep. Works with milliseconds. """
    time.sleep(ms / 1000)
