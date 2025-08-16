#!/usr/bin/env python3

import sys
import random
from pathlib import Path

class OS:
    SYSCALLS = ['read', 'write', 'spawn']

    class Process:

        def __init__(self, func, *args):
            self._func = func(*args)

            self.retval = None

        def step(self):
            syscall, args, *_ = self._func.send(self.retval)
            self.retval = None
            return syscall, args

    def __init__(self, src):
        exec(src, globals())
        self.procs = [OS.Process(main)]
        self.buffer = ''

    def run(self):
        while self.procs:

            current = random.choice(self.procs)

            try:
                match current.step():
                    case 'read', _:
                        current.retval = random.choice([0, 1])
                    case 'write', s:
                        self.buffer += s
                    case 'spawn', (fn, *args):
                        self.procs += [OS.Process(fn, *args)]
                    case _:
                        assert 0

            except StopIteration:
                self.procs.remove(current)

        return self.buffer

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(f'Usage: {sys.argv[0]} file')
        exit(1)

    src = Path(sys.argv[1]).read_text()

    for syscall in OS.SYSCALLS:
        src = src.replace(f'sys_{syscall}',
                          f'yield "{syscall}", ')

    stdout = OS(src).run()
    print(stdout)
