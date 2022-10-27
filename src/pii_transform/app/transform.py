"""
Command-line script to process data and perform PII substitutions
"""

import sys
import argparse
import json

from typing import List, Dict

from pii_data.types.localdoc import LocalSrcDocumentFile
from pii_data.types.piicollection import PiiCollectionLoader

from .. import VERSION
from ..helper.substitution import POLICIES
from ..api import PiiTransformer


class Log:

    def __init__(self, verbose: bool):
        self._v = verbose

    def __call__(self, msg: str, *args):
        if self._v:
            print(msg, *args, file=sys.stderr)


def get_policy(policy_file: str, log: Log) -> Dict:
    if not policy_file:
        return None
    log(". Loading policy file:", policy_file)
    with open(policy_file, encoding="utf-8") as f:
        return json.load(f)


def process(args: argparse.Namespace):

    log = Log(args.verbose)

    if args.hash_key and args.default_policy == "hash":
        args.default_policy = {"name": "hash", "key": args.hash_key}
    policy = get_policy(args.policy_file, log)
    trf = PiiTransformer(default_policy=args.default_policy,
                         policy=policy, placeholder_file=args.placeholder_file)

    log(". Loading document:", args.infile)
    doc = LocalSrcDocumentFile(args.infile)

    log(". Loading Pii collection:", args.pii)
    pii = PiiCollectionLoader()
    pii.load(args.pii)

    log(". Processing and dumping to:", args.outfile)
    out = trf(doc, pii)
    out.dump(args.outfile)



def parse_args(args: List[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=f"Transform detected PII instances in a document (version {VERSION})")

    g0 = parser.add_argument_group("Input/output paths")
    g0.add_argument("infile", help="source document file")
    g0.add_argument("pii", help="source detected PII collection")
    g0.add_argument("outfile", help="destination document file")

    g2 = parser.add_argument_group("Processing options")
    g2.add_argument("--default-policy", choices=POLICIES,
                    help="Apply a default policy to all entities")
    g2.add_argument("--policy-file",
                    help="JSON file with policies to be applied")
    g2.add_argument("--placeholder-file",
                    help="JSON file with substitution values for the placeholder policy")
    g2.add_argument("--hash-key",
                    help="key value for the hash policy")

    g3 = parser.add_argument_group("Other")
    g3.add_argument("-q", "--quiet", action="store_false", dest="verbose")
    g3.add_argument('--reraise', action='store_true',
                    help='re-raise exceptions on errors')
    g3.add_argument("--show-stats", action="store_true", help="show statistics")
    g3.add_argument("--show-tasks", action="store_true", help="show defined tasks")

    return parser.parse_args(args)


def main(args: List[str] = None):
    if args is None:
        args = sys.argv[1:]
    args = parse_args(args)
    try:
        process(args)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        if args.reraise:
            raise
        else:
            sys.exit(1)


if __name__ == "__main__":
    main()
