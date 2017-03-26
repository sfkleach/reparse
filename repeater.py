from collections import deque
class Repeater:

	def __init__( self, source ):
		self._pushed = deque()
		self._source = source

	def __iter__( self ):
		return self

	def __next__( self ):
		ch = self.nextOptChar()
		if ch:
			return ch
		else:
			raise StopIteration

	def nextOptChar( self ):
		if self._pushed:
			return self._pushed.popleft()
		try:
			line = self._source.__next__()
			self._pushed.extend( line )
			if self._pushed:
				return self._pushed.popleft()
			return None
		except StopIteration:
			return None

	def pushbackOptChar( self, char ):
		self._pushed.appendleft( char )
