"""Run from the installed skill root: python3 -B -m jev."""
import argparse
import json
import sys
from .core import MAX_INPUT, evaluate, key_available


def main():
    parser=argparse.ArgumentParser(description='Bounded advisory evaluation; never edits text.')
    parser.add_argument('command',choices=['status','evaluate'])
    parser.add_argument('--input',help='Authorized JSON document; stdin if omitted.')
    parser.add_argument('--pattern',help='Single-pattern diagnostic; not full coverage.')
    args=parser.parse_args()
    if args.command=='status':
        print(json.dumps({'status':'key_available' if key_available() else 'key_absent'}));return 0
    if not key_available():
        print(json.dumps(evaluate(None)));return 0
    try:
        if args.input:
            with open(args.input,'rb') as stream:data=stream.read(MAX_INPUT+1)
        else:data=sys.stdin.buffer.read(MAX_INPUT+1)
        if len(data)>MAX_INPUT: raise ValueError('invalid_input')
        document=json.loads(data)
        result=evaluate(document,only_pattern=args.pattern)
    except (OSError,ValueError,TypeError,UnicodeError,RecursionError):result={'status':'invalid_input'}
    print(json.dumps(result,ensure_ascii=False,allow_nan=False))
    return 0 if result['status'] in ('evaluated','key_absent') else 2


if __name__=='__main__': raise SystemExit(main())
