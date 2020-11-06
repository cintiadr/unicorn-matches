class Person:
    def __init__(self, name, email, allow_imperfect_matches, identifies_as, searching_for):
        self.name = name.strip()
        self.email = email.strip()
        self.allow_imperfect_matches = allow_imperfect_matches.strip()

        self.identifies_as = identifies_as.strip().split('|')
        self.searching_for = searching_for.strip().split('|')
        self.matches = []
        self.dates = []

    def matches_with(self, possible_match):
        print("Attempting match: %s and %s" % (self.email, possible_match.email))
        for i in self.identifies_as:
            for j in possible_match.identifies_as:
                if i in possible_match.searching_for and j in self.searching_for:
                    print('Yep')
                    return True
        print('Nope')
        return False

def print_people(people):
    for p in people:
        print(" - %s [%s] (non-perfect matches - %s) " % (p.name, p.email, p.allow_imperfect_matches) )