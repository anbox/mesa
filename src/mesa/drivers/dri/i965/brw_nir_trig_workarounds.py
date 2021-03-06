#! /usr/bin/env python
#
# Copyright (C) 2016 Intel Corporation
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice (including the next
# paragraph) shall be included in all copies or substantial portions of the
# Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
# IN THE SOFTWARE.

import nir_algebraic

# The SIN and COS instructions on Intel hardware can produce values
# slightly outside of the [-1.0, 1.0] range for a small set of values.
# Obviously, this can break everyone's expectations about trig functions.
#
# According to an internal presentation, the COS instruction can produce
# a value up to 1.000027 for inputs in the range (0.08296, 0.09888).  One
# suggested workaround is to multiply by 0.99997, scaling down the
# amplitude slightly.  Apparently this also minimizes the error function,
# reducing the maximum error from 0.00006 to about 0.00003.

trig_workarounds = [
   (('fsin', 'x'), ('fmul', ('fsin', 'x'), 0.99997)),
   (('fcos', 'x'), ('fmul', ('fcos', 'x'), 0.99997)),
]

print '#include "brw_nir.h"'
print nir_algebraic.AlgebraicPass("brw_nir_apply_trig_workarounds",
                                  trig_workarounds).render()
