import abc
from collections import deque

class TokenIterator:

	def __init__( self, rules, source ):
		self._state = rules.start()
		self._rules = rules
		self._source = source
		self._sofar = []
		self._pushed = deque()
		self._last_char = None

	def nextChar( self ):
		'''Returns the next character from the input stream. When the
		input stream is empty it returns None the first time it is called
		and throws StopIteration after that.
		'''
		if self._pushed:
			return self._pushed.popleft()
		elif self._source: 
			try:
				line = self._source.__next__()
				self._pushed.extend( line )

				# This test is necessary to cope with bad iterators that
				# return the empty string.
				if self._pushed:
					return self._pushed.popleft()
				else:
					self._source = None
					return None
			except StopIteration:
				self._source = None
				return None
		else:
			raise StopIteration

	def __iter__( self ):
		return self

	def __next__( self ):
		while True:
			ch = self.nextChar()

			# print( 'Next char is: {}. Current state is: {}.'.format( ch, self._state ) )
			# print( ' Pushed = ' + str( self._pushed ) )
			# print( ' Collected = ' + str( self._sofar ) )
			move = self._rules.findMove( self._state, ch )

			if move:
				move.processChar( ch, self._sofar, self._pushed )
				if move.isTerminus():
					accepted = self._sofar
					self._sofar = []
					self._state = self._rules.start()
					return move.result( accepted )
				else:
					self._state = move.destination()
			else:
				raise Exception( 'Unexpected character: {}'.format( ch ) )

class Move:

	def __init__( self, test, dst, *extras ):
		self._test = test
		self._dst = dst
		self._is_terminus = hasattr( dst, "__call__" )
		self._extras = extras

	def destination( self ):
		return self._dst

	def allows( self, ch ):
		if self._test == True:
			return ch
		elif self._test:
			return ch in self._test
		else:
			return not( self._test )

	def isTerminus( self ):
		return self._is_terminus

	def result( self, collected ):
		return self._dst( collected )

	@abc.abstractmethod
	def doMove( self, ch, collected ): pass

	def processChar( self, ch, collected, pushed ):
		for e in self._extras:
			e( collected, pushed=pushed )
		self.doMove( ch, collected, pushed )

class Accept( Move ):
	def doMove( self, ch, collected, pushed ):
		collected.append( ch )

class Erase( Move ):
	def doMove( self, ch, collected, pushed ):
		pass

class Pushback( Move ):
	def doMove( self, ch, collected, pushed ):
		pushed.append( ch )

class MoveSet:

	def __init__( self, *moves ):
		self._moves = moves

	def __iter__( self ):
		return iter( self._moves )
		
class TokenRules:
	'''This is a casual implementation of a transition-diagram
	based tokeniser that has a lot of scope for optimisation.
	Since I am just doing a prototype, I won't bother with that.
	'''
	
	def __init__( self, start_node, node_dict ): 
		self._start_state = start_node
		self._moveset_dict = node_dict

	def findMove( self, state, ch ):
		for move in self._moveset_dict[ state ]:
			if ch and move.allows( ch ):
				return move
			elif not( ch ) and move.isTerminus():
				return move
		return None

	def start( self ):
		return self._start_state

	def __call__( self, source ):
		return TokenIterator( self, source )



