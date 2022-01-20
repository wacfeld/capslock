#!/bin/env python3

import sys

# two flowchart formats:
# - dot (theirs)
# - mini (mine)

# questions have multiple named outputs
# commands have a single unnamed output
# each file starts with the name on one line
# followed by names of all things
# things ending in question marks are questions
# followed by their connections, one per line
# things are space separated
# all sections are separated by a space
# ex.
'''
collatz

0 even?
1 divide by two
2 multiply by three, add one

0 yes 1
0 no 2
1 0
2 0
'''

# see if string ends in '?'
def gettype(s):
    if s[-1] == '?':
        return 'q'
    else:
        return 'c'

# delete all blanks at front of list
def skipblanks(l):
    while l[0] == '':
        del l[0]

# not gonna implement anytime soon, hard
# def dot2mini():

# questions are ovals
# commands are rectangles
def mini2dot(minifile):
    dotfile = "digraph G {\n"

    minifile = minifile.split('\n')

    skipblanks(minifile)
    title = minifile[0]
    del minifile[0] # keep moving forward

    skipblanks(minifile)
    nametypes = {} # dictionary of name types (question/command)
    while(minifile[0]) != '': # assign names
        pair = minifile[0].split(maxsplit=1) # split on first space
        nametypes[pair[0]] = gettype(pair[1]) # store if it is a question
        dotfile += pair[0] + '[label="' + pair[1] + '"'
        if nametypes[pair[0]] == 'c': # command
            dotfile += ',shape=box'

        dotfile += '];\n'

        del minifile[0] # keep moving forward
    
    skipblanks(minifile)

    # connections
    while len(minifile) > 0 and minifile[0] != '':
        cur = minifile[0]
        src = cur.split(maxsplit=1)[0]
        mid = None
        dest = cur[::-1].split(maxsplit=1)[0][::-1] # reverse string, split, reverse

        dotfile += src + ' -> ' + dest
        # if nametypes[src] == 'q': # question
        if len(cur.split()) != 2: # label
            mid = cur.split(maxsplit=1)[1][::-1].split(maxsplit=1)[1][::-1] # cut off src, reverse, cut off dest, reverse
            dotfile += '[label="' + mid + '"]'
        
        dotfile += ";\n"

        del minifile[0] # tatakae
    
    # add title
    dotfile += 'labelloc="t";\n'
    dotfile += 'label="' + title + '";\n'
    
    dotfile += '}' # close

    return dotfile

# create a dictionary containing the structure of the flowchart
def interp(minifile):
    minifile = minifile.split('\n')

    del minifile[0] # remove title
    skipblanks(minifile)

    names = {} # dictionary of names
    while(minifile[0]) != '': # assign names
        pair = minifile[0].split(maxsplit=1) # split on first space
        names[pair[0]] = pair[1]

        del minifile[0]
    
    skipblanks(minifile)

    connections = {} # dictionary of connections
    while len(minifile) > 0 and minifile[0] != '':
        cur = minifile[0]
        src = names[cur.split(maxsplit=1)[0]]
        mid = None
        dest = names[cur[::-1].split(maxsplit=1)[0][::-1]] # reverse string, split, reverse
        
        # questions point to a dictionary with potential answers and destinations for them
        if gettype(src) == 'q':
            mid = cur.split(maxsplit=1)[1][::-1].split(maxsplit=1)[1][::-1] # cut off src, reverse, cut off dest, reverse

            if src in connections: # don't need to create it
                pass
            else:
                connections[src] = {} # create empty dict

            connections[src][mid] = dest
        # commands always have one destination
        else:
            connections[src] = dest

        del minifile[0]
    
    return connections

def run(minifile):
    connections = interp(minifile)

    cur = 'START' # always start at START
    while cur != 'END': # always end at END
        if gettype(cur) == 'q': # have to show options
            print(cur + ' (' + '/'.join(connections[cur].keys()) + ') ', end="")
        else:
            print(cur + ' ', end="")
        act = input()
        if gettype(cur) == 'c': # interpret as 'continue'
            cur = connections[cur]
        else: # question
            if act in connections[cur]:
                cur = connections[cur][act]
            else:
                print('invalid')

# TODO show options on question
# TODO allow going backwards
# TODO random access jumps
# TODO allowing options for non-questions. probably have everything be a dictionary, with empty dictionary meaning it's not a question

with open('what.mini') as f:
    minifile = f.read()
    run(minifile)
