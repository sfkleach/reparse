# Converts indentation tokens into indents and outdents.
from lexeme import LexemeType, Lexeme

class Dent:

	def __init__( self, token_src ):
		self._previous = []
		self._token_src = token_src

	def previous( self ):
		try:
			return self._previous[ len( self._previous ) - 1 ]
		except:
			return ''

	def peekOptToken( self ):
		t = self.nextOptToken()
		self._token_src.pushToken( t )
		return t

	def nextOptToken( self ):
		while True:
			token = self._token_src.nextOptToken()
			if token:
				if token.isIndentation() and isinstance( token.lexemeValue(), str ) :
					v = token.lexemeValue()
					if v == self.previous():
						continue
					else:
						# print( 'COMPARE', len( self.previous() ), len( v ) )
						# print( 'Stack', self._previous )
						if v.startswith( self.previous() ):
							# It is a new, deeper indentation level.
							# Record the nesting level.
							self._previous.append( v )
							# Return an indent.
							return Lexeme( LexemeType.Indentation, 1 )
						else:
							# It is a shallower indentation level.
							# Keep popping the stack and pushing outdents.
							self._previous.pop()
							self._token_src.pushToken( token )
							return Lexeme( LexemeType.Indentation, -1 )
				else:
					return token
			elif self._previous:
				self._previous.pop()
				return Lexeme( LexemeType.Indentation, -1 )
			else:
				return token

	def __next__( self ):
		t = self.nextOptToken()
		if t:
			return t
		else:
			raise StopIteration

	def __iter__( self ):
		return self
