#!/usr/bin/env python

import sys

print("Reticulating splines... ")


class Person:
    def __init__(self, name, email, identifies_as, searching_for):
        self.name = name
        self.email = email
        self.identifies_as = identifies_as
        self.searching_for = searching_for.split('|')
        self.matches = []

    def matches_with(self, possible_match):
        print("Attempting match: %s and %s" % (self.email, possible_match.email))
        try:
            i = possible_match.searching_for.index(self.identifies_as)
            j = self.searching_for.index(possible_match.identifies_as)
            print('Yep')
            return True
        except:
            print('Nope')
            return False



filename = sys.argv[1]
people = []

with open(filename) as fp:
    Lines = fp.readlines()
    for line in Lines:
        fields = line.strip().split(',')
        people.append(Person(fields[0],fields[1], fields[2], fields[3]))


count = 0
for p in people:
    for pm in people[count+1:]:
        if p.matches_with(pm):
            p.matches.append(pm)
            pm.matches.append(p)
    count += 1


for p in people:
    print("======================")
    if len(p.matches) == 0:
        print("No matches for %s" % p.email)
    for m in p.matches:
        print("Matched: %s and %s" % (p.email, m.email))

print("======================")
