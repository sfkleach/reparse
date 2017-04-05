import parse
import tokenise
import io
import actions

def readStatements( text ):
	return parse.scriptParser( io.StringIO( text ) ).readStatements()

def test_parse():
	text = 'Header[1]: Title="Foo"\nHeader[2]: Title="Bar"\nPrint-Repeat //(.{3})(.*)//\n'
	p = readStatements( text )
	assert isinstance( p, actions.Seq ), type( p )
	assert isinstance( p[0], actions.SetHeader ), type( p )

def test_done():
	text = 'Done\n'
	p = readStatements( text )
	assert isinstance( p, actions.Seq ), type( p )
	assert isinstance( p[0], actions.Done ), type( p )

def test_dummy_transform():
	text = 'Transform[1]\n'
	p = readStatements( text )
	assert isinstance( p, actions.Seq ), type( p )
	assert isinstance( p[0], actions.Transform ), type( p )
	assert not p[0]._callables 
	assert p[0]._index == 1

def test_dummy_transform_star():
	text = 'Transform[*]\n'
	p = readStatements( text )
	assert isinstance( p, actions.Seq ), type( p )
	assert isinstance( p[0], actions.TransformAll ), type( p )
	assert not p[0]._callables 

def test_transform_1argument():
	text = 'Transform[1]: Trim\n'
	p = readStatements( text )
	assert isinstance( p, actions.Seq ), type( p )
	assert isinstance( p[0], actions.Transform ), type( p )
	assert len( p[0]._callables ) == 1
	assert p[0]._callables[0]( ' foo  ' ) == 'foo'

def test_transform_1argument():
	text = 'Transform[1]: Trim, Uppercase, Lowercase\n'
	p = readStatements( text )
	assert isinstance( p, actions.Seq ), type( p )
	assert isinstance( p[0], actions.Transform ), type( p )
	assert len( p[0]._callables ) == 3
	assert p[0]._callables[0]( ' foo  ' ) == 'foo'
	assert p[0]._callables[1]( ' foo  ' ) == ' FOO  '
	assert p[0]._callables[2]( ' fOo  ' ) == ' foo  '


if __name__ == "__main__":
    test_parse()
