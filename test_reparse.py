import parse
import actions
import io
import unittest


class TestReparse( unittest.TestCase ):

	def test_done_fail( self ):
		text = 'Done\n'
		program = parse.scriptParser( io.StringIO( text ) ).readStatements()
		env = actions.Environment()
		env.input = io.StringIO( 'Not EOF' )
		self.assertRaises( Exception, program.interpret, env )

	def test_done_ok( self ):
		text = 'Done\n'
		program = parse.scriptParser( io.StringIO( text ) ).readStatements()
		env = actions.Environment()
		env.input = io.StringIO( '' )
		program.interpret( env )
