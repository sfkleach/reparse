import dents
import tokenise
import io
import lexeme 

TEXT = '''ALPHA
  BETA
  GAMMA
DELTA
  EPSILON
    ZETA
    ETA
THETA
'''

def isIndent( L ):
	return (
		L.lexemeType() == lexeme.LexemeType.Indentation and
		L.lexemeValue() == 1
	)

def isOutdent( L ):
	return (
		L.lexemeType() == lexeme.LexemeType.Indentation and
		L.lexemeValue() == -1
	)

def test_dents():
	lexemes = [ *dents.Dent( tokenise.ReparseLexerFactory( io.StringIO( TEXT ) ) ) ]
	assert lexemes[ 0 ].lexemeType() != lexeme.LexemeType.Indentation
	assert isIndent( lexemes[ 1 ] )
	assert lexemes[ 2 ].lexemeType() != lexeme.LexemeType.Indentation
	assert lexemes[ 3 ].lexemeType() != lexeme.LexemeType.Indentation
	assert isOutdent( lexemes[ 4 ] )

	assert len( lexemes ) == 14

		# GOT HERE ... turn this into tests
		# <lexeme LexemeType.Symbol:ALPHA>
		# <lexeme LexemeType.Indentation:1>
		# <lexeme LexemeType.Symbol:BETA>
		# <lexeme LexemeType.Symbol:GAMMA>
		# <lexeme LexemeType.Indentation:-1>
		# <lexeme LexemeType.Symbol:DELTA>
		# <lexeme LexemeType.Indentation:1>
		# <lexeme LexemeType.Symbol:EPSILON>
		# <lexeme LexemeType.Indentation:1>
		# <lexeme LexemeType.Symbol:ZETA>
		# <lexeme LexemeType.Symbol:ETA>
		# <lexeme LexemeType.Indentation:-1>
		# <lexeme LexemeType.Indentation:-1>
		# <lexeme LexemeType.Symbol:THETA>
