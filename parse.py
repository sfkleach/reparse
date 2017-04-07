import re
from lexeme import LexemeType
import actions
import dents
import tokenise

class ReparseParser:

	def __init__( self, tokens ):
		self._tokens = dents.Dent( tokens )

	def mustReadToken( self, ttype, tvalue ):
		t = self._tokens.nextOptToken()
		if not t:
			raise Exception( 'Expected token "{}" but at end of input'.format( tvalue ) )
		if t.lexemeType() != ttype or t.lexemeValue() != tvalue:
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
 
	def tryReadIndent( self ):
		return self.tryReadToken( LexemeType.Indentation, 1 )
 
	def tryReadOutdent( self ):
		return self.tryReadToken( LexemeType.Indentation, -1 )
 
	def mustReadOutdent( self ):
		self.mustReadToken( LexemeType.Indentation, -1 )
 
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
		t = self._tokens.peekOptToken()
		if t:
			if t.isSymbol():
				v = t.lexemeValue()
				if v in PREFIX_TABLE:
					self._tokens.nextOptToken()
					return PREFIX_TABLE[ v ]( self )
				else:
					raise Exception( 'Not implemented yet: {}'.format( v ) )
			else:
				return None
		else:
			return None

	def readStatements( self ):
		sofar = []
		while True:
			e = self.readCommand()
			# print( 'Command', e )
			if not e:
				break
			sofar.append( e )
		return actions.Seq( *sofar )

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
		elif n.isKeyword( value="*" ):
			return actions.TransformAll( *callables )
		else:
			raise Exception( 'Not implemented yet: {} {}'.format( n.lexemeType(), n.lexemeValue() ) )

	def readUntil( self ):
		regex = self.readRegexLiteral()
		break_at_end = False
		if self.tryReadKeyword( ':' ):
			key = self.readToken()
			if key.isSymbol( value="At-End" ):
				self.mustReadKeyword( '=' )
				val = self.readToken()
				if val.isSymbol( value="Break" ):
					break_at_end = True
				else:
					raise Exception( 'Not implemented yet' )
			else:
				raise Exception( 'Until: unrecognised key: {}'.format( key.lexemeValue() ) )
		if self.tryReadIndent():
			stmnts = self.readStatements()
			self.mustReadOutdent()
			return actions.Until( regex, stmnts, break_at_end=break_at_end )
		else:
			return actions.Until( regex, actions.Seq(), break_at_end=break_at_end )

	def readRequire( self ):
		regex = self.readRegexLiteral()
		if self.tryReadIndent():
			stmnts = self.readStatements()
			self.mustReadOutdent()
			return actions.Require( regex, stmnts )
		else:
			return actions.Require( regex, actions.Seq() )

	def readPrint( self ):
		return actions.Print()

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
	'Print': ReparseParser.readPrint,
	'Print-Repeat': ReparseParser.readPrintRepeat,
	'Require': ReparseParser.readRequire,
	'Transform': ReparseParser.readTransform,
	'Until': ReparseParser.readUntil
}

def scriptParser( src ):
	return ReparseParser( tokenise.ReparseLexerFactory( src ) )
