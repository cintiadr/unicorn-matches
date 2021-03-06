import sys
import argparse
import logging
import os

from person import Person,print_non_allocated_people
from date import Date,generate_possible_dates, retrieve_dates, initiate_rounds, allocate_dates
from files import read_input_file,generate_output_files, generate_output_folder, generate_summary_file

subfolder = generate_output_folder()


parser = argparse.ArgumentParser(description='Creates pairings for speed dating events.')
parser.add_argument('--file', nargs='?', help='CSV file with the attendees', required=True)
parser.add_argument('--min-rounds', nargs='?', default=1, help='Minimum number of dating rounds (default is 1)', type=int)
parser.add_argument('--max-rounds', nargs='?', default=5, help='Maximum number of dating rounds (default is 5)', type=int)
args = parser.parse_args(sys.argv[1:])


logging.info(" ** Reticulating splines... ")

# actually allocated dates per round
# dict round number -> date
dates_per_round = None

# =======================
logging.info("\n ==> Reading application arguments \n")
max_dates = args.max_rounds
min_dates = args.min_rounds
filename = args.file
logging.info(" ** Using arguments: ")
logging.info(args)
logging.info("\n ==> Finished reading application arguments \n")
# =======================

# Returns metadata about matching fields and people to be included (dict indexed by email)
matching_fields, people = read_input_file(filename)

# Returns list for all possible dates
possible_dates = generate_possible_dates(matching_fields, people)

# Returns high compatibility matches (dict indexed by email)
hc_possible_dates, hc_cut = retrieve_dates(matching_fields, possible_dates, people, True)

# Returns low compatibility matches (dict indexed by email)
# and high compatibility cut
lc_possible_dates, _ = retrieve_dates(matching_fields, possible_dates, people, False)

# Returns a dict round_numer -> List of Dates with 'None' for all empty slots
dates_per_round = initiate_rounds(people, hc_possible_dates, min_dates, max_dates)

# Allocates dates and adds them to dates_per_round
dates_to_be_dropped = allocate_dates(dates_per_round, hc_possible_dates, people, True)
allocate_dates(dates_per_round, lc_possible_dates, people, False)

generate_output_files(dates_per_round, subfolder)

generate_summary_file(dates_per_round, dates_to_be_dropped, people, hc_cut, subfolder)

print_non_allocated_people(list(dates_per_round.keys()), people)

logging.info("\n ** Breakout rooms, debug logs and summary created: %s \n" % os.path.join("out", subfolder))




