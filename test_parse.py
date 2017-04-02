import parse
import tokenise
import io

def test_parse():
	text = 'Header[1]: "Foo"\nHeader[2]: "Bar"\nPrint-Repeat //(.{3})(.*)//\n'
	p = parse.ReparseParser( tokenise.ReparseLexerFactory( io.StringIO( text ) ) )
	print( p.readStatements() )

if __name__ == "__main__":
    test_parse()
