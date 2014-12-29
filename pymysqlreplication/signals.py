# -*- coding: utf-8 -*-

from __future__ import absolute_import

from blinker import Namespace

# The namespace for code signals.  If you are not pymysqlreplication code, do
# not put signals in here.  Create your own namespace instead.
_signals = Namespace()
signal = _signals.signal
