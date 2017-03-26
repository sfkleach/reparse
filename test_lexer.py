import io
from tokeniserfactory import TokeniserFactory, MoveSet, Accept, Erase, Pushback

def test_lexer():
	ttt = (
		TokeniserFactory(
		    { 
			    "start": 
			    	MoveSet(
			            Accept( 'a', 'grab_a' ),
			            Erase( True, 'start' ),
			            Erase( None, lambda t: None )
			        ),
			    "grab_a": 
				    MoveSet(
				        Accept( 'a', 'grab_a' ),
				        Erase( True, lambda t: t.collected() ),
				        Pushback( None, lambda t: t.collected() )
				    )
		    },
		    start="start"
		)
	)
	# t = ttt( io.StringIO( 'xxxxaaabaaca' ) )
	# print( t.nextOptToken() )
	# print( t.nextOptToken() )
	# print( t.nextOptToken() )
	# print( t.nextOptToken() )
	assert [ *ttt( io.StringIO( 'aaabaaca' ) ) ] == [ 'aaa', 'aa', 'a' ]

