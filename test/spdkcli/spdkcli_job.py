#!/usr/bin/env python3.5
import pexpect
import os
import sys


def execute_command(cmd, element=None, element_exists=False):
    child.sendline(cmd)
    child.expect("/>")
    if "error response" in child.before.decode():
        print("Error in cmd: %s" % cmd)
        exit(1)
    ls_tree = cmd.split(" ")[0]
    if ls_tree and element:
        child.sendline("ls %s" % ls_tree)
        child.expect("/>")
        print("child: %s" % child.before.decode())
        if element_exists:
            if element not in child.before.decode():
                print("Element %s not in list" % element)
                exit(1)
        else:
            if element in child.before.decode():
                print("Element %s is in list" % element)
                exit(1)


if __name__ == "__main__":
    socket = "/var/tmp/spdk.sock"
    if len(sys.argv) == 5:
        socket = sys.argv[4]
    testdir = os.path.dirname(os.path.realpath(sys.argv[0]))
    child = pexpect.spawn(os.path.join(testdir, "../../scripts/spdkcli.py") + " -s %s" % socket)
    child.expect(">")
    child.sendline("cd /")
    child.expect("/>")

    execute_command(*sys.argv[1:4])
