import argparse
import sys

import parse
import actions
import tokenise

# python3 reparse.py --script SCRIPT --input INPUT --output OUTPUT
def reparse():
	parser = argparse.ArgumentParser()
	parser.add_argument( "--script", "-s", metavar="FILE", help="Input script file", type=argparse.FileType( 'r' ), required=True )
	parser.add_argument( "--input", "-i", help="Input file to process (or - for stdin), defaults to stdin", default=sys.stdin, type=argparse.FileType( 'r' ) )
	parser.add_argument( "--output", "-o", help="Output file to generate (or - for stdout), defaults to stdout", default=sys.stdout, type=argparse.FileType( 'r' ) )
	args = parser.parse_args()
	program = parse.scriptParser( args.script ).readStatements()
	env = actions.Environment()
	env.input = args.input
	env.output = args.output
	program.interpret( env )

if __name__ == "__main__":
	reparse()
