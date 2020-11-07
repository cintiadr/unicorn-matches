import sys
# import random
# from shutil import rmtree
# import os

from person import Person,print_people
from date import Date,generate_possible_dates, retrieve_hc_dates
from input_file import read_input_file
from config import room_names

print(" ** Reticulating splines... ")

print("\n ==> Reading application arguments \n")
max_dates = int(sys.argv[2])
filename = sys.argv[1]
print("\n ==> Finished reading application arguments \n")



# Returns metadata about matching fields and people to be included (dict indexed by email)
matching_fields, people = read_input_file(filename)

# Returns list for all possible dates
possible_dates = generate_possible_dates(matching_fields, people)

# Returns high compatibility matches (dict indexed by email)
hc_possible_dates = retrieve_hc_dates(matching_fields, possible_dates)


# # Sorting based on least number of matches
# print("======================")
# sorted_people = sorted(people, key=lambda x: len(x.matches))

# print("Sorting people based on number of matches")
# for p in sorted_people:
#     print("Person %s has %d matches" % (p.email, len(p.matches)))

# # Creating matched dates
# print("======================")
# print("Sorting people based on number of matches")
# for p in people:
#     for m in p.matches:
#         if len(m.dates) < max_dates and len(p.dates) < max_dates:
#             p.dates.append(m)
#             m.dates.append(p)
#         else:
#             print("Match didn't transform into date: %s and %s" % (p.email, m.email))

# # Printing matched dates
# for p in people:
#     print("======================")
#     if len(p.dates) == 0:
#         print("No dates for %s" % p.email)
#     for m in p.dates:
#         print("It's a date! %s and %s" % (p.email, m.email))

# # Adding extra dates (when possible)
# # print("======================")
# # count = 0
# # for p in people:
# #     for m in people[count+1:]:
# #         if p.extra_dates == "true" and m.extra_dates == "true":
# #             if len(m.dates) < max_dates and len(p.dates) < max_dates:
# #                 print("Adding extra date: %s and %s" % (p.email, m.email))
# #                 p.dates.append(m)
# #                 m.dates.append(p)
# #     count += 1


# # Printing all dates
# all_dates = []
# print("+++++++++++  All dates per person +++++++++++++++")
# for p in people:
#     print("======================")
#     if len(p.dates) == 0:
#         print("No dates for %s" % p.email)
#     for m in p.dates:
#         all_dates.append(Date(p,m))
#         print("%s and %s" % (p.email, m.email))


# print("+++++++++++  All dates +++++++++++++++")
# unique_dates = list(set(all_dates))
# for a in unique_dates:
#     print("%s and %s" % (a.people[0].email, a.people[1].email))

# print("======= Allocation dates ====== ")
# # Calculating rooms
# number_rooms = int(len(people)/2)
# print("Using %d rooms per round" % number_rooms)
# random.shuffle(unique_dates)

# rounds = {}

# rounds_ids = []
# for r in range(1, max_dates+1):
#     if r not in rounds:
#         rounds[r] = {
#             'dates': [],
#             'nonallocated_people': []
#         }
#     rounds_ids.append(r)
# random.shuffle(rounds_ids)

# unique_unmatched_dates = []
# for r in range(1, max_dates+1):
#     busy_people = []
#     to_remove = []
#     id = rounds_ids[r-1]
#     print("Temp round %d, remaining %d dates" % (id, len(unique_dates)))
#     for d in unique_dates:
#         #print("Date %s + %s " % (d.people[0].email, d.people[1].email))
#         if d.people[0] not in busy_people and d.people[1] not in busy_people:
#             print("Allocating %s + %s to %d" % (d.people[0].email, d.people[1].email, id))
#             rounds[id]['dates'].append(d)
#             busy_people.append(d.people[0])
#             busy_people.append(d.people[1])
#             to_remove.append(d)
#         else:
#             print("Skipping %s + %s to %d" % (d.people[0].email, d.people[1].email, id))

#     for d in to_remove:
#         unique_dates.remove(d)

#     unmatched_people = []
#     random.shuffle(people)
#     for p in people:
#         if p not in busy_people:
#             if p.extra_dates == "false":
#                 print("Person %s won't be allocated in round %d due to lack of matches" % (p.email, id) )
#                 rounds[id]['nonallocated_people'].append(p)
#             else:
#                 unmatched_people.append(p)

#     for i in range(0, len(unmatched_people)-1, 2):
#         d = Date(unmatched_people[i], unmatched_people[i+1])

#         if d not in unique_unmatched_dates:
#             rounds[id]['dates'].append(d)
#             unique_unmatched_dates.append(d)
#             busy_people.append(d.people[0])
#             busy_people.append(d.people[1])
#             print("Allocating unmatched date %s + %s to %d" % (d.people[0].email, d.people[1].email, id))

#     if (len(unmatched_people) % 2) != 0:
#         p = unmatched_people[-1]
#         print("Person %s won't be allocated in round %d due to odd number of people" % (p.email, id) )
#         rounds[id]['nonallocated_people'].append(p)


# print("+++++++++++  Rooms +++++++++++++++")
# try:
#     rmtree('out')
# except Exception as e:
#     print(e)
# os.mkdir('out')

# for id, data in rounds.items():
#     print("===> Round %s" % id )
#     with open(os.path.join("out","round_%s.csv" % id), "w") as fp:
#         fp.write("Pre-assign Room Name,Email Address\n")
#         count = 1
#         for d in data['dates']:
#             print("[%10s]\t%s + %s" % (room_names[count], d.people[0].email, d.people[1].email))
#             fp.write("%s,%s\n" % (room_names[count], d.people[0].email))
#             fp.write("%s,%s\n" % (room_names[count], d.people[1].email))
#             count += 1
#     for p in data['nonallocated_people']:
#         print("Non allocated: %s" % p.email)
