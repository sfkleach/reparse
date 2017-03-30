import parse
import tokenise
import io

def test_parse():
	text = 'Header[1]: "Foo"\nHeader[2]: "Bar"\nPrint-Repeat //(.{3})(.*)//\n'
	# for t in tokenise.ReparseTokeniserFactory( io.StringIO( text ) ):
	# 	print( 'TOKEN', t.tokenValue() )
	p = parse.ReparseParser( tokenise.ReparseTokeniserFactory( io.StringIO( text ) ) )
	print( p.readStatements() )