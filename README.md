# parks-mp4_downloader
## mp4 downloader used shotgrid ami
###  - You must install anaconda3 env name py3.7
###  - The py3.7 pakage gat a PySide2, shotgun_api3

## initial registry setup
### https://developer.shotgridsoftware.com/ko/af0c94ce/#registering-a-protocol-on-windows

## window os setup
### in registry
### [HKEY_CLASSES_ROOT\ShotGrid\shell\open\command]
#### "C:\Windows\System32\cmd.exe" "/k" "C:\{your_path}\parks-mp4_downloader\connect.bat" "%1"

### [batch file path]
#### C:\{your_path}\anaconda3\condabin\activate.bat py3.7 && python C:\{your_path}\parks-mp4_downloader\python\Mp4Download\controller.py %1
#### pause

## linux os setup
#### cd ~/.local/share/applications
#### make shotgrid.desktop
#### [Desktop Entry]
Type=Application
Terminal=True
Name=shotgrid
Exec=/{your_path}/anaconda3/envs/py3.7/bin/python /{your_path}/parks-mp4_downloader/python/Mp4Download/view.py %u
Categories=Application
MimeType=x-scheme-handler/shotgrid
NoDisplay=Ture

#### and update-desktop-database ~/.local/share/applications

##### done.

