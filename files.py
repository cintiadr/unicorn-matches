from person import Person,print_people
from shutil import rmtree
import os
from config import room_names


def _read_header(fp):
    matching_fields = {}
    first_line = fp.readline()
    header_columns = first_line.strip().split(',')[3:]

    for index, f in enumerate(header_columns):
        field_info = f.strip().split('|')
        matching_fields[index] = {
            'Name': field_info[0],
            'Percentage': int(field_info[1].replace('%', ''))
        }

    print(" ** Matching fields detected: %s" % matching_fields)

    if sum([ f['Percentage'] for f in matching_fields.values() ]) != 100:
        raise Exception("Percentage of matching fields should be exactly 100%, please change your CSV headers")

    return matching_fields


def read_input_file(filename):
    print("\n ==> Importing CSV input file %s\n" % filename)
    people = {}
    
    with open(filename) as fp:
        matching_fields = _read_header(fp)

        lines = fp.readlines()
        for line in lines:
            fields = line.strip().split(',')
            people[fields[1].strip()] = Person(fields[0],fields[1], fields[2], matching_fields, fields[3:])

    print("\n ** List imported ")
    print_people(people)
    print("\n ==> Import completed for %s\n" % filename)
    return matching_fields, people

def generate_output_files(dates_per_round):
    # dates_per_round is a dict round_numer -> List of Dates with 'None' for all empty slots
    print("\n ==> Generating output files\n")
    try:
        rmtree('out')
    except Exception as e:
        print(e)
    os.mkdir('out')

    for r, dates in dates_per_round.items():
        print(" ** Round %s (%d dates)" % (r, len(dates)) )
        with open(os.path.join("out","round_%s.csv" % r), "w") as fp:
            fp.write("Pre-assign Room Name,Email Address\n")
            count = 1
            for d in dates:
                if d is not None:
                    print(" \-> [%10s] {%s}" % (room_names[count], d.printable()))
                    pair = d.get_emails()
                    fp.write("%s,%s\n" % (room_names[count], pair[0]))
                    fp.write("%s,%s\n" % (room_names[count], pair[1]))
                    count += 1
                else:  
                     print(" [WARN] Non allocated slot in round %d" % r)
                


    print("\n ==> Finished generating output files\n")