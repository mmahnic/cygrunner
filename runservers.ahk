; Author: Marko Mahnič
; Created: October 2012
; License: GPL
#SingleInstance force

DetectHiddenWindows, On
hw_tohide = 0
is_hidden = 0
runnerWin := "CYGRUNNER"
xWin := "Cygwin/X"

FindWindow(name)
{
   IfWinNotExist, %name%
   {
      return 0
   }
   WinGet, winid, ID, %name%
   return winid
}

HideWindow(winid)
{
   global is_hidden
   WinHide, ahk_id %winid%
   is_hidden = 1   
}

ShowWindow(winid)
{
   global is_hidden
   if (winid <> 0)
   {
      WinShow, ahk_id %winid%
   }

   is_hidden = 0
}

StartXServer()
{
   global xWin
   IfWinNotExist, %xWin%
   {
      Run, C:\cygwin\bin\run.exe /usr/bin/bash.exe -l -c "/usr/bin/startxwin.exe exit",,Hide
      WinWait,, %xWin%, 10
   }
   IfWinNotExist, %xWin%
   { 
      return 0
   }
   return 1
}

StartCygRunner()
{
   global xWin, runnerWin
   IfWinNotExist, %xWin%
   {
      MsgBox, I don't see %xWin%
   }
   else
   {
      IfWinNotExist, %runnerWin%
      {
         Run, cmd.exe /C start /MIN "%runnerWin%" C:\cygwin\bin\bash --login -c 'python /usr/local/share/cygrunner/cygrunsrv.py',, Hide, CygRunPid
         WinWait,, %runnerWin%, 10
      }
   }
   IfWinNotExist, %runnerWin%
   {
      return 0
   }
   return 1
}

have_x := StartXServer()
have_runner := StartCygRunner()
hw_tohide := FindWindow(runnerWin)
HideWindow(hw_tohide)
;; MsgBox, X: %have_x%  runner: %have_runner%:%hw_tohide%  hider: %hw_hider%

OnExit, ExitSub

#F12::
if (is_hidden)
{
   ShowWindow(hw_tohide)
}
else
{
   HideWindow(hw_tohide)
}
return

ExitSub:
ShowWindow(hw_tohide)
ExitApp

DetectHiddenWindows, Off
