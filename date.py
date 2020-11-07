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

    # def __eq__(self, other):
    #     return self.people.keys() == other.people.keys()

    # def __hash__(self):
    #     return hash(self.people.keys())


def print_dates(dates):
    for d in dates:
        pair = sorted(d.people.keys(), key=lambda x: x)
        print(" - %s [%d%%] & %s [%d%%]" % (pair[0], d.people[pair[0]], pair[1], d.people[pair[1]]))


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

    print("\n ** List possible high compatibility dates (and preferences matched %)")
    print_dates(hc_dates_list)

    hc_dates = {}
    for d in hc_dates_list:
        for p in d.people.keys():
            if p not in hc_dates:
                hc_dates[p] = []
            hc_dates[p].append(d)

    print("\n ** High compatibility dates per person")
    for p in hc_dates.keys():
        print(" - %s: %d dates" % (p, len(hc_dates[p])))

    print("\n ==> Finished Retrieving high compatibility dates")
    return hc_dates