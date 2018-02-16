#!/usr/bin/python3
# encoding=utf-8
# Copyright © 2016 Intel Corporation

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""Flask webpage for performance data."""

import itertools

# pylint: disable=import-error
import flask
from flask_mako import MakoTemplates, render_template
# pylint: enable=import-error

APP = flask.Flask(__name__)
_ = MakoTemplates(APP)

# pylint: disable=bad-whitespace
_BENCHMARKS = [
    ('gfxbench5_fill',                              'micro-benchmark'    ),
    ('gfxbench5_fill_o',                            'micro-benchmark'    ),
    ('gfxbench5_alu2',                              'micro-benchmark'    ),
    ('gfxbench5_alu2_o',                            'micro-benchmark'    ),
    ('gfxbench5_driver2',                           'micro-benchmark'    ),
    ('gfxbench5_driver2_o',                         'micro-benchmark'    ),
    ('gfxbench5_manhattan',                         'synthetic-benchmark'),
    ('gfxbench5_manhattan_o',                       'synthetic-benchmark'),
    ('gfxbench5_car_chase',                         'synthetic-benchmark'),
    ('gfxbench5_car_chase_o',                       'synthetic-benchmark'),
    ('gfxbench5_tess',                              'synthetic-benchmark'),
    ('gfxbench5_tess_o',                            'synthetic-benchmark'),
    ('gfxbench5_trex',                              'synthetic-benchmark'),
    ('gfxbench5_trex_o',                            'synthetic-benchmark'),
    ('gfxbench5_aztec_ruins_gl_normal',             'synthetic-benchmark'),
    ('gfxbench5_fill_windowed',                     'micro-benchmark'    ),
    ('gfxbench5_fill_o_windowed',                   'micro-benchmark'    ),
    ('gfxbench5_alu2_windowed',                     'micro-benchmark'    ),
    ('gfxbench5_alu2_o_windowed',                   'micro-benchmark'    ),
    ('gfxbench5_driver2_windowed',                  'micro-benchmark'    ),
    ('gfxbench5_driver2_o_windowed',                'micro-benchmark'    ),
    ('gfxbench5_manhattan_windowed',                'synthetic-benchmark'),
    ('gfxbench5_manhattan_o_windowed',              'synthetic-benchmark'),
    ('gfxbench5_car_chase_windowed',                'synthetic-benchmark'),
    ('gfxbench5_car_chase_o_windowed',              'synthetic-benchmark'),
    ('gfxbench5_tess_windowed',                     'synthetic-benchmark'),
    ('gfxbench5_tess_o_windowed',                   'synthetic-benchmark'),
    ('gfxbench5_trex_windowed',                     'synthetic-benchmark'),
    ('gfxbench5_trex_o_windowed',                   'synthetic-benchmark'),
    ('gfxbench5_aztec_ruins_gl_normal_windowed',    'synthetic-benchmark'),
]
# pylint: enable=bad-whitespace


class _Getter(object):
    """A container for making working with benchmark data easier.

    Stores dictionaries relating each element to each other, allowing for fast
    searches.

    """
    def __init__(self):
        self.by_name = dict(iter(_BENCHMARKS))
        self.by_category = {c: [n[0] for n in b] for c, b in itertools.groupby(
            sorted(_BENCHMARKS, key=lambda x: x[1]), lambda x: x[1])}


GETTER = _Getter()


@APP.route('/')
def front():
    return render_template('index.html.mako', getter=GETTER)


@APP.route('/apps/all')
def all():  # pylint: disable=redefined-builtin
    return render_template('apps.html.mako', benchmarks=dict(_BENCHMARKS),
                           category="All Benchmarks")


@APP.route('/apps/<benchmark>')
def apps(benchmark):
    return render_template(
        'apps.html.mako',
        benchmarks=[benchmark],
        category=None)


@APP.route('/categories/<category>')
def categories(category):
    return render_template(
        'apps.html.mako',
        benchmarks=GETTER.by_category[category],
        category=category)


if __name__ == '__main__':
    APP.run()
