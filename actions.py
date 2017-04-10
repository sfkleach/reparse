from abc import abstractmethod 
import sys
import re
import io
from collections import deque
import json

class FormatPrint:

	@abstractmethod
	def printRow( self, env ): pass

	@abstractmethod
	def printHeader( self, env ): pass

	@abstractmethod
	def printFooter( self, env ): pass

def csvPrint( b, item ):
	if '"' in item:
		item = item.replace( '"', '""' )
	b.write( item )

class CSVPrint( FormatPrint ):

	def printRow( self, env ):
		b = env.output
		gap = '"'
		for c in env.columns:
			b.write( gap )
			gap = ',"'
			csvPrint( b, env.match[c] )
			b.write( '"' )
		b.write( '\n' )

	def printHeader( self, env ):
		b = env.output
		gap = '"'
		for name in env.column_names:
			b.write( gap )
			gap = ',"'
			csvPrint( b, name )
			b.write( '"' )
		b.write( '\n' )

	def printFooter( self, env ):
		pass

class JSONPrint( FormatPrint ):

	def __init__( self ):
		self._gap = ''

	def printHeader( self, env ):
		b = env.output
		b.write( '[\n' )

	def printRow( self, env ):
		b = env.output
		b.write( self._gap )
		self._gap = ',\n'
		row = {}
		names = iter( env.column_names )
		for c in env.columns:
			row[ names.__next__() ] = env.match[c]
		json.dump( row, b )

	def printFooter( self, env ):
		b = env.output
		b.write( '\n]\n' )

class Wrapped( FormatPrint ):
	'''Wraps up an arbitrary format-print so that it will dynamically
	print the header at first call but not thereafter.
	'''

	def __init__( self, printer ):
		self._printer = printer

	def printHeader( self, env ):
		env.printer = self._printer
		env.printer.printHeader( env )

	def printRow( self, env ):
		self.printHeader( env )
		env.printer.printRow( env )

	def printFooter( self, env ):
		self.printHeader( env )
		env.printer.printFooter( env )

def choosePrinter( style ):
	if style == 'CSV':
		return CSVPrint()
	elif style == 'JSON':
		return JSONPrint()
	else:
		raise Exception( "Unknown style: {}".format( style) )


class Environment:

	def __init__( self, style='CSV' ):
		self.match = []
		self.vars = {}
		self.column_names = []
		self.columns = []
		self.printer = Wrapped( choosePrinter( style ) )
		self.tables = {}
		self._peeked_lines = deque()	# Pop-front, Push-back.
		self._lookup = None

	def nextLine( self ):
		if self._peeked_lines:
			return self._peeked_lines.popleft()
		else:
			return self.input.readline()			

	def peekLine( self ):
		if self._peeked_lines:
			return self._peeked_lines[0]
		else:
			line = self.input.readline()
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

class PrintHeader( Action ):

	def interpret( self, env ):
		env.printer.printHeader( env )

class PrintFooter( Action ):

	def interpret( self, env ):
		env.printer.printFooter( env )

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
			env.match = [ *m.groups() ]
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

	def __init__( self, regex, body, break_at_end = False ):
		self._regex = regex
		self._body = body
		self._break_at_end = break_at_end

	def interpret( self, env ):
		while True:
			line = env.peekLine()
			if not line:
				if self._break_at_end:
					break
				else:
					raise Exception( 'Unexpected end of input' )
			m = self._regex.fullmatch( line )
			if m:
				env.nextLine()
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

class SetOutputFormat( Action ):
	'''TODO: Don't allow if output has started'''

	def __init__( self, style ):
		self._style = style

	def interpret( self, env ):
		env.printer = Wrapped( choosePrinter( self._style ) )

class Seq( Action ):

	def __init__( self, *args ):
		self._children = args

	def interpret( self, env ):
		for action in self._children:
			action.interpret( env )

	def __len__( self ):
		return len( self._children )

	def __getitem__( self, n ):
		return self._children[ n ]

class EndOfInput( Action ):

	def interpret( self, env ):
		line = env.peekLine()
		if line:
			raise Exception( 'Unprocessed lines at end of processing')

class TrimAll( Action ):

	def interpret( self, env ):
		env.match = [ v.strip() for v in env.match ]


class TransformMixin( Action ):

	def __init__( self, callables, values ):
		self._callables = callables
		self._values = values

	def update( self, env, index ):
		c_iter = iter( self._callables )
		v_iter = iter( self._values )
		try:
			while True:
				c = c_iter.__next__()
				v = v_iter.__next__()
				r = c( env.match[ index ], option=v, env=env )
				env.match[ index ] = r
		except StopIteration:
			pass	

class Transform( TransformMixin ):

	def __init__( self, index, callables, values ):
		super().__init__( callables, values )
		self._index = index

	def interpret( self, env ):
		self.update( env, self._index - 1 )

class TransformAll( TransformMixin ):

	def __init__( self, callables, values ):
		self._callables = callables
		self._values = values

	def interpret( self, env ):
		for i in range( 0, env.match.lastindex ):
			self.update( env, i )

def TrimCallable( value, option=None, env=None ):
	return value.strip()

def LowerCaseCallable( value, option=None, env=None ):
	return value.lower()

def UpperCaseCallable( value, option=None, env=None ):
	return value.upper()

def CaseFoldCallable( value, option=None, env=None ):
	return value.casefold()

def UseTableCallable( value, option=None, env=None ):
	return env.tables[ option ]( value )

class Done( Action ):

	def interpret( self, env ):
		if env.nextLine():
			raise Exception( 'Extra lines found when end of input required' )

class Table( Action ):

	def __init__( self, name, error=None ):
		self._name = name
		self._error = error

	def interpret( self, env ):
		lookup = LookupFilter( name=self._name, error=self._error )
		env.tables[ self._name ] = lookup
		env._lookup = lookup

class Entry( Action ):

	def __init__( self, match, value ):
		self._match = match
		self._value = value

	def interpret( self, env ):
		if env._lookup:
			env._lookup.add( self._match, self._value )
		else:
			raise Exception( 'No Table definition encountered yet' )

class Rule:
	
	def __init__( self, match, value ):
		self._match = match
		self._value = value

	def matches( self, key ):
		raise Exception( 'To be implemented' )


class LookupFilter:
	'''A callable filter for use with Transform'''

	def __init__( self, name='', error=None ):
		self._name = name
		self._error = error
		self._rules = []

	def add( self, match, value ):
		self._rules.append( Rule( match, value ) )

	def __call__( self, key ):
		for r in self._rules:
			if r._match.fullmatch( key ):
				return r._value
		return self.fail( key )

	def fail( self, key ):
		if self._error:
			raise Exception( self._error )
		else:
			return key

if __name__ == "__main__":
	import re
	Seq(
		SetHeader( 'Foo', 3 ),
		SetHeader( 'Bar', 2 ),
		SetHeader( 'Gort', 1),
		SetHeader( 'Flump', 1),
		PrintHeader(),
		Repeat( 
			Require( 
				re.compile( '^(.{5})(.{10})(.{20})\n$' ),
				Seq( TrimAll(), Print() )
			) 
		)
	).interpret( Environment() )
