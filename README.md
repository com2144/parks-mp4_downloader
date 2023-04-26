# parks-mp4_downloader
## mp4 downloader used shotgrid ami
###  - You must install anaconda3 env name py3.7
###  - The py3.7 pakage gat a PySide2, shotgun_api3

## initial registry setup
### [HKEY_CLASSES_ROOT\ShotGrid\shell\open\command]
#### "C:\Windows\System32\cmd.exe" "/k" "C:\{your_path}\parks-mp4_downloader\connect.bat" "%1"

### [batch file path]
#### C:\Users\admin\anaconda3\condabin\activate.bat py3.7 && python C:\{your_path}\parks-mp4_downloader\python\Mp4Download\controller.py %1
