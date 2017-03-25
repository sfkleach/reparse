from abc import abstractmethod 
import sys
import re
import io

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
		line = sys.stdin.readline()
		if not line:
			raise StopIteration
		m = self._regex.match( line )
		if m:
			env.match = m.groups()
			self._body.interpret( env )
		else:
			raise Exception( 'Invalid line', line )

class Repeat( Action ):

	def __init__( self, body ):
		self._body = body

	def interpret( self, env ):
		try:
			while True:
				self._body.interpret( env )
		except StopIteration:
			pass

class Until( Action ):

	def __init__( self, regex, body ):
		self._regex = regex
		self._body = body

	def interpret( self, env ):
		try:
			raise Exception( 'TO BE DONE' )
		except StopIteration:
			pass

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

class TrimAll( Action ):

	def interpret( self, env ):
		env.match = [ v.strip() for v in env.match ]


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
