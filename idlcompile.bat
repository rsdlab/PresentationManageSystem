@echo off
cd /d %~dp0
setlocal
for %%I in (python.exe) do if exist %%~$path:I set f=%%~$path:I
if exist %f% (
  %f:python.exe=%omniidl.exe -bpython -I"%RTM_ROOT%rtm\idl" -I"/home/rsdlab/workspace/idl" -I"/home/rsdlab/workspace/FCSCServiceManagerORG/idl" -I"/home/rsdlab/workspace/WebCamera/idl" -I"/home/rsdlab/rtctree/idl" -I"/home/rsdlab/Downloads/OpenRTM-aist-1.1.2/src/lib/rtm/idl/device_interfaces" -I"/home/rsdlab/workspace/PresentationManageSystem/idl" idl/SpeechConsumer.idl idl/ActionManage.idl idl/SpeechProvider.idl idl/BasicDataType.idl 
) else (
  echo "python.exe" can not be found.
  echo Please modify PATH environmental variable for python command.
)
endlocal
