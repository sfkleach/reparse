import parse
import tokenise
import io
import actions


def test_parse():
	text = 'Header[1]: Title="Foo"\nHeader[2]: Title="Bar"\nPrint-Repeat //(.{3})(.*)//\n'
	p = parse.scriptParser( io.StringIO( text ) ).readStatements()
	assert isinstance( p, actions.Seq ), type( p )
	assert isinstance( p[0], actions.SetHeader ), type( p )

def test_done():
	text = 'Done\n'
	p = parse.scriptParser( io.StringIO( text ) ).readStatements()
	assert isinstance( p, actions.Seq ), type( p )
	assert isinstance( p[0], actions.Done ), type( p )

if __name__ == "__main__":
    test_parse()
