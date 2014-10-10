#!/usr/bin/python

import os
import subprocess

def return_word():
    return "String"


def get_workspace():
    return os.getenv('WORKSPACE', "~/")


def traverse(directory):
    for cur, files in os.walk(directory):
        pref = ''
        head, tail = os.path.split(cur)
        while head:
            pref += '---'
            head, _tail = os.path.split(head)
        print(pref + tail)
        for f in files:
            print(pref + '---' + f)


def input_from_user():
    return input('What directory?: ')


def execute_command(command):
    try:
        return subprocess.check_output(["cd", "/opt"])
    except OSError:
        return None
