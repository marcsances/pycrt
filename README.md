# pycrt
The Python Console Resource Toolkit library.

## What's this?
PyCrt is a open-source Python module aimed to provide TUI-oriented console functions at its most basic level, that is, setting colors, moving cursor, clearing screen, and reading synchronously terminal input.
It's inspired on the classic Pascal unit "crt.pas", hence the backronym. It shares some function names and syntax from it as well.
At the moment, it's only available for POSIX systems providing ANSI escape sequences and termios/unistd libraries.
Therefore, it works on OSX/Linux/UNIX, but not on Win32.

## Which features does it provide?
At the moment, the following functions are implemented:
* GotoXY(int x,int y)
  * Makes the terminal cursor jump to the given coordinates on screen. X is the column and Y is the row.
* int WhereX()
  * Returns the column where the cursor is.
* int WhereY()
  * Returns the row where the cursor is.
* (int,int) WhereXY()
  * Returns a tuple containing both X and Y coordinates of cursor.
* HideCursor()
  * Hides cursor.
* ShowCursor()
  * Shows cursor.
* CursorStatus()
  * Returns 1 if the cursor is visible, 0 otherwise.
* ClrScr()
  * Clears console screen.
* ClrEOL()
  * Clears the current line from cursor position onwards.
* RawOn()
  * Enables raw terminal mode (prevents OS from handling buffers). Necessary for PendKey() and ReadKey(). Developers are adviced to call RawOff() before exiting program.
* RawOff()
  * Diables raw terminal mode and restores old status.
* IsRaw()
  * Returns true if raw mode is enabled.
* TextBackground(pycrt.Color color)
  * Sets the background of the text that will follow stdout from now on. Does not affect previous output. Argument must be of class Color (see below).
* TextColor(pycrt.Color color)
  * Sets the foreground of the text that will follow stdout from now on. Does not affect previous output. Argument must be of class Color (see below).
* SetBold(int value)
  * If value is 1, the following text output to stdout will be bold. Does not affect previous output. If value is 0, bold is disabled. Not all terminals support this format (those which don't, will simply ignore it).
* SetItalic(int value)
  * If value is 1, the following text output to stdout will be italic. Does not affect previous output. If value is 0, italic is disabled. Not all terminals support this format (those which don't, will simply ignore it).
* SetUnderline(int value)
  * If value is 1, the following text output to stdout will be underline. Does not affect previous output. If value is 0, underline is disabled. Not all terminals support this format (those which don't, will simply ignore it).
* SetStrike(int value)
  * If value is 1, the following text output to stdout will be striked out. Does not affect previous output. If value is 0, strike is disabled. Not all terminals support this format (those which don't, will simply ignore it).
* FormatReset()
  * Resets colors and format to terminal defaults.
* ReadKey()
  * Reads the next key in buffer and outputs is value as char. RAW mode should be enabled before. Throws pycrt.RawModeOffException if RAW Mode is off.
  
The following functions will be implemented soon:
* PendKey()
  * Returns true if there's a key in the buffer ready to be read. RAW mode should be enabled before. Throws pycrt.RawModeOffException if RAW Mode is off.
  
The following classes are available:
* class Color(Enum)
  * Enumeration of the available colors for TextColor and TextBackground, which are: DEFAULT (default terminal settings), BLACK,	RED, GREEN,	BROWN, BLUE, MAGENTA, CYAN and WHITE.
* class RawModeOffException(Exception)
  * Exception threwn if an operation requiring RAW mode to be enabled is called with this mode disabled.
  
## Which is the license for this?
This software is available as open-source software under the BSD license which follows:
```
 Python Console Resource Toolkit
 Copyright (c) 2015, Marc Sances
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