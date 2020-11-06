from person import Person,print_people


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
    print("\n ==> Reading CSV input file %s\n" % filename)
    people = {}
    
    with open(filename) as fp:
        matching_fields = _read_header(fp)

        lines = fp.readlines()
        for line in lines:
            fields = line.strip().split(',')
            people[fields[1]] = Person(fields[0],fields[1], fields[2], matching_fields, fields[3:])

    print("\n ** List imported ")
    print_people(people)
    print("\n ==> Import completed for %s\n" % filename)
    return matching_fields, people