import random

class Date:
    def __init__(self, person1, person2, compatibility_1, compatibility_2):
        self.people = {
            person1.email: compatibility_1,
            person2.email: compatibility_2,
        }
    
    def combined_compatibility(self, cut_compatibility):
        for c in self.people.values():
            if c < cut_compatibility:
                return False
        return True
    
    def printable(self):
        pair = sorted(self.people.keys(), key=lambda x: x)
        return "(%s) [%d%%] & (%s) [%d%%]" % (pair[0], self.people[pair[0]], pair[1], self.people[pair[1]])
    
    def get_emails(self):
        pair = sorted(self.people.keys(), key=lambda x: x)
        return pair
    
    def __repr__(self):
        pair = sorted(self.people.keys(), key=lambda x: x)
        return "(%s)&(%s)" % (pair[0],pair[1])

    def __eq__(self, other):
        if other is None:
            return False
        return self.people.keys() == other.people.keys()

    def __hash__(self):
        return hash(self.people.keys())


def print_dates(dates, prefix = " - "):
    for d in dates:
        print("%s%s" % (prefix, d.printable()))


def generate_possible_dates(matching_fields, people):  
    print("\n ==> Calculating possible dates")
    possible_dates = []
    all_people = list(people.values())
    for index, p in enumerate(all_people):
        for pm in all_people[index+1:]:
            compatibility_1 = p.calculate_compatibility_with(matching_fields, pm)
            compatibility_2 = pm.calculate_compatibility_with(matching_fields, p)

            # negative number means that person config doesn't allow an imperfect match
            if compatibility_1 >= 0 and compatibility_2 >= 0:
                possible_dates.append(Date(p, pm, compatibility_1, compatibility_2))
            else:
                print("  [WARN] Incompatible date: %s [%d%%] & %s [%d%%]" % (p.short_printable(), compatibility_1, pm.short_printable(), compatibility_2))
            
    
    print("\n ** List possible dates (and preferences matched %)")
    print_dates(possible_dates)
    print("\n ==> Finished calculating possible dates\n")
    return possible_dates
    

def retrieve_dates(matching_fields, all_possible_dates, people, high_compatibility = True):
    dates_list = {}

    if high_compatibility:
        label = "high"
        operation = ">="
    else:
        label = "low"
        operation = "<"    

    print("\n ==> Retrieving possible %s compatibility dates" % label)
    hc_cut = max([ f['Percentage'] for f in matching_fields.values() ])
    print(" ** Preferences matched %s %d%% for both sides is consided %s compatibility" % (operation, hc_cut, label))
    
    if high_compatibility:
        dates_list = [ d for d in all_possible_dates if d.combined_compatibility(hc_cut)]
    else:
        dates_list = [ d for d in all_possible_dates if not d.combined_compatibility(hc_cut)]

    # print("\n ** List possible high compatibility dates (and preferences matched %)")
    # print_dates(dates_list)

    selected_dates = {}
    for p in people.keys():
        selected_dates[p] = []

    for d in dates_list:
        for p in d.people.keys():
            selected_dates[p].append(d)

    # Sorting by compatibility
    # But ramdomise first to mix same compatibility
    for p in selected_dates.keys():   
        random.shuffle(selected_dates[p]) 
        selected_dates[p] = sorted(selected_dates[p], key=lambda x: x.people[p] * (-1))


    print("\n ** Ordered %s compatibility dates per person" % label)
    for p in selected_dates.keys():
        print(" - (%s) [%d dates]" % (p, len(selected_dates[p])))
        print_dates(selected_dates[p], "\t \-> ")

    print("\n ==> Finished Retrieving %s compatibility dates" % label)
    return selected_dates

def initiate_rounds(people, rounds):
    print("\n ==> Creating empty rounds")
    dates_per_round = {}
    number_rooms = int(len(people)/2)
    print("\n ** Initialising %d rounds of dates (configured by argument)" % (rounds))
    print(" ** Allowing %d dates per round (for %d people)" % (number_rooms, len(people)))
    for i in range(1,rounds+1):   
        dates_per_round[i] = []
        for j in range(0,number_rooms):
            dates_per_round[i].append(None)
    #print(dates_per_round)
    print("\n ==> Finished creating empty rounds")
    return dates_per_round

def allocate_dates(dates_per_round, possible_dates, people, high_compatibility = True):

    if high_compatibility:
        label = "high compatibility"
    else:
        label = "low compatibility"

    print("\n ==> Allocating %s dates\n" % label)
    # possible_dates is dict email -> [Sorted Dates]
    # people is dict email -> Person

    # sorting people with less dates, but randomise first
    # so people with same amount of dates won't necessarily be on the same order
    all_emails = list(people.keys())
    random.shuffle(all_emails)
    sorted_people = sorted(all_emails, key=lambda x: len(possible_dates[x]))
    if high_compatibility:
        print(" ** Attempting to allocate %s dates from people in this order: " % label) 
    print(sorted_people)

    # This will be the rounds we'll attempt to allocate the dates
    rounds_to_attempt = list(dates_per_round.keys())
    dates_to_be_dropped = []
    
    print("\n ** Allocating %s dates: " % label)
    for p in sorted_people:
        for d in possible_dates[p]:
            # attempting to find a suitable round for this date
            random.shuffle(rounds_to_attempt)
            date_created = False
            for r in rounds_to_attempt:
                if None not in dates_per_round[r]:
                    print(" \-> Round %d is full, removing it from available pool" % r)
                    rounds_to_attempt.remove(r)
                else:
                    # finding our if either people are busy already
                    people_in_date = list(d.people.keys())
                    person1 = people[people_in_date[0]]
                    person2 = people[people_in_date[1]]
                    if r not in person1.allocated_rounds and r not in person2.allocated_rounds:
                        date_created = True

                        # Find an available spot in round to add date
                        none_index = dates_per_round[r].index(None)
                        dates_per_round[r][none_index] = d

                        # Mark those people as busy
                        person1.allocated_rounds.append(r)
                        person2.allocated_rounds.append(r)

                        # delete date from other person's list
                        people_in_date.remove(p)
                        possible_dates[people_in_date[0]].remove(d)

                        print(" \-> Date {%s} allocated to round %d" % (d.printable(), r))
                        break
            if not date_created:
                if high_compatibility:
                    print("  [WARN] Date {%s} couldn't be allocated to any round" % (d.printable())) 
                dates_to_be_dropped.append(d)


    print("\n **  All allocated dates so far: ")
    for r in dates_per_round:
        print(" \-> Round %d" % r)
        for d in dates_per_round[r]:
            if d:
                print(" \----> %s" % d.printable())
            else:
                print(" \----> Empty")
    
    if high_compatibility:
        if len(dates_to_be_dropped) != 0:
            print("\n **  Possible %s dates that won't be allocated due to no rounds available: " % label)
            for d in dates_to_be_dropped:
                print(" \----> %s" % d.printable())
        else: 
            print("\n **  No %s dates dropped so far." % label)

    print("\n ==> Finished allocating %s dates" % label)
    return dates_per_round
