# Web Remote MPlayer

This nugget is forked from Nassty/web-remote-mplayer

I have reworked it to suit my own needs which is to simultaneously control three separate instances of itself spread accross separate playback devices. 

For best results install [hhpc](https://github.com/Aktau/hhpc) to hide the mouse pointer, set wallpaper to black and hide all UI elements (gnome extension [Just Perfection](https://extensions.gnome.org/extension/3843/just-perfection/) does the trick)

Additionally, you can add zindor_start.sh to your system startup so that the app will start automatically. 

### Notes:
`clean` option serves to manually remove .sock file after playback is finished as mplayed fails to do so. 
`nuke` option reboots the system provided that operating user has sufficient privileges. 