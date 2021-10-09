#!/usr/bin/env python3

from flask import Flask, render_template, g,\
    redirect, url_for, session, request, json, make_response
from functools import wraps
import os
import requests
import re
from app import app,mplayer

@app.before_request
def get_mplayer():
    g.mplayer = mplayer.Mplayer()
    g.extensions = ('.avi', '.mp4', '.m4a', '.mov', '.mpg', '.mpeg',
                    '.ogg', '.flac', '.mkv')

def check_running(endpoint='controls', on_stop=False):
    def outer(f):
        @wraps(f)
        def inner(*args, **kwargs):
            if not g.mplayer.check_fifo():
                if on_stop:
                    return redirect(url_for(endpoint))
                return f(*args, **kwargs)

            if on_stop:
                return f(*args, **kwargs)
            return redirect(url_for(endpoint))
        return inner
    return outer

# search and display directory listing
@app.route('/', defaults={"path": "Downloads"}, methods=['GET','POST'])
@app.route('/index', methods=['GET','POST'])
@app.route('/explore/<path:path>')
@check_running()
def explore(path):
    app.logger.info("Exploring directory "+str(path))
    directories = []
    files = []
    internal_path = os.path.join(app.config['USER_HOME'], path)
    for content in os.listdir(internal_path):
        fullpath = os.path.join(internal_path, content)
        if os.path.isdir(fullpath) and not content.startswith('.'):
            directories.append((os.path.join(path, content), content))
        else:
            ext = os.path.splitext(content)[-1].lower()
            if ext in g.extensions:
                filepath = (os.path.join(path, content))
                sub_exists = os.path.exists(os.path.join(
                    internal_path, content.replace(ext, '.srt')))
                files.append((filepath, content, sub_exists))

    app.logger.info("Found things")

    parent = list(os.path.split(path))
    parent.pop()
    parent = os.path.join(*parent)
    parent = (parent, os.path.basename(parent))
    directories.sort(key=natural_key)
    files.sort(key=natural_key)

    app.logger.info("done exploring")
    return render_template('listing.html', files=files,
                           directories=directories, title=parent)

# natural key for sorting
def natural_key(string_):
    """See http://www.codinghorror.com/blog/archives/001018.html"""
    return [int(s) if s.isdigit() else s for s in re.split(r'(\d+)',
                                                           string_[0])]

# play a video in path
@app.route('/play/<path:path>')
@check_running()
def play(path):
    app.logger.info("playing... "+str(path))
    full_path = os.path.join(app.config['USER_HOME'], path)
    if not g.mplayer.check_fifo():
        session['filename'] = full_path
        g.mplayer.load_file(full_path)
        g.mplayer.start()
    return redirect(url_for('controls'))

# display playback controls
@app.route('/controls')
@check_running('explore', on_stop=True)
def controls():
    app.logger.info("loading controls")
    return render_template('controls.html')

# process playback controll commands
@app.route('/command/', methods=['POST'])
def command():
    redirect = False
    cmd = request.form['cmd']
    app.logger.info("processing command "+str(cmd))
    try:
        g.mplayer.send_cmd(cmd)
        if cmd == "quit":
            cleanup()
            redirect = url_for('explore')
    except Exception as e:
        app.logger.error("failed to process /ctrl/ command")
        app.logger.error("Exception: "+str(e))
        app.logger.warn("trying to recover")            
    return json.dumps({"redirect": redirect})

# play a predefined collection of videos on all outputs at once
@app.route('/playset/', methods=['POST'])
@check_running()
def playset():
    vidset = request.form['cmd']
    app.logger.info("playing vidset: "+str(vidset))
    print(type(vidset))     #DEBUG
    if vidset == '1_1':
        r1 = requests.get(app.config['PROJECTOR_1']+'/play/Downloads/01_01_01C_Tolaan_ROZ_Play_Test.mov')

    if vidset == '1_2':
        r2 = requests.get(app.config['PROJECTOR_2']+'/play/Downloads/01_02_02C_Krinu_ROZ_Play_Test.mov')

    if vidset == '1_3':
        r3 = requests.get(app.config['PROJECTOR_3']+'/play/Downloads/01_03_03C_Ubo_ROZ_Play_Test.mov')

    if vidset == '2_1':
        r1 = requests.get(app.config['PROJECTOR_1']+'/play/Downloads/02_01_01C_Tolaan_ROZ_Play_Test.mov')
        r2 = requests.get(app.config['PROJECTOR_2']+'/play/Downloads/02_01_02C_Krinu_ROZ_Play_Test.mov')
        r3 = requests.get(app.config['PROJECTOR_3']+'/play/Downloads/02_01_03C_Ubo_ROZ_Play_Test.mov')

    if vidset == '2_2':
        r1 = requests.get(app.config['PROJECTOR_1']+'/play/Downloads/02_02_01C_Tolaan_ROZ_Play_Test.mov') 
        r2 = requests.get(app.config['PROJECTOR_2']+'/play/Downloads/02_02_02C_Krinu_ROZ_Play_Test.mov') 
        r3 = requests.get(app.config['PROJECTOR_3']+'/play/Downloads/02_02_03C_Ubo_ROZ_Play_Test.mov') 

    if vidset == '2_3':
        r1 = requests.get(app.config['PROJECTOR_1']+'/play/Downloads/02_03_01C_Tolaan_ROZ_Play_Test.mov')
        r2 = requests.get(app.config['PROJECTOR_2']+'/play/Downloads/02_03_02C_Krinu_ROZ_Play_Test.mov')
        r3 = requests.get(app.config['PROJECTOR_3']+'/play/Downloads/02_03_03C_Ubo_ROZ_Play_Test.mov')

    if vidset == '2_4':
        r1 = requests.get(app.config['PROJECTOR_1']+'/play/Downloads/02_04_01C_Tolaan_ROZ_Play_Test.mov')
        r2 = requests.get(app.config['PROJECTOR_2']+'/play/Downloads/02_04_02C_Krinu_ROZ_Play_Test.mov')
        r3 = requests.get(app.config['PROJECTOR_3']+'/play/Downloads/02_04_03C_Ubo_ROZ_Play_Test.mov')

    if vidset == '3_1':
        r1 = requests.get(app.config['PROJECTOR_1']+'/play/Downloads/03_01_01C_Tolaan_ROZ_Play_Test.mov') 
        r2 = requests.get(app.config['PROJECTOR_2']+'/play/Downloads/03_01_02C_Krinu_ROZ_Play_Test.mov') 
        r3 = requests.get(app.config['PROJECTOR_3']+'/play/Downloads/03_01_03C_Ubo_ROZ_Play_Test.mov') 

    return json.dumps({"redirect": (url_for('explore'))})

# administrative routes for just in case
@app.route('/ctrl/', methods=['POST'])
def ctrl():
    cmd = request.form['cmd']
    app.logger.info("processing ctrl command "+str(cmd))
    try:
        if cmd == "quitall":
            # quit all playbacks
            requests.post(app.config['PROJECTOR_1']+'/command/', data={"cmd": "quit"})
            requests.post(app.config['PROJECTOR_2']+'/command/', data={"cmd": "quit"})
            requests.post(app.config['PROJECTOR_3']+'/command/', data={"cmd": "quit"})        
        if cmd == "clean":
            # OS remove fifo file
            g.mplayer.remove_fifo()
        if cmd == "cleanall":
            # call clean on all projectors
            requests.post(app.config['PROJECTOR_1']+'/ctrl/', data={"cmd": "clean"})
            requests.post(app.config['PROJECTOR_2']+'/ctrl/', data={"cmd": "clean"})
            requests.post(app.config['PROJECTOR_3']+'/ctrl/', data={"cmd": "clean"})
        if cmd == "nuke":
            #reboot system
            os.system('sudo reboot')
    except Exception as e:
        app.logger.error("failed to process /ctrl/ command")
        app.logger.error("Exception: "+str(e))
        app.logger.warn("trying to recover")

    return json.dumps({"redirect": (url_for('explore'))})

def cleanup(fifo_path='/tmp/mplayer-fifo.sock'):
    app.logger.info("cleaning up")
    try:
        os.unlink(fifo_path)
    except OSError:
        pass
