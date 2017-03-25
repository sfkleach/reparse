#!/usr/bin/env python3

import sys
import re

matcher = re.compile( '^(.{5})(.{10})(.{20})\n$' )

def parseStdin():
	for line in sys.stdin:
		m = matcher.match( line )
		if m:
			print( m.group(1), ",", m.group(2), ",", m.group(3), sep='' )

if __name__ == "__main__":
	parseStdin()
