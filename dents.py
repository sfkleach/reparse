# Converts indentation tokens into indents and outdents.
from tokenise import TokenType, Token

class Dent:

	def __init__( self, token_src ):
		self._previous = []
		self._token_src = token_src

	def previous( self ):
		try:
			return self._previous[ len( self._previous ) - 1 ]
		except:
			return ''

	def dent( self, token ):
		if token and token.isIndentation():
			v = token.tokenValue()
			if v == self.previous():
				return token
			else:
				print( 'COMPARE', len( self.previous() ), len( v ) )
				print( 'Stack', self._previous )
				if v.startswith( self.previous() ):
					self._previous.append( v )
					return Token( TokenType.Indentation, 1 )
				elif self.previous().startswith( v ):
					self._previous.pop()
					return Token( TokenType.Indentation, -1 )
				elif self.previous() == v:
					return token
				else:
					raise Exception( 'Indentation mixes tabs and spaces' )
		else:
			return token

	def nextOptToken( self ):
		return self.dent( self._token_src.nextOptToken() )

	def __next__( self ):
		t = self.nextOptToken()
		if t:
			return t
		else:
			raise StopIteration

	def __iter__( self ):
		return self
