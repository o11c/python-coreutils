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


class MyArgumentParser(argparse.ArgumentParser):
    def _get_positional_actions(self):
        rv = super()._get_positional_actions()
        rv.append(None)
        return rv
    def _match_arguments_partial(self, actions, arg_strings_pattern):
        if actions and actions[-1] is None:
            n_formals = len(actions) - 1
            n_actuals = arg_strings_pattern.count('A')
            actions[-1:] = [actions[-2]] * (n_actuals - n_formals)
        return super()._match_arguments_partial(actions, arg_strings_pattern)


class MyAppendAction(argparse._AppendAction):
    def __init__(self, *args, **kwargs):
        assert kwargs.get('required')
        kwargs['required'] = False
        super().__init__(*args, **kwargs)


if 0:
    from ._util import intercept_all
    intercept_all(MyArgumentParser)
    intercept_all(MyAppendAction)
