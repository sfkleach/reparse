from abc import abstractmethod 
import sys
import re
import io
from collections import deque

def csvPrint( b, item ):
	if '"' in item:
		item = item.replace( '"', '""' )
	b.write( item )

class CSVPrint:

	def printRow( self, env ):
		b = sys.stdout
		gap = '"'
		for c in env.columns:
			b.write( gap )
			gap = ',"'
			csvPrint( b, env.match[c] )
			b.write( '"' )
		b.write( '\n' )

	def printHeader( self, env ):
		b = sys.stdout
		gap = '"'
		for name in env.column_names:
			b.write( gap )
			gap = ',"'
			csvPrint( b, name )
			b.write( '"' )
		b.write( '\n' )

class Environment:

	def __init__( self ):
		self.match = []
		self.vars = {}
		self.column_names = []
		self.columns = []
		self.printer = CSVPrint()
		self._peeked_lines = deque()	# Pop-front, Push-back.

	def nextLine( self ):
		if self._peeked_lines:
			return self._peeked_lines.popleft()
		else:
			return sys.stdin.readline()			

	def peekLine( self ):
		if self._peeked_lines:
			return self._peeked_lines[0]
		else:
			line = sys.stdin.readline()
			self._peeked_lines.append( line )
			return line

class Action:

	def __init__( self ):
		pass

	@abstractmethod
	def interpret( self, env ):
		pass

class Print( Action ):

	def interpret( self, env ):
		env.printer.printRow( env )

class PrintHeaderLine( Action ):

	def interpret( self, env ):
		env.printer.printHeader( env )

class Require( Action ):

	def __init__( self, regex, action ):
		self._regex = regex
		self._body = action

	def interpret( self, env ):
		line = env.nextLine()
		if not line:
			raise StopIteration
		m = self._regex.fullmatch( line )
		if m:
			env.match = m.groups()
			self._body.interpret( env )
		else:
			raise Exception( 'Invalid line', line )

class Repeat( Action ):

	def __init__( self, regex, body ):
		self._body = Require( regex, body )

	def interpret( self, env ):
		while True:
			line = env.peekLine()
			if not line:
				break
			self._body.interpret( env )

class Until( Action ):

	def __init__( self, regex, body ):
		self._regex = regex
		self._body = body

	def interpret( self, env ):
		while True:
			line = env.peekLine()
			if not line:
				break
			m = self._regex.fullmatch( line )
			if m:
				break
			else:
				self._body.interpret( env )

class SetHeader( Action ):

	def __init__( self, name, index1 ):
		self._index0 = index1 - 1
		self._name = name

	def interpret( self, env ):
		env.column_names.append( self._name )
		env.columns.append( self._index0 )

class Seq( Action ):

	def __init__( self, *args ):
		self._children = args

	def interpret( self, env ):
		for action in self._children:
			action.interpret( env )

class EndOfInput( Action ):

	def interpret( self, env ):
		line = env.peekLine()
		if line:
			raise Exception( 'Unprocessed lines at end of processing')

class TrimAll( Action ):

	def interpret( self, env ):
		env.match = [ v.strip() for v in env.match ]

class Transform( Action ):

	def __init__( self, index, *callables ):
		self._index = index
		self._callables = callables

	def interpret( self, env ):
		for c in self._callables:
			env.match[ self._index ] = c( env.match[ self._index ] )

class TransformAll( Action ):

	def __init__( self, index, callable ):
		self._index = index
		self._callable = callable

	def interpret( self, env ):
		env.match = [ self._callable( v ) for v in env.match ]

TrimCallable = str.strip
LowerCaseCallable = str.lower
UpperCaseCallable = str.upper
CaseFoldCallable = str.casefold


if __name__ == "__main__":
	import re
	Seq(
		SetHeader( 'Foo', 3 ),
		SetHeader( 'Bar', 2 ),
		SetHeader( 'Gort', 1),
		SetHeader( 'Flump', 1),
		PrintHeaderLine(),
		Repeat( 
			Require( 
				re.compile( '^(.{5})(.{10})(.{20})\n$' ),
				Seq( TrimAll(), Print() )
			) 
		)
	).interpret( Environment() )
