from person import Person

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
    return matching_fields


def read_input_file(filename):
    print("\n ==> Reading CSV input file %s\n" % filename)
    people = []
    
    with open(filename) as fp:
        matching_fields = _read_header(fp)

        lines = fp.readlines()
        for line in lines:
            fields = line.strip().split(',')
            people.append(Person(fields[0],fields[1], fields[2], matching_fields, fields[3:]))
    return people