import subprocess
import os
from app import app

class Mplayer(object):

    def __init__(self, filename=False, fifo_path='/tmp/mplayer-fifo.sock',
                 binary='mplayer'):

        self.filename = filename
        self.p = None
        self.fifo_path = fifo_path
        self.arguments = [
            binary,
            #'-really-quiet',
            '-fs', #full screen            
            '-nogui',
            '-noconsolecontrols',
            '-slave',
            '-input',
            'file=%s' % self.fifo_path,
        ]

    def load_file(self, filename):
        app.logger.info("loading file")
        self.filename = filename
        return self

    def check_fifo(self):
        app.logger.info("checking fifo")
        return os.path.exists(self.fifo_path)

    def remove_fifo(self):
        app.logger.info("removing fifo")
        try:
            os.unlink(self.fifo_path)
        except OSError as e:
            app.logger.warn("OSError:")
            app.logger.warn(e)
            pass

    def start(self):
        app.logger.info("mplayer starting")
        self.remove_fifo()
        os.mkfifo(self.fifo_path)
        app.logger.info("starting subprocess")
        #print(self.arguments + [self.filename])   # DEBUG
        self.p = subprocess.Popen(self.arguments + [self.filename])
        #print(self.p)  #DEBUG
        return self

    def send_cmd(self, *args):
        app.logger.info("sending cmd to mplayer")
        with open(self.fifo_path, 'w') as sock:
            cmd = " ".join(args)
            sock.write("%s\n" % cmd)
            sock.flush()
            if cmd == 'quit':
                self.remove_fifo()
        return self

    def kill(self):
        print("self kill")
        self.p.kill()
        return self
