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

	def nextOptToken( self ):
		while True:
			token = self._token_src.nextOptToken()
			if token and token.isIndentation():
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

	def __next__( self ):
		t = self.nextOptToken()
		if t:
			return t
		else:
			raise StopIteration

	def __iter__( self ):
		return self
