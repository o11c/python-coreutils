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


import functools
import types


def replace_code(code, **kwargs):
    arg_names = [
        'co_argcount',
        'co_kwonlyargcount',
        'co_nlocals',
        'co_stacksize',
        'co_flags',
        'co_code',
        'co_consts',
        'co_names',
        'co_varnames',
        'co_filename',
        'co_name',
        'co_firstlineno',
        'co_lnotab',
        'co_freevars',
        'co_cellvars',
    ]
    args = [
        kwargs.pop(arg_name, getattr(code, arg_name))
        for arg_name in arg_names
    ]
    if kwargs:
        raise TypeError('Unused arguments: %r' % sorted(kwargs))
    return types.CodeType(*args)


def intercept(cls, name):
    old_func = getattr(cls, name)
    if old_func is object.__new__:
        def old_func(cls, *args, **kwargs):
            return object.__new__(cls)

    @functools.wraps(old_func)
    def interceptor(self, *args, **kwargs):
        bits = []
        bits += [cls.__name__, '.', name, '(']
        for a in args:
            bits += [repr(a), ', ']
        for k, v in sorted(kwargs.items()):
            bits += [k, '=', repr(v), ', ']
        if args or kwargs:
            bits.pop()
        bits += [')']
        print(''.join(bits))
        return old_func(self, *args, **kwargs)
    interceptor.__name__ = name
    interceptor.__code__ = replace_code(interceptor.__code__, co_name='interceptor for ' + name)
    return interceptor


all_function_types = {
    type(object.__delattr__),
    type(object().__delattr__),
    type(object.__dir__),
    type(len),
    type(lambda: None),
}


def intercept_all(cls):
    for method_name in dir(cls):
        method_obj = getattr(cls, method_name)
        method_type = type(method_obj)
        if not callable(method_obj):
            continue
        if method_name in ('__class__', '__getattribute__'):
            continue
        assert not isinstance(method_obj, (type,))
        assert method_type in all_function_types, (method_name, method_type)
        setattr(cls, method_name, intercept(cls, method_name))


