from distutils.util import strtobool

class Person:
    def __init__(self, name, email, allow_imperfect_matches, matching_fields_metadata, matching_fields_values):
        self.name = name.strip()
        self.email = email.strip()
        self.allow_imperfect_matches = bool(strtobool(allow_imperfect_matches.strip()))

        self.i_am = {}
        self.searching_for = {}

        for index, field in enumerate(matching_fields_values):
            pp = field.strip().split('@')
            pi = matching_fields_metadata[index]['Name']
            self.i_am[pi] = pp[0].split('|')
            self.searching_for[pi] = pp[1].split('|')


    def short_printable(self):
        return self.email

    def printable(self): 
       return ("%s [%s] [Imperfect Matches - %r] \n\t \-> I am: %s \n\t \-> Looking for: %s]\n" % (self.email, self.name, self.allow_imperfect_matches, self.i_am, self.searching_for) )

    # calcules compability of other person based on my looking for
    def calculate_compatibility_with(self, matching_fields_metadata, person):
        compability = 0
        for f in matching_fields_metadata.values():
            field_name = f['Name']
            percentage = f['Percentage']
            for g in self.searching_for[field_name]:
                if g in person.i_am[field_name]:
                    compability += percentage
                    break
        
        if not self.allow_imperfect_matches and compability < 100:
            return -1
        else:
            return compability
        

def print_people(people):
    for p in people.values():
        print(" - %s" % p.printable() )