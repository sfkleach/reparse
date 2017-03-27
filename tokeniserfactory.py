import abc
from collections import deque
from repeater import Repeater

class Tokeniser:

    def __init__( self, rules, repeater ):
        self._state = rules.startState()
        self._rules = rules
        self._repeater = repeater
        self._sofar = []
        self._pushed_tokens = []

    def __iter__( self ):
        return self

    def collected( self ):
        return ''.join( self._sofar )

    def collectedArray( self ):
        return ''.join( self._sofar )

    def pushToken( self, t ):
        self._pushed_tokens.append( t )

    def pushbackOptChar( self, optch ):
        self._repeater.pushbackOptChar( optch )

    def acceptOptChar( self, optch ):
        self._sofar.append( optch )

    def nextOptToken( self ):
        if self._pushed_tokens:
            return self._pushed_tokens.pop()
        while True:
            ch = self._repeater.nextOptChar()
            move = self._rules.findMove( self._state, ch )
            # print( 'Next char is: {}. Current state is: {}.'.format( ch, self._state ) )
            # print( ' Collected = ' + str( self._sofar ) )
            if move:
                move.processOptChar( ch, self )
                if move.isTerminus():
                    token = move.result( self )
                    self._state = self._rules.resetState()
                    self._sofar.clear()
                    return token
                else:
                    self._state = move.destination()
            elif ch:
                raise Exception( 'Unexpected character: {}'.format( ch ) )
            else:
                raise Exception( 'Unexpected end of input (in state {})'.format( self._state ) )
                
    def __next__( self ):
        token = self.nextOptToken()
        if token:
            return token
        else:
            raise StopIteration

class Move:

    def __init__( self, test, dst, *extras ):
        self._test = test
        self._dst = dst
        self._is_terminus = hasattr( dst, "__call__" )
        self._extras = extras

    def destination( self ):
        return self._dst

    def allows( self, optch ):
        # if optch == '1':
        #     print( 'here {}'.format( self._test ) )
        if self._test == True:
            return optch
        elif self._test:
            if hasattr( self._test, "__call__" ):
                return self._test( optch )
            else:
                return optch in self._test
        else:
            return not( optch )

    def isTerminus( self ):
        return self._is_terminus

    def result( self, tokeniser ):
        return self._dst( tokeniser )

    @abc.abstractmethod
    def doMove( self, ch, tokeniser ): pass

    def processOptChar( self, optch, tokeniser ):
        for e in self._extras:
            e( tokeniser )
        self.doMove( optch, tokeniser )

class Accept( Move ):
    def doMove( self, optch, tokeniser ):
        tokeniser.acceptOptChar( optch )

class Erase( Move ):
    def doMove( self, optch, tokeniser ):
        pass

class Pushback( Move ):
    def doMove( self, optch, tokeniser ):
        tokeniser.pushbackOptChar( optch )

class MoveSet:

    def __init__( self, *moves ):
        self._moves = moves

    def __iter__( self ):
        return iter( self._moves )
        
class TokeniserFactory:
    '''This is a casual implementation of a transition-diagram
    based tokeniser that has a lot of scope for optimisation.
    Since I am just doing a prototype, I won't bother with that.
    '''
    
    def __init__( self, node_dict, start=None, reset=None ): 
        self._moveset_dict = node_dict
        if start in self._moveset_dict:
            self._start_state = start
        else:
            raise Exception( 'Start state must be a named rule' )
        self._reset_state = reset if reset else self._start_state


    def findMove( self, state, optch ):
        for move in self._moveset_dict[ state ]:
            if optch and move.allows( optch ):
                return move
            elif not( optch ) and move.isTerminus():
                return move
        if optch:
            raise Exception( 'Unexpected character: {}'.format( optch ) )
        else:
            raise Exception( 'Unexpected end of input' )

    def startState( self ):
        return self._start_state

    def resetState( self ):
        return self._reset_state

    def __call__( self, source ):
        return Tokeniser( self, Repeater( source ) )
