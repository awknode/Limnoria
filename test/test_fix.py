###
# Copyright (c) 2002-2005, Jeremiah Fincher
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#   * Redistributions of source code must retain the above copyright notice,
#     this list of conditions, and the following disclaimer.
#   * Redistributions in binary form must reproduce the above copyright notice,
#     this list of conditions, and the following disclaimer in the
#     documentation and/or other materials provided with the distribution.
#   * Neither the name of the author of this software nor the name of
#     contributors to this software may be used to endorse or promote products
#     derived from this software without specific prior written consent.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
###

## from __future__ import generators

from supybot.test import *

import random
import itertools

class FunctionsTest(SupyTestCase):
    def testRandomChoice(self):
        self.assertRaises(IndexError, random.choice, {})
        
    def testReversed(self):
        L = range(10)
        revL = list(reversed(L))
        L.reverse()
        self.assertEqual(L, revL, 'reversed didn\'t return reversed list')
        for _ in reversed([]):
            self.fail('reversed caused iteration over empty sequence')

    def testGroup(self):
        s = '1. d4 d5 2. Nf3 Nc6 3. e3 Nf6 4. Nc3 e6 5. Bd3 a6'
        self.assertEqual(group(s.split(), 3)[:3],
                         [['1.', 'd4', 'd5'],
                          ['2.', 'Nf3', 'Nc6'],
                          ['3.', 'e3', 'Nf6']])

    def testWindow(self):
        L = range(10)
        def wwindow(*args):
            return list(window(*args))
        self.assertEqual(wwindow([], 1), [], 'Empty sequence, empty window')
        self.assertEqual(wwindow([], 2), [], 'Empty sequence, empty window')
        self.assertEqual(wwindow([], 5), [], 'Empty sequence, empty window')
        self.assertEqual(wwindow([], 100), [], 'Empty sequence, empty window')
        self.assertEqual(wwindow(L, 1), [[x] for x in L], 'Window length 1')
        self.assertRaises(ValueError, wwindow, [], 0)
        self.assertRaises(ValueError, wwindow, [], -1)

    def testAny(self):
        self.failUnless(any(lambda i: i == 0, range(10)))
        self.failIf(any(None, range(1)))
        self.failUnless(any(None, range(2)))
        self.failIf(any(None, []))

    def testAll(self):
        self.failIf(all(lambda i: i == 0, range(10)))
        self.failIf(all(lambda i: i % 2, range(2)))
        self.failIf(all(lambda i: i % 2 == 0, [1, 3, 5]))
        self.failUnless(all(lambda i: i % 2 == 0, [2, 4, 6]))
        self.failUnless(all(None, ()))

    def testPartition(self):
        L = range(10)
        def even(i):
            return not(i % 2)
        (yes, no) = partition(even, L)
        self.assertEqual(yes, [0, 2, 4, 6, 8])
        self.assertEqual(no, [1, 3, 5, 7, 9])

    def testIlen(self):
        self.assertEqual(itertools.ilen(iter(range(10))), 10)

    def testRsplit(self):
        self.assertEqual(rsplit('foo bar baz'), 'foo bar baz'.split())
        self.assertEqual(rsplit('foo bar baz', maxsplit=1),
                         ['foo bar', 'baz'])
        self.assertEqual(rsplit('foo        bar baz', maxsplit=1),
                         ['foo        bar', 'baz'])
        self.assertEqual(rsplit('foobarbaz', 'bar'), ['foo', 'baz'])


class TestDynamic(SupyTestCase):
    def test(self):
        def f(x):
            i = 2
            return g(x)
        def g(y):
            j = 3
            return h(y)
        def h(z):
            self.assertEqual(dynamic.z, z)
            self.assertEqual(dynamic.j, 3)
            self.assertEqual(dynamic.i, 2)
            self.assertEqual(dynamic.y, z)
            self.assertEqual(dynamic.x, z)
            #self.assertRaises(NameError, getattr, dynamic, 'asdfqwerqewr')
            self.assertEqual(dynamic.self, self)
            return z
        self.assertEqual(f(10), 10)

    def testCommonUsage(self):
        foo = 'bar'
        def f():
            foo = dynamic.foo
            self.assertEqual(foo, 'bar')
        f()

# vim:set shiftwidth=4 tabstop=8 expandtab textwidth=78: