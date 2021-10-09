# Web Remote MPlayer

This nugget is forked from Nassty/web-remote-mplayer

I have reworked it to suit my own needs which is to simultaneously control three separate instances of itself spread accross separate playback devices. 

# Usage
* Turn on the machines! (side note:For projector 2, you may with to look at the screen while doing this because it has a bit of a boot procedure to follow: take keyboard, press F1, take a breath, press F2, take another breath, press “enter”… it’ll come up)
* Connect yourself to Backyard network with password: thereisnopassword
* Open web browser and navigate to:
** Projector 1 http://192.168.0.201:5001
** Projector 2 http://192.168.0.202:5001
** Projector 3 http://192.168.0.203:5001
(side note: once you navigate to any one of the projectors, you’ll be able to click buttons on the page to swap to any other projector)
* On this view, you will see one of two things:
** If video is playing, you’ll see playback controls
** if video isn’t playing, you’ll see a list of available videos for playback on that projector
(another side note: in rare event that video isn’t playing but you are seeing playback controls, use “clean” button and reload the page)
## Troubleshooting:
If something goes terribly wrong: things are frozen, system is non responsive or coffee is too cold - “Nuke” button will reboot the projector that you are currenly viewing in your web browser
In rare event that video isn’t playing but you are seeing playback controls, use “clean” button and reload the page. “Clean All” button does this to all projectors

### Notes:
`clean` option serves to manually remove .sock file after playback is finished as mplayed fails to do so. 
`nuke` option reboots the system provided that operating user has sufficient privileges. 

For best results install [hhpc](https://github.com/Aktau/hhpc) to hide the mouse pointer, set wallpaper to black and hide all UI elements (gnome extension [Just Perfection](https://extensions.gnome.org/extension/3843/just-perfection/) does the trick)

Additionally, you can add zindor_start.sh to your system startup so that the app will start automatically. 