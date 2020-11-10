from person import Person,print_people,find_non_allocated_people_in_round
from date import find_dates_per_person
from shutil import rmtree
import os
from config import room_names
import datetime
import logging


def _read_header(fp):
    matching_fields = {}
    first_line = fp.readline()
    header_columns = first_line.strip().split(',')[3:]

    for index, f in enumerate(header_columns):
        field_info = f.strip().split('|')
        matching_fields[index] = {
            'Name': field_info[0].strip(),
            'Percentage': int(field_info[1].strip().replace('%', ''))
        }

    logging.info(" ** Matching fields detected: %s" % matching_fields)

    if sum([ f['Percentage'] for f in matching_fields.values() ]) != 100:
        raise Exception("Percentage of matching fields should be exactly 100%, please change your CSV headers")

    return matching_fields


def read_input_file(filename):
    logging.info("\n ==> Importing CSV input file %s\n" % filename)
    people = {}
    
    with open(filename) as fp:
        matching_fields = _read_header(fp)

        lines = fp.readlines()
        for line in lines:
            fields = line.strip().split(',')
            people[fields[1].strip()] = Person(fields[0],fields[1], fields[2], matching_fields, fields[3:])

    logging.info("\n ** List imported ")
    print_people(people)
    logging.info("\n ==> Import completed for %s\n" % filename)
    return matching_fields, people


def generate_output_folder():
    print("\n ==> Generating output folder\n")
    if not os.path.exists("out"): 
        os.mkdir('out')
    
    current_time_string = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    os.mkdir(os.path.join('out', current_time_string))

    print("\n ==> Finished generating output folder\n")

    logging.basicConfig(
        level=logging.DEBUG,
        format="%(message)s",
        handlers=[
            logging.FileHandler(os.path.join("out", current_time_string, "debug.logs")),
            logging.StreamHandler()
        ]
    )

    return current_time_string

def generate_output_files(dates_per_round, subfolder):
    # dates_per_round is a dict round_numer -> List of Dates with 'None' for all empty slots
    logging.info("\n ==> Generating output files\n")

    os.mkdir(os.path.join('out', subfolder, "zoom-breakout-rooms"))

    for r, dates in dates_per_round.items():
        logging.info(" ** Round %s (%d dates)" % (r, len(dates)) )
        with open(os.path.join("out", subfolder, "zoom-breakout-rooms", "round_%s.csv" % r), "w") as fp:
            fp.write("Pre-assign Room Name,Email Address\n")
            count = 1
            for d in dates:
                if d is not None:
                    logging.info(" \-> [%10s] {%s}" % (room_names[count], d.printable()))
                    pair = d.get_emails()
                    fp.write("%s,%s\n" % (room_names[count], pair[0]))
                    fp.write("%s,%s\n" % (room_names[count], pair[1]))
                    count += 1
                else:  
                     logging.info(" [WARN] Non allocated slot in round %d" % r)
                


    logging.info("\n ==> Finished generating output files\n")

def generate_summary_file(dates_per_round, dates_to_be_dropped, people, hc_cut, subfolder):
    logging.info("\n ==> Generating summary file\n")
    with open(os.path.join("out", subfolder, "summary.txt"), "w") as fp:
        fp.write("Overview: \n" )
        fp.write(" - Compatibility >= %d is considered high compatibility dates \n" % hc_cut )
        fp.write(" - %d rounds\n" % len(dates_per_round.items()) )
        fp.write(" - %d dates per round \n" % len(dates_per_round[1]) )
        fp.write(" - %d high compatibility dates dropped \n" % len(dates_to_be_dropped) )


        total_non_allocated_people = 0
        for r in dates_per_round.keys():
            non_allocated_people = [p.email for p in people.values() if r not in p.allocated_rounds]
            total_non_allocated_people += len(non_allocated_people)

        fp.write(" - %d unpaired people occurences \n" % total_non_allocated_people )


        fp.write("\n\nRounds information: \n" )

        for r in dates_per_round.keys():
            dates = dates_per_round[r]
            fp.write("  - Round %d: \n" % r)

            hc_dates = [d for d in dates if d is not None and d.high_compatibility]
            fp.write("    - %d High compatibility dates \n" % len(hc_dates))

            lc_dates = [d for d in dates if d is not None and not d.high_compatibility]
            fp.write("    - %d Low compatibility dates \n" % len(lc_dates))

            non_allocated_people = find_non_allocated_people_in_round(r,people)
            fp.write("    - %d unpaired people \n" % len(non_allocated_people))
            for p in non_allocated_people:
                fp.write("      - %s \n" % p)


        fp.write("\nPeople information: \n" )
        for email, p in people.items():
            fp.write("  -  %s: \n" % email)
            dates_per_person = find_dates_per_person(dates_per_round, p)

            hc_dates = [d for d in dates_per_person if d is not None and d.high_compatibility]
            fp.write("    - %d High compatibility dates \n" % len(hc_dates))

            lc_dates = [d for d in dates_per_person if d is not None and not d.high_compatibility]
            fp.write("    - %d Low compatibility dates \n" % len(lc_dates))

            non_allocated_rounds = p.find_non_allocated_rounds(dates_per_round.keys())
            fp.write("    - %d unpaired rounds \n" % len(non_allocated_rounds))
            for r in non_allocated_rounds:
                fp.write("      - Round %s \n" % r)

        logging.info("\n ==> Finished summary file\n")


    
