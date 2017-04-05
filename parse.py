import re
from lexeme import LexemeType
# from actions import SetHeader, Seq, Print, Repeat, Done, SetOutputFormat, Transform
import actions
import dents
import tokenise

class ReparseParser:

	def __init__( self, tokens ):
		self._tokens = dents.Dent( tokens )

	def mustReadToken( self, ttype, tvalue ):
		t = self._tokens.nextOptToken()
		if not t or t.lexemeType() != ttype or t.lexemeValue() != tvalue:
			raise Exception( 'Expected token "{}" but got "{}"'.format( tvalue, t[1] ) )
 
	def tryReadToken( self, ttype, tvalue ):
		t = self._tokens.peekOptToken()
		if not t or t.lexemeType() != ttype or t.lexemeValue() != tvalue:
			return False
		else:
			t = self._tokens.nextOptToken()
			return True
 
	def mustReadKeyword( self, tvalue ):
		self.mustReadToken( LexemeType.Keyword, tvalue )
 
	def tryReadKeyword( self, tvalue ):
		return self.tryReadToken( LexemeType.Keyword, tvalue )
 
	def readToken( self ):
		t = self._tokens.nextOptToken()
		if t:
			return t
		else:
			raise Exception( 'Unexpected end of file' )

	def readNumLiteral( self ):
		t = self._tokens.nextOptToken()
		if t:
			if t.isNumLiteral():
				try:
					return int( t.lexemeValue() )
				except ValueError:
					return float( t.lexemeValue() )
			else:
				raise Exception( 'Number needed: {}'.format( t.lexemeValue() ) )
		else:
			raise Exception( 'Unexpected end of file' )

	def readStringLiteral( self ):
		t = self._tokens.nextOptToken()
		if t:
			if t.isStringLiteral():
				return t.lexemeValue()
			else:
				raise Exception( 'String needed: {}'.format( t.lexemeValue() ) )
		else:
			raise Exception( 'Unexpected end of file' )

	def readRegexLiteral( self, with_newline=True ):
		t = self._tokens.nextOptToken()
		if t:
			if t.isRegexLiteral():
				return re.compile( t.lexemeValue() + ( '\\n' if with_newline else '' ) )
			else:
				raise Exception( 'String needed: {}'.format( t.lexemeValue() ) )
		else:
			raise Exception( 'Unexpected end of file' )

	def readCommand( self ):
		t = self._tokens.nextOptToken()
		if t:
			if t.isSymbol():
				v = t.lexemeValue()
				if v in PREFIX_TABLE:
					return PREFIX_TABLE[ v ]( self )
				else:
					raise Exception( 'Not implemented yet: {}'.format( v ) )
			else:
				raise Exception( 'Not implemented yet: {}'.format( t.lexemeType() ) )
		else:
			return None

	def readHeader( self ):
		self.mustReadToken( LexemeType.Keyword, '[' )
		num = self.readNumLiteral()
		self.mustReadToken( LexemeType.Keyword, ']' )
		self.mustReadToken( LexemeType.Keyword, ':' )
		self.mustReadToken( LexemeType.Symbol, 'Title' )
		self.mustReadToken( LexemeType.Keyword, '=' )
		title = self.readStringLiteral()
		return actions.SetHeader( title, num )

	def readPrintRepeat( self ):
		# self.mustReadToken( LexemeType.Keyword, ':' )		
		regex = self.readRegexLiteral()
		return actions.Repeat( regex, actions.Print() )

	def readPass( self ):
		return actions.Seq()

	def readDone( self ):
		return actions.Done()

	def readOutput( self ):
		self.mustReadToken( LexemeType.Keyword, ':' )
		self.mustReadToken( LexemeType.Symbol, 'Format' )
		self.mustReadToken( LexemeType.Keyword, '=' )
		format_style = self.readStringLiteral()
		return actions.SetOutputFormat( format_style )

	def readStatements( self ):
		sofar = []
		while True:
			e = self.readCommand()
			# print( 'Command', e )
			if not e:
				break
			sofar.append( e )
		return actions.Seq( *sofar )

	def readTransform( self ):
		self.mustReadKeyword( '[' )
		n = self.readToken()
		self.mustReadKeyword( ']' )
		callables = []
		if self.tryReadKeyword( ':' ):
			while True:
				key = self.readToken()
				try:
					callables.append( TRANSFORMS_TABLE[ key.lexemeValue() ] )
				except KeyError:
					raise Exception( 'Unrecognised transform: {}'.format( key.lexemeValue() ) )
				if not self.tryReadKeyword( ',' ):
					break
		if n.isNumLiteral():
			return actions.Transform( n.toInt(), *callables )
		else:
			return actions.TransformAll( *callables )

TRANSFORMS_TABLE = {
	'Trim': actions.TrimCallable,
	'Lowercase': str.lower,
	'Uppercase': str.upper
}

PREFIX_TABLE = {
	'Done': ReparseParser.readDone,
	'Header': ReparseParser.readHeader,
	'Output': ReparseParser.readOutput,
	'Pass': ReparseParser.readPass,
	'Print-Repeat': ReparseParser.readPrintRepeat,
	'Transform': ReparseParser.readTransform
}

def scriptParser( src ):
	return ReparseParser( tokenise.ReparseLexerFactory( src ) )
