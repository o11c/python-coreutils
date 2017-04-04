#   Copyright © 2017  Ben Longbons <brlongbons@gmail.com>
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.


import argparse
import os
from . import _argparse


__version__ = '0.0.1'


_BUFSIZ = 4096 * 16
STDIN_FILENO = 0
STDOUT_FILENO = 1
STDERR_FILENO = 2


def do_cat(ifd, ofd, *, unbuffered):
    # Currently, always act as if `unbuffered` is True.
    while True:
        buf = os.read(ifd, _BUFSIZ)
        if not buf:
            break
        while buf:
            n = os.write(ofd, buf)
            buf = buf[n:]


def main(argv=None):
    parser = _argparse.MyArgumentParser(description='concatenate files and print on the standard output')
    parser.add_argument('files', action=_argparse.MyAppendAction)
    parser.add_argument('--version', action='version', version=__version__, help='output version information and exit')
    parser.add_argument('-A', '--show-all', action='store_true', help='equivalent to -vET')
    parser.add_argument('-b', '--number-nonblank', action='store_true', help='number nonempty output lines, overrides -n')
    parser.add_argument('-e', action='store_true', help='equivalent to -vE')
    parser.add_argument('-E', '--show-ends', action='store_true', help='display $ at end of each line')
    parser.add_argument('-n', '--number', action='store_true', help='number all output lines')
    parser.add_argument('-s', '--squeeze-blank', action='store_true', help='suppress repeated empty output lines')
    parser.add_argument('-t', action='store_true', help='equivalent to -vT')
    parser.add_argument('-T', '--show-tabs', action='store_true', help='display TAB characters as ^I')
    parser.add_argument('-u', action='store_true', dest='unbuffered', help='force unbuffered output')
    parser.add_argument('-v', '--show-nonprinting', action='store_true', help='use ^ and M- notation, except for LFD and TAB')
    ns = parser.parse_args(argv)
    if ns.show_all:
        ns.show_nonprinting = True
        ns.show_ends = True
        ns.show_tabs = True
    del ns.show_all
    if ns.e:
        ns.show_nonprinting = True
        ns.show_ends = True
    del ns.e
    if ns.t:
        ns.show_nonprinting = True
        ns.show_tabs = True
    del ns.t
    if ns.files is None:
        ns.files = ['-']
    ns.unbuffered = True

    if ns.number or ns.number_nonblank:
        raise NotImplementedError
    if ns.show_ends or ns.show_nonprinting or ns.show_tabs:
        raise NotImplementedError
    if ns.squeeze_blank:
        raise NotImplementedError

    for f in ns.files:
        if f == '-':
            do_cat(STDIN_FILENO, STDOUT_FILENO, unbuffered=ns.unbuffered)
        else:
            fd = os.open(f, os.O_RDONLY)
            try:
                do_cat(fd, STDOUT_FILENO, unbuffered=ns.unbuffered)
            finally:
                os.close(fd)


if __name__ == '__main__':
    main()
