from main import Wyndex as wyndex
import argparse

parser = argparse.ArgumentParser(
    prog='Wyndex',
    description='A reporter, helping keep your code clean')

parser.add_argument('files', metavar='file', nargs='*',
                    help='file(s) to run Wyndex against')

parser.add_argument('--skip-tests', action='store_true', help='skip tests')

parser.add_argument('-c', '--commit', metavar='SHA', nargs='?',
                    dest='SHA', const='HEAD^', required=False,
                    help='use SHA to get files')

args = parser.parse_args()

if args.SHA:
    wyndex(SHA=args.SHA)
else:
    wyndex(args.files)

