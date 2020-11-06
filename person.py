class Person:
    def __init__(self, name, email, identifies_as, searching_for, extra_dates):
        self.name = name.strip()
        self.email = email.strip()
        self.identifies_as = identifies_as.strip().split('|')
        self.searching_for = searching_for.strip().split('|')
        self.extra_dates = extra_dates.strip()
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