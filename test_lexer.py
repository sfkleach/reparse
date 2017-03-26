import io
from lexer import TokenRules, MoveSet, Accept, Erase, Pushback

def test_lexer():
	ttt = (
		TokenRules(
		    "start",
		    { "start": 
		    	MoveSet(
		            Accept( 'a', 'grab_a' ),
		            Erase( True, 'start' ),
		            Erase( None, lambda x: ( 'id', ''.join( x ) ) )
		        ),
		    "grab_a": 
			    MoveSet(
			        Accept( 'a', 'grab_a' ),
			        Erase( True, lambda x: ''.join( x ) ),
			        Pushback( None, lambda x: ( 'id', ''.join( x ) ) )
			    )
		    }
		)
	)
	assert [ *ttt( io.StringIO( 'aaabaaca' ) ) ] == [ 'aaa', 'aa', 'a' ]

