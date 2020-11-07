import sys
# import random
# from shutil import rmtree
# import os

from person import Person,print_people
from date import Date,generate_possible_dates, retrieve_dates, initiate_rounds, allocate_dates
from input_file import read_input_file

print(" ** Reticulating splines... ")

# actually allocated dates per round
# dict round number -> date
dates_per_round = None

# =======================
print("\n ==> Reading application arguments \n")
max_dates = int(sys.argv[2])
filename = sys.argv[1]
print("\n ==> Finished reading application arguments \n")
# =======================

# Returns metadata about matching fields and people to be included (dict indexed by email)
matching_fields, people = read_input_file(filename)

# Returns list for all possible dates
possible_dates = generate_possible_dates(matching_fields, people)

# Returns high compatibility matches (dict indexed by email)
hc_possible_dates = retrieve_dates(matching_fields, possible_dates, people, True)

# Returns low compatibility matches (dict indexed by email)
lc_possible_dates = retrieve_dates(matching_fields, possible_dates, people, False)

# Returns a dict round_numer -> List of Dates with 'None' for all empty slots
dates_per_round = initiate_rounds(people, max_dates)

# Allocates dates and adds them to dates_per_round
allocate_dates(dates_per_round, hc_possible_dates, people, True)
allocate_dates(dates_per_round, lc_possible_dates, people, False)


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
