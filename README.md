# pycrt
The Python Console Resource Toolkit library.

**This branch contains the Python 3 version. For the old Python 2 version visit the ``python2`` branch.**

## What's this?
PyCrt is a open-source Python module aimed to provide TUI-oriented console functions at its most basic level, that is, setting colors, moving cursor, clearing screen, and reading synchronously terminal input.
It's inspired on the classic Pascal unit "crt.pas", hence the backronym. It shares some function names and syntax from it as well.
At the moment, it's only available for POSIX systems providing ANSI escape sequences and termios/unistd libraries.
Therefore, it works on OSX/Linux/UNIX, as well as Windows Terminal and enhanced Windows 10 console host (not the legacy console).

## Which features does it provide?
At the moment, the following functions are implemented:
* goto_xy(int x,int y)
  * Makes the terminal cursor jump to the given coordinates on screen. X is the column and Y is the row.
* int where_x()
  * Returns the column where the cursor is.
* int where_y()
  * Returns the row where the cursor is.
* (int,int) where_xy()
  * Returns a tuple containing both X and Y coordinates of cursor.
* hide_cursor()
  * Hides cursor.
* show_cursor()
  * Shows cursor.
* cursor_status()
  * Returns 1 if the cursor is visible, 0 otherwise.
* clrscr()
  * Clears console screen.
* clreol()
  * Clears the current line from cursor position onwards.
* raw_on()
  * Enables raw terminal mode (prevents OS from handling buffers). Necessary for PendKey() and ReadKey(). Developers are adviced to call RawOff() before exiting program.
* raw_off()
  * Diables raw terminal mode and restores old status.
* is_raw()
  * Returns true if raw mode is enabled.
* text_background(pycrt.Color color)
  * Sets the background of the text that will follow stdout from now on. Does not affect previous output. Argument must be of class Color (see below).
* text_color(pycrt.Color color)
  * Sets the foreground of the text that will follow stdout from now on. Does not affect previous output. Argument must be of class Color (see below).
* set_bold(int value)
  * If value is 1, the following text output to stdout will be bold. Does not affect previous output. If value is 0, bold is disabled. Not all terminals support this format (those which don't, will simply ignore it).
* set_italic(int value)
  * If value is 1, the following text output to stdout will be italic. Does not affect previous output. If value is 0, italic is disabled. Not all terminals support this format (those which don't, will simply ignore it).
* set_underline(int value)
  * If value is 1, the following text output to stdout will be underline. Does not affect previous output. If value is 0, underline is disabled. Not all terminals support this format (those which don't, will simply ignore it).
* set_strike(int value)
  * If value is 1, the following text output to stdout will be striked out. Does not affect previous output. If value is 0, strike is disabled. Not all terminals support this format (those which don't, will simply ignore it).
* set_conceal(int value)
  * If value is 1, the following text output to stdout will be concealed. Does not affect previous output. If value is 0, concealing is disabled. Not all terminals support this format (those which don't, will simply ignore it). 
* format_reset()
  * Resets colors and format to terminal defaults.
* read_key()
  * Reads the next key in buffer and outputs is value as char. RAW mode should be enabled before. Throws pycrt.RawModeOffException if RAW Mode is off.
* pend_key()
  * Returns true if there's a key in the buffer ready to be read. RAW mode should be enabled before. Throws pycrt.RawModeOffException if RAW Mode is off.
  
The following classes are available:
* class Color(IntEnum)
  * Enumeration of the available colors for TextColor and TextBackground, which are: DEFAULT (default terminal settings), BLACK,	RED, GREEN,	BROWN, BLUE, MAGENTA, CYAN and WHITE.
* class RawModeOffException(Exception)
  * Exception threwn if an operation requiring RAW mode to be enabled is called with this mode disabled.
  
## Which is the license for this?
This software is available as open-source software under the BSD license which follows:
```
 Python Console Resource Toolkit
 Copyright (c) 2022, Marc Sances
 All rights reserved.

 Redistribution and use in source and binary forms, with or without
 modification, are permitted provided that the following conditions
 are met:
 1. Redistributions of source code must retain the above copyright
    notice, this list of conditions and the following disclaimer.
 2. Redistributions in binary form must reproduce the above copyright
    notice, this list of conditions and the following disclaimer in the
    documentation and/or other materials provided with the distribution.
 3. Neither the name of copyright holders nor the names of its
    contributors may be used to endorse or promote products derived
    from this software without specific prior written permission.

 THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
 ''AS IS'' AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED
 TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
 PURPOSE ARE DISCLAIMED.  IN NO EVENT SHALL COPYRIGHT HOLDERS OR CONTRIBUTORS
 BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
 CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
 SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
 INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
 CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
 ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
 POSSIBILITY OF SUCH DAMAGE.
```