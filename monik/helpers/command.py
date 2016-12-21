# -*- coding: utf-8 -*-
"""Provide helper for execute a command."""

import shlex
from subprocess import PIPE, Popen


class Command(object):
    """Provide a command executution."""

    def __init__(self, config):
        self.cmd = config.get('CMD_ON_STATUS_CHANGE', 'sleep 1')

    def run(self, params):
        """Run async command."""
        command = self.cmd.format(**params)
        Popen(shlex.split(command), stdout=PIPE, stderr=PIPE, shell=False)
