# -*- coding: utf-8 -*-
#  Copyright (C) 2009, 2013, 2015, 2020 Rocky Bernstein
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

from xpython.vmtrace import (
    PyVMEVENT_ALL,
    PyVMEVENT_INSTRUCTION,
)

from trepan.processor.command.base_cmd import DebuggerCommand

# Our local modules


class StepCommand(DebuggerCommand):
    """**step**[**+**|**-**|**<**|**>**|**!**] [*event*...] [*count*]

Execute the current simple statement, stopping at the next event.

With an integer argument, step that many times.

*event* is list of an event name which is one of: `call`,
`return`, `line`, `exception` `c-call`, `c-return` or `c-exception`.
If specified, only those stepping events will be considered. If no
list of event names is given, then any event triggers a stop when the
count is 0.

There is however another way to specify a *single* event, by
suffixing one of the symbols `<`, `>`, or `!` after the command or on
an alias of that.  A suffix of `+` on a command or an alias forces a
move to another line, while a suffix of `-` disables this requirement.
A suffix of `>` will continue until the next call. (`finish` will run
run until the return for that call.)

If no suffix is given, the debugger setting `different-line`
determines this behavior.

Examples:
---------

  step        # step 1 event, *any* event
  step 1      # same as above
  step 5/5+0  # same as above
  step line   # step only line events
  step call   # step only call events
  step>       # same as above
  step call line # Step line *and* call events

Related and similar is the `next` command.

See also:
---------

`next`, `skip`, `jump` (there's no `hop` yet), `continue`, `return` and
`finish` for other ways to progress execution.
"""

    aliases = (
        "step+",
        "step-",
        "step>",
        "step<",
        "step!",
        "s",
        "s+",
        "s-",
        "s<",
        "s>",
        "s!",
    )
    category = "running"
    execution_set = ["Running"]
    short_help = "Step into"

    DebuggerCommand.setup(locals(), category="running", max_args=1, need_stack=True)

    def run(self, args):
        # event_flags  = []
        # if args[0][-1] == '>':
        #     event_flags  = ['call']
        # elif args[0][-1] == '<':
        #     event_flags  = ['return']
        # elif args[0][-1] == '!':
        #     event_flags  = ["exception"]
        #     pass
        proc = self.proc
        core = self.core
        if len(args) <= 1:
            core.step_ignore = 0
        else:
            pos = 1
            if pos == len(args) - 1:
                core.step_ignore = self.proc.get_int(
                    args[pos], default=1, cmdname="step"
                )
                if self.core.step_ignore is None:
                    return False
                # 0 means stop now or step 1, so we subtract 1.
                core.step_ignore -= 1
                pass
            elif pos != len(args):
                self.errmsg("Invalid additional parameters %s" % " ".join(args[pos]))
                return False
            pass

        # All events except instruction tracing which is xor'd out.
        core.step_flags = proc.vm.frame.event_flags = (
            PyVMEVENT_ALL ^ PyVMEVENT_INSTRUCTION
        )

        core.different_line = (
            True  # Mcmdfns.want_different_line(args[0], self.settings['different'])
        )
        core.stop_level = None
        core.last_frame = None
        core.stop_on_finish = False
        proc.continue_running = True  # Break out of command read loop
        return True

    pass


if __name__ == "__main__":
    from trepan.processor.command.mock import MockDebugger

    d = MockDebugger()
    cmd = StepCommand(d.core.processor)
    for c in (["s", "5"], ["step", "1+2"], ["s", "foo"]):
        d.core.step_ignore = 0
        cmd.proc.continue_running = False
        result = cmd.run(c)
        print("Execute result: %s" % result)
        print("step_ignore %s" % repr(d.core.step_ignore))
        print("continue_running: %s" % cmd.proc.continue_running)
        pass
    for c in (["s"], ["step+"], ["s-"], ["s!"], ["s>"], ["s<"]):
        d.core.step_ignore = 0
        cmd.continue_running = False
        result = cmd.run(c)
        print("different line %s:" % c[0], cmd.core.different_line)
        pass
    pass
