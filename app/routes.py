#!/usr/bin/env python3

from flask import Flask, render_template, g,\
    redirect, url_for, session, request, json, make_response
from functools import wraps
import os
import mplayer
import re
from app import app

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

@app.route('/controls')
@check_running('explore', on_stop=True)
def controls():
    app.logger.info("loading controls")
    return render_template('controls.html')

@app.route('/command/', methods=['POST'])
def command():
    cmd = request.form['cmd']
    app.logger.info("processing command "+str(cmd))    
    g.mplayer.send_cmd(cmd)
    redirect = False
    #print('here')                                          #DEBUG
    if cmd == "quit":
        #print("here2")                                     #DEBUG
        cleanup()
        redirect = url_for('explore')
    return json.dumps({"redirect": redirect})

@app.route('/projector', methods=['GET','POST'])
def projector():    
    projector_idx = request.form['cmd']    
    app.logger.info("Routing to projector "+str(projector_idx))
    app.logger.info('http://'+app.config['PROJECTOR_'+str(projector_idx)]+':5001')
    #print('PROJECTOR_'+str(projector_idx))                 #DEBUG
    #print(app.config['PROJECTOR_'+str(projector_idx)])     #DEBUG
    return redirect('http://'+app.config['PROJECTOR_'+str(projector_idx)]+':5001')    

def cleanup(fifo_path='/tmp/mplayer-fifo.sock'):
    app.logger.info("cleaning up")
    try:
        os.unlink(fifo_path)
    except OSError:
        pass
