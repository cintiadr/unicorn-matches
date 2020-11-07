from config import room_names

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

    def __eq__(self, other):
        return self.people.keys() == other.people.keys()

    def __hash__(self):
        return hash(self.people.keys())


def print_dates(dates, prefix = " - "):
    for d in dates:
        pair = sorted(d.people.keys(), key=lambda x: x)
        print("%s%s [%d%%] & %s [%d%%]" % (prefix, pair[0], d.people[pair[0]], pair[1], d.people[pair[1]]))


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
    

def retrieve_hc_dates(matching_fields, possible_dates):
    hc_dates_list = {}
    print("\n ==> Retrieving possible high compatibility dates")
    hc_cut = max([ f['Percentage'] for f in matching_fields.values() ])
    print(" ** Preferences matched >= %d%% for both sides is consided high compatibility" % hc_cut)
    hc_dates_list = [ d for d in possible_dates if d.combined_compatibility(hc_cut)]

    # print("\n ** List possible high compatibility dates (and preferences matched %)")
    # print_dates(hc_dates_list)

    hc_dates = {}
    for d in hc_dates_list:
        for p in d.people.keys():
            if p not in hc_dates:
                hc_dates[p] = []
            hc_dates[p].append(d)

    # Sorting by compatibility
    for p in hc_dates.keys():    
        hc_dates[p] = sorted(hc_dates[p], key=lambda x: x.people[p])


    print("\n ** Ordered high compatibility dates per person")
    for p in hc_dates.keys():
        print(" - %s (%d dates)" % (p, len(hc_dates[p])))
        print_dates(hc_dates[p], "\t \-> ")

    print("\n ==> Finished Retrieving high compatibility dates")
    return hc_dates

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

def allocate_dates(dates_per_round, hc_possible_dates, people):
    return dates_per_round
