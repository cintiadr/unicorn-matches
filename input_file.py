from person import Person

def read_input_file(filename):
    print("\n ==> Reading CSV input file %s\n" % filename)
    people = []
    with open(filename) as fp:
        first_line = fp.readline()
        lines = fp.readlines()
        for line in lines:
            fields = line.strip().split(',')
            people.append(Person(fields[0],fields[1], fields[2], fields[3], fields[4]))
    return people