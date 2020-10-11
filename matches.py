#!/usr/bin/env python

import sys
from random import *
import random

max_dates = int(sys.argv[2])
filename = sys.argv[1]


print("Reticulating splines... ")


class Person:
    def __init__(self, name, email, identifies_as, searching_for, extra_dates):
        self.name = name.strip()
        self.email = email.strip()
        self.identifies_as = identifies_as.strip()
        self.searching_for = searching_for.strip().split('|')
        self.extra_dates = extra_dates.strip()
        self.matches = []
        self.dates = []

    def matches_with(self, possible_match):
        print("Attempting match: %s and %s" % (self.email, possible_match.email))
        if self.identifies_as in possible_match.searching_for and possible_match.identifies_as in self.searching_for:
            print('Yep')
            return True
        else:
            print('Nope')
            return False

class Date:
    def __init__(self, person1, person2):
        self.people = sorted([person1, person2], key=lambda x: x.email)

    def __eq__(self, other):
        return self.people[0].email == other.people[0].email and self.people[1].email == other.people[1].email

    def __hash__(self):
        return hash(self.people[0].email + "@" + self.people[1].email)

# Reading CSV file
people = []
with open(filename) as fp:
    Lines = fp.readlines()
    for line in Lines:
        fields = line.strip().split(',')
        people.append(Person(fields[0],fields[1], fields[2], fields[3], fields[4]))


# Finding all possible matches
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

# Sorting based on least number of matches
print("======================")
sorted_people = sorted(people, key=lambda x: len(x.matches))

print("Sorting people based on number of matches")
for p in sorted_people:
    print("Person %s has %d matches" % (p.email, len(p.matches)))

# Creating matched dates
print("======================")
print("Sorting people based on number of matches")
for p in people:
    for m in p.matches:
        if len(m.dates) < max_dates and len(p.dates) < max_dates:
            p.dates.append(m)
            m.dates.append(p)
        else:
            print("Match didn't transform into date: %s and %s" % (p.email, m.email))

# Printing matched dates
for p in people:
    print("======================")
    if len(p.dates) == 0:
        print("No dates for %s" % p.email)
    for m in p.dates:
        print("It's a date! %s and %s" % (p.email, m.email))

# Adding extra dates (when possible)
print("======================")
count = 0
for p in people:
    for m in people[count+1:]:
        if p.extra_dates == "true" and m.extra_dates == "true":
            if len(m.dates) < max_dates and len(p.dates) < max_dates:
                print("Adding extra date: %s and %s" % (p.email, m.email))
                p.dates.append(m)
                m.dates.append(p)
    count += 1


# Printing all dates
all_dates = []
print("+++++++++++  All dates per person +++++++++++++++")
for p in people:
    print("======================")
    if len(p.dates) == 0:
        print("No dates for %s" % p.email)
    for m in p.dates:
        all_dates.append(Date(p,m))
        print("%s and %s" % (p.email, m.email))


print("+++++++++++  All dates +++++++++++++++")
unique_dates = list(set(all_dates))
for a in unique_dates:
    print("%s and %s" % (a.people[0].email, a.people[1].email))

print("======= Allocation dates ====== ")
# Calculating rooms
number_rooms = int(len(people)/2)
print("Using %d rooms per round" % number_rooms)
random.shuffle(unique_dates)

rounds = {}
for r in range(1, max_dates+1):
    busy_people = []
    to_remove = None
    print("Round %d, remaining %d dates" % (r, len(unique_dates)))
    for d in unique_dates:
        print("Date %s + %s " % (d.people[0].email, d.people[1].email))
        if d.people[0] not in busy_people and d.people[1] not in busy_people:
            print("Allocating %s + %s to %d" % (d.people[0].email, d.people[1].email, r))
            if r not in rounds:
                rounds[r] = []
            rounds[r].append(d)
            busy_people.append(d.people[0])
            busy_people.append(d.people[1])
            to_remove = d
        else:
            print("Skipping %s + %s to %d" % (d.people[0].email, d.people[1].email, r))

    if to_remove:
        unique_dates.remove(to_remove)


print("+++++++++++  Rooms +++++++++++++++")
for id, dates in rounds.items():
    print("===> Round %s" % id )
    for d in dates:
        print("%s + %s" % (d.people[0].email, d.people[1].email))
