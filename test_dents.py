import dents
import tokenise
import io

TEXT = '''ALPHA
  BETA
  GAMMA
DELTA
  EPSILON
    ZETA
    ETA
THETA
'''

def test_dents():
	for t in dents.Dent( tokenise.ReparseLexerFactory( io.StringIO( TEXT ) ) ):
		print( t )

