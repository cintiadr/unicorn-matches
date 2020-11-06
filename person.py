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


    #     self.identifies_as = identifies_as.strip().split('|')
    #     self.searching_for = searching_for.strip().split('|')
    #     self.matches = []
    #     self.dates = []

    # def matches_with(self, possible_match):
    #     print("Attempting match: %s and %s" % (self.email, possible_match.email))
    #     for i in self.identifies_as:
    #         for j in possible_match.identifies_as:
    #             if i in possible_match.searching_for and j in self.searching_for:
    #                 print('Yep')
    #                 return True
    #     print('Nope')
    #     return False

def print_people(people):
    for p in people:
        print(" - %s [%s] [Imperfect Matches - %r] \n\t |-> I am: %s \n\t |-> Looking for: %s]\n" 
            % (p.name, p.email, p.allow_imperfect_matches, p.i_am, p.searching_for) )