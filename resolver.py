#! usr/bin/env python
# -*- coding: utf-8 -*-
########################################
#Author: CirQ
#Created Time: 2017-03-27 21:45:25
########################################
#
import re
import sys
#
class Resolver(object):
    def __init__(self):
        self.__checker = None
    
    @staticmethod
    def _gcd(a, b):  # b > a
        return Resolver._gcd(b, a%b) if a%b else b
    
    def _parse(self, s):
        self.__checker = re.compile(self._regex)
        mat = self.__checker.match(s)
        if mat:
            return mat.groups()
        else:
            return None
#
#
class Repeating(Resolver):
    def __init__(self):
        self._regex = r"^(\d+)\.(\d*)(\((\d+)\))?$"
    
    def _resolve(self, t):
        # integer part
        i = int(t[0])
        # finite decimal part
        f = (0, 1) if re.match(r"^0*$", t[1]) else (int(t[1]), 10**len(t[1]))
        # repeating decimal part
        r = (0, 1) if not (t[2] and re.match(r"^\d*[1-9]\d*$", t[3])) else \
                (int(t[3]), 10**len(t[1]) * (10**len(t[3])-1))
        n, d = i*f[1]*r[1]+f[0]*r[1]+r[0]*f[1], f[1]*r[1]
        gcd = self._gcd(n, d) if d > n else self._gcd(d, n)
        return "%d/%d" % (n/gcd, d/gcd)
#
class Rational(Resolver):
    def __init__(self):
        self._regex = r"^(\d*[1-9]\d*)/(\d*[1-9]\d*)$"
    
    def _resolva(self, t):
        n, d = int(t[0]), int(t[1])
        i, re = n/d, n%d
        res = {}
        f, p = "", 0
        while re not in res.keys():
            if re == 0:
                break
            res[re] = p
            while re < d:
                re *= 10
                if re < d:
                    f, p = "%s%d" % (f, 0), p+1
            f, p = "%s%d" % (f, re/d), p+1
            re %= d
        if f == "":
            return "%d" % i
        elif re == 0:
            return "%d.%s" % (i, f)
        else:
            return "%d.%s(%s)" % (i, f[:res[re]], f[res[re]:])
#
#
class RESOLVE(Repeating, Rational):
    def find(self, s):
        super(RESOLVE, self).__init__()
        tre = self._parse(s)
        if tre:
            return self._resolve(tre)
        super(Repeating, self).__init__()
        tra = self._parse(s)
        if tra:
            return self._resolva(tra)
        return "error format"
#
#
#
if __name__ == "__main__":
    r = RESOLVE()
    s = sys.argv[1]
    print r.find(s)
#
