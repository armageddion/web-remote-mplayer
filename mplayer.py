import subprocess
import os


class Mplayer(object):

    def __init__(self, filename=False, fifo_path='/tmp/mplayer-fifo.sock',
                 binary='mplayer'):

        self.filename = filename
        self.p = None
        self.fifo_path = fifo_path
        self.arguments = [
            binary,
            '-really-quiet',
            '-noconsolecontrols',
            '-slave',
            '-input',
            '-fs', #full screen
            'file=%s' % self.fifo_path,
        ]

    def load_file(self, filename):
        print("loading file")
        self.filename = filename
        return self

    def check_fifo(self):
        print("checking fifo")
        return os.path.exists(self.fifo_path)

    def remove_fifo(self):
        print("removing fifo")
        try:
            os.unlink(self.fifo_path)
        except OSError as e:
            print("OSError:")
            print(e)
            pass

    def start(self):
        print("mplayer starting")
        self.remove_fifo()
        os.mkfifo(self.fifo_path)
        self.p = subprocess.Popen(self.arguments + [self.filename])
        print(self.p)
        return self

    def send_cmd(self, *args):
        print("sending cmd to mplayer")
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
