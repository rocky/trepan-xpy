# -*- coding: utf-8 -*-
#  Copyright (C) 2020 Rocky Bernstein
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os.path as osp

from trepan.processor.command.info import InfoCommand as Trepan3kInfoCommand

class InfoCommand(Trepan3kInfoCommand):
    """Generic command for showing things about the program being debugged.

You can give unique prefix of the name of a subcommand to get
information about just that subcommand.

Type `info` for a list of *info* subcommands and what they do.
Type `help info *` for just a list of *info* subcommands.
"""

    aliases       = ('i',)
    category      = 'status'
    min_args      = 0
    max_args      = None
    name          = osp.basename(__file__).split('.')[0]
    need_stack    = False
    short_help    = 'Information about debugged program and its environment'

    def __init__(self, proc, name="info"):
        """Initialize info subcommands. Note: instance variable name
        has to be setcmds ('set' + 'cmds') for subcommand completion
        to work."""

        super().__init__(proc, name)
        self._load_debugger_subcommands(name, "trepanxpy")


if __name__ == '__main__':
    from trepan.processor.command import mock
    d, cp = mock.dbg_setup()
    command = InfoCommand(cp, 'info')
    command.run(['info'])
    pass
