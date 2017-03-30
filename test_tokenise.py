import io
from tokenise import ReparseTokeniserFactory, TokenType, Token

def match( t, ttype_tvalue ):
	return (
		t.tokenType() == ttype_tvalue[0] and
		t.tokenValue() == ttype_tvalue[1]
	)

def test_tokenise():
	text = 'Header[1]: "Foo"'
	tokens = [ *ReparseTokeniserFactory( io.StringIO( text ) ) ]
	assert match( tokens[0], ( TokenType.Symbol, 'Header' ) )
	assert match( tokens[1], ( TokenType.Keyword, '[' )	)
	assert match( tokens[2], ( TokenType.NumLiteral, '1' ) )
	assert match( tokens[3], ( TokenType.Keyword, ']' ) )
	assert match( tokens[4], ( TokenType.Keyword, ':' ) )
	assert match( tokens[5], ( TokenType.StringLiteral, 'Foo' ) )
	assert len( tokens ) == 6
	
def test_regex():
	text = '//(.*/)//'
	tokens = [ *ReparseTokeniserFactory( io.StringIO( text ) ) ]
	print( tokens[0].tokenValue() )
	assert match( tokens[0], ( TokenType.RegexLiteral, '(.*/)' ) )
	assert len( tokens ) == 1