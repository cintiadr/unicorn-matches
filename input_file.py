from person import Person

def read_input_file(filename):
    # Reading CSV file
    people = []
    with open(filename) as fp:
        Lines = fp.readlines()
        for line in Lines:
            fields = line.strip().split(',')
            people.append(Person(fields[0],fields[1], fields[2], fields[3], fields[4]))
    return people