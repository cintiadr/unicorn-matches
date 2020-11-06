class Date:
    def __init__(self, person1, person2):
        self.people = sorted([person1, person2], key=lambda x: x.email)

    def __eq__(self, other):
        return self.people[0].email == other.people[0].email and self.people[1].email == other.people[1].email

    def __hash__(self):
        return hash((self.people[0].email, self.people[1].email))