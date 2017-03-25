#!/usr/bin/env python3

import random

def field1():
	txt = []
	for i in range( 0, 5 ):
		txt += chr( random.randrange( ord( 'A' ), ord( 'Z' ) ) )
	return ''.join( txt )

def field2():
	txt = []
	white = False
	for i in range( 0, 10 ):
		if white:
			txt += ' '
		else:
			white = random.random() < 0.1
			txt += chr( random.randrange( ord( '0' ), ord( '9' ) ) )
	return ''.join( txt )

def field3():
	txt = []
	for i in range( 0, 20 ):
		txt += chr( random.randrange( ord( 'a' ), ord( 'z' ) ) )
	return ''.join( txt )

def genTestData():
	for i in range( 0, 100000 ):
		print( '{}{}{}'.format( field1(), field2(), field3() ) )

if __name__ == "__main__":
	genTestData()
