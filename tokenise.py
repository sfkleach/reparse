from lexerfactory import LexerFactory, MoveSet, Accept, Pushback, Erase
from lexeme import Lexeme, LexemeType
import dents

ReparseLexerFactory = (
	LexerFactory(
	    { 
		    "StartLine": 
		    	MoveSet(
		            Accept( ' \t', "Indentation" ),
		            Pushback( True, lambda t: Lexeme( LexemeType.Indentation, t.collected() )  ),
		            Erase( None, lambda t: None )
		        ),
		    "Indentation":
		    	MoveSet(
		    		Accept( ' \t', "Indentation" ),
		    		Erase( '#', "EndOfLineComment", lambda t: t.clearAccepted() ),
		    		Pushback( True, lambda t: Lexeme( LexemeType.Indentation, t.collected() ) ),
		    		Erase( None, lambda t: None )
		    	),
		    "StartToken": 
			    MoveSet(
			        Erase( '\n', "StartLine" ),
			        Erase( ' \t', "StartToken" ),
			        Accept( '[]:', lambda t: Lexeme( LexemeType.Keyword, t.collected() ) ),
			        Accept( lambda x: x.isalpha(), "Symbol" ),
			        Accept( lambda x: x.isnumeric() or x in '+-', "Num" ),
			        Erase( '"', "String" ),
			        Accept( '/', "Slash" ),
			        Erase( '#', "EndOfLineComment" ),
			        Erase( None, lambda t: None )
			    ),
			"EndOfLineComment": 
				MoveSet(
					Erase( '\n', "StartLine" ),
					Erase( True, "EndOfLineComment" ),
					Erase( None, lambda t: None )
				),
			"Slash":
				MoveSet(
					Erase( '/', "Regex0", lambda t: t.clearAccepted() ),
					Pushback( True, lambda t: Lexeme( LexemeType.Symbol, t.collected() ) ),
					Erase( None, lambda t: Lexeme( LexemeType.Symbol, t.collected() ) )
				),
			"Regex0":
				MoveSet(
					Erase( '/', "Regex1" ),
					# Erase( '/', lambda t: Lexeme( LexemeType.RegexLiteral, t.collected() ) ),
					Accept( True, "Regex0" )
				),
			"Regex1":
				MoveSet(
					Erase( '/', lambda t: Lexeme( LexemeType.RegexLiteral, t.collected() ) ),
					Accept( True, "Regex0", lambda t: t.acceptOptChar( '/' ) )
				),			
			"Symbol":
				MoveSet(
			        Pushback( ' \t\n', lambda t: Lexeme( LexemeType.Symbol, t.collected() ) ),
			        Accept( lambda x: x.isalnum() or x in '_-', "Symbol" ),
			        Pushback( True, lambda t: Lexeme( LexemeType.Symbol, t.collected() ) ),
			        Erase( None, lambda t: Lexeme( LexemeType.Symbol, t.collected() ) )
				),
			"Num":
				MoveSet(
					Accept( lambda x: x.isnumeric(), "Num" ),
			        Pushback( True, lambda t: Lexeme( LexemeType.NumLiteral, t.collected() ) ),
			        Erase( None, lambda t: Lexeme( LexemeType.NumLiteral, t.collected() ) )
				),
			"String":
				MoveSet(
					Erase( '"', lambda t: Lexeme( LexemeType.StringLiteral, t.collected() ) ),
					Accept( True, "String" )
				)
	    },
	    start="StartLine",
	    reset="StartToken"
	)
)
