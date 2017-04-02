import io
from tokenise import ReparseTokeniserFactory
from lexeme import  LexemeType, Lexeme
from dents import Dent

def match( t, ttype_tvalue ):
	return (
		t.lexemeType() == ttype_tvalue[0] and
		t.lexemeValue() == ttype_tvalue[1]
	)

def test_tokenise():
	text = 'Header[1]: "Foo"'
	lexemes = [ *Dent( ReparseTokeniserFactory( io.StringIO( text ) ) ) ]
	assert match( lexemes[0], ( LexemeType.Symbol, 'Header' ) ), "UGLY {}, {}".format( lexemes[0].lexemeType(), lexemes[0].lexemeValue() )
	assert match( lexemes[1], ( LexemeType.Keyword, '[' )	)
	assert match( lexemes[2], ( LexemeType.NumLiteral, '1' ) )
	assert match( lexemes[3], ( LexemeType.Keyword, ']' ) )
	assert match( lexemes[4], ( LexemeType.Keyword, ':' ) )
	assert match( lexemes[5], ( LexemeType.StringLiteral, 'Foo' ) )
	assert len( lexemes ) == 6
	
def test_regex():
	text = '//(.*/)//'
	lexemes = [ *Dent( ReparseTokeniserFactory( io.StringIO( text ) ) ) ]
	# print( lexemes[0].lexemeValue() )
	assert match( lexemes[0], ( LexemeType.RegexLiteral, '(.*/)' ) )
	assert len( lexemes ) == 1
