import io
from tokenise import ReparseLexerFactory
from lexeme import  LexemeType, Lexeme
from dents import Dent

def match( t, ttype_tvalue ):
	return (
		t.lexemeType() == ttype_tvalue[0] and
		t.lexemeValue() == ttype_tvalue[1]
	)

def parse( text ):
	return [ *Dent( ReparseLexerFactory( io.StringIO( text ) ) ) ]

def test_tokenise():
	text = 'Header[1]: "Foo"'
	lexemes = parse( text )
	assert match( lexemes[0], ( LexemeType.Symbol, 'Header' ) ), "UGLY {}, {}".format( lexemes[0].lexemeType(), lexemes[0].lexemeValue() )
	assert match( lexemes[1], ( LexemeType.Keyword, '[' )	)
	assert match( lexemes[2], ( LexemeType.NumLiteral, '1' ) )
	assert match( lexemes[3], ( LexemeType.Keyword, ']' ) )
	assert match( lexemes[4], ( LexemeType.Keyword, ':' ) )
	assert match( lexemes[5], ( LexemeType.StringLiteral, 'Foo' ) )
	assert len( lexemes ) == 6
	
def test_regex():
	text = '//(.*/)//'
	lexemes = parse( text )
	# print( lexemes[0].lexemeValue() )
	assert match( lexemes[0], ( LexemeType.RegexLiteral, '(.*/)' ) )
	assert len( lexemes ) == 1

def test_comment():
	text = 'Foo   # This is a comment\nBar\n'
	lexemes = parse( text )
	# print( lexemes[0].lexemeValue() )
	assert match( lexemes[0], ( LexemeType.Symbol, 'Foo' ) )
	assert match( lexemes[1], ( LexemeType.Symbol, 'Bar' ) )
	assert len( lexemes ) == 2
