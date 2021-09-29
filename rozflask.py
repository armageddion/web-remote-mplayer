#!/usr/bin/env python3

from app import app

@app.shell_context_processor
def make_shell_context():
    return