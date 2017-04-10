import actions
import re

def test_table():
	env = actions.Environment()
	t = actions.Table( "T" )
	assert not env._lookup
	assert not 'T' in env.tables
	t.interpret( env )
	assert env._lookup
	assert 'T' in env.tables
	assert env._lookup is env.tables[ 'T' ]

class test_Entry():

	def __init__( self ):
		env = actions.Environment()
		t = actions.Table( "T" )
		t.interpret( env )
		self._lookup = env._lookup
		e = actions.Entry( re.compile( 'abc' ), 'XYZ' )
		e.interpret( env )

	def test_rules( self ):
		assert len( self._lookup._rules ) == 1
		assert self._lookup._name == 'T'

	def test_valid( self ):
		# print( 'LOOKUP', 'abc', self._lookup( 'abc' ) )
		assert 'XYZ' == self._lookup( 'abc' )

	def test_fail( self ):
		assert 'pqr' == self._lookup( 'pqr' )

def test_UseTableCallable():
	env = actions.Environment()
	env.tables[ "MyTable" ] = actions.LookupFilter( name="T", error=None )
	env.tables[ "MyTable" ].add( re.compile( 'abc' ), 'xyz' )
	assert 'xyz' == actions.UseTableCallable( 'abc', option="MyTable", env=env )
