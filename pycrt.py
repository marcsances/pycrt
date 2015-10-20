# Python Console Resource Toolkit
# Copyright (c) 2015, Marc Sances
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
import sys, os, termios, fcntl, tty
from enum import Enum

# Global enum declarations
class Color(Enum):
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
__PYCRT_TEXTCOLOR = -1						# default console text color
__PYCRT_TEXTBACKGROUND = -1					# default console text __PYCRT_TEXTBACKGROUND
__PYCRT_BOLD = 0
__PYCRT_ITALIC = 0
__PYCRT_UNDERLINE = 0						
__PYCRT_STRIKETHROUGH = 0
# Storage for terminal status parameters
__PYCRT_RAW_MODE = 0									# raw mode on or off
__PYCRT_RAW_FD = sys.stdin.fileno()						# file descriptor for stdin
__PYCRT_RAW_CNF = termios.tcgetattr(__PYCRT_RAW_FD) 	# current console status
__PYCRT_CURSOR_STATUS = 1								# cursor visible by default


# Main functions
# Cursor control functions
def GotoXY(x,y):
	""" Sets cursor position to the given X, Y coordinates. """
	sys.stdout.write("\033[%d;%dH" % (y,x))
	
def __WhereRC():
	""" Internal. Returns a tuple containing the row and column of the cursor. """
	__unraw = 0
	if (__PYCRT_RAW_MODE == 0):
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
		if (__unraw == 1):				# terminal status was not RAW before invoke. restore terminal status
			termios.tcsetattr(__fd,termios.TCSADRAIN,__tcnf)
	return tuple([int(i) for i in output[2:].split(';')])
	
def WhereX():
	""" Returns the X (column) coordinate of the cursor. """
	return __WhereRC()[1]
	
def WhereY():
	""" Returns the Y (row) coordinate of the cursor. """
	return __WhereRC()[0]
	
def WhereXY():
	""" Returns a tuple containing both the X and Y coordinates of the cursor. """
	return __WhereRC[::-1]
	
def HideCursor():
	""" Hides console cursor. """
	sys.stdout.write("\033[?25l");
	__PYCRT_CURSOR_STATUS = 0
	
def ShowCursor():
	"""	Shows console cursor. """
	sys.stdout.write("\033[?25h");
	__PYCRT_CURSOR_STATUS = 1
	
def CursorStatus()
	""" Returns 1 if the cursor is visible, 0 otherwise. """
	return __PYCRT_CURSOR_STATUS
	
# Line manipulation functions
	
def ClrScr():
	""" Clears the terminal screen. """
	sys.stdout.write("\033[2J");
	sys.stdout.write("\033[1;1H");							# move cursor to 0,0. Should be done by default by terminal.