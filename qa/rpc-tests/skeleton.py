#!/usr/bin/env python

# Skeleton for python-based regression tests using
# JSON-RPC


# Add python-scarycoinrpc to module search path:
import os
import sys
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "python-scarycoinrpc"))

import json
import shutil
import subprocess
import tempfile
import traceback

from scarycoinrpc.authproxy import AuthServiceProxy, JSONRPCException
from util import *


def run_test(nodes):
    # Replace this as appropriate
    for node in nodes:
        assert_equal(node.getblockcount(), 200)
        assert_equal(node.getbalance(), 25*50)

def main():
    import optparse

    parser = optparse.OptionParser(usage="%prog [options]")
    parser.add_option("--nocleanup", dest="nocleanup", default=False, action="store_true",
                      help="Leave scarycoinds and test.* datadir on exit or error")
    parser.add_option("--srcdir", dest="srcdir", default="../../src",
                      help="Source directory containing scarycoind/scarycoin-cli (default: %default%)")
    parser.add_option("--tmpdir", dest="tmpdir", default=tempfile.mkdtemp(prefix="test"),
                      help="Root directory for datadirs")
    (options, args) = parser.parse_args()

    os.environ['PATH'] = options.srcdir+":"+os.environ['PATH']

    check_json_precision()

    success = False
    try:
        print("Initializing test directory "+options.tmpdir)
        if not os.path.isdir(options.tmpdir):
            os.makedirs(options.tmpdir)
        initialize_chain(options.tmpdir)

        nodes = start_nodes(2, options.tmpdir)
        connect_nodes(nodes[1], 0)
        sync_blocks(nodes)

        run_test(nodes)

        success = True

    except AssertionError as e:
        print("Assertion failed: "+e.message)
    except Exception as e:
        print("Unexpected exception caught during testing: "+str(e))
        stack = traceback.extract_tb(sys.exc_info()[2])
        print(stack[-1])

    if not options.nocleanup:
        print("Cleaning up")
        stop_nodes()
        shutil.rmtree(options.tmpdir)

    if success:
        print("Tests successful")
        sys.exit(0)
    else:
        print("Failed")
        sys.exit(1)

if __name__ == '__main__':
    main()
