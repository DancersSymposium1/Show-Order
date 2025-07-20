import random
import csv 
import codecs
from collections import defaultdict
import copy

DANCER_FILE = "new_s25_rosters.csv"
SHOW_ORDER_FILE = "tmp.csv"
SHOW_LENGTH = 40

ALL_PIECES = random.sample(["soulstylz","en pointe","abhinaya","valia","juli","suzy","fsa","arcc","vera","tyler & kina",
                            "jianing & lydia","tricking seniors","kpdc","alex & alisa","alex senior solo","camille","paige","jiya","jillian",
                            "lydia senior solo","street seniors","infra","caroline","karina","helen","valia senior solo","tricking","stanley","infra seniors",
                            "helix seniors","sydney","sonya","nina senior solo","kina senior solo","lily senior solo","tiffany","helix","nina & lily",
                            "eleanor senior solo","alex"],SHOW_LENGTH)

FIXED_ACT1 = ["soulstylz","valia","abhinaya","kpdc","caroline",
              "lily senior solo","stanley","jillian","valia senior solo","camille",
              "","nina senior solo","sydney","infra seniors","alex & alisa",
              "kina senior solo","karina","tiffany","juli","nina & lily"]
FIXED_ACT2 = ["tyler & kina","","","","",
              "","","","","",
              "","","","","",
              "","","helix","eleanor senior solo","alex"]

def write_file(act1,act2):
    with open(SHOW_ORDER_FILE ,"rw") as f:
        f.write("Act 1, Act 2\n")
        for p1,p2 in act1,act2:
            f.write(f"{p1},{p2}\n",p1,p2)

# util function for printing lists (useful for debugging)
def print_list(list):
    for item in list:
        print(item)
    print(" ")

# util function for printing dictionaries (useful for debugging)
def print_dic(dic):
    for key in dic.keys():
        print(key + ": ")
        print_list(dic[key])
    print(" \n ")

# util function to find dancers that overlap between two lists
def check_dancers(list1, list2):
    conflicts = list1 & list2
    return list(conflicts)

class PrepareShow():
    # Class to hold all of the information about dancers, pieces, and show order
    # The main class elements are:
    #       Pieces: a dictionary with pieces as keys and dancer lists as values 
    #               (DS and Outside Orgs)
    #       Dancers: a dictionary with dancers as keys and their pieces in a list as 
    #               values 
    #       Order: a dictionary with "ACT I" and "ACT II" as the keys and the piece 
    #               order of each act in a list as the value
    # The main class functions are:
    #       list_dancer_pieces(self, dancer) : line 130
    #       list_conflicts(self, piece1, piece2): line 144
    #       list_good_pieces(self, piece): line 179
    #       list_bad_pieces(self, piece): line 188
    #       most_conflicting(self): line 197
    #       list_at_least(self, num): line 215
    #       dancer_most_pieces(self): line 229
    #       check_act(self, act): line 247
    #       check_show(self): line 271
    def __init__(self):
        self.known_bad = set()
        self.known_bad.add(("soulstylz","jillian"))
        self.known_bad.add(("soulstylz","alex & alisa"))
        self.known_bad.add(("soulstylz","karina"))
        self.known_bad.add(("alex","suzy"))
        self.known_bad.add(("soulstylz","kina senior solo"))
        self.known_bad.add(("soulstylz","valia senior solo"))
        self.known_bad.add(("soulstylz","alex senior solo"))
        self.known_bad.add(("soulstylz","tricking seniors"))
        self.known_bad.add(("soulstylz","helix seniors"))
        self.known_bad.add(("soulstylz","nina senior solo"))
        self.known_bad.add(("soulstylz","eleanor senior solo"))
        self.known_bad.add(("soulstylz","street seniors"))
        self.known_bad.add(("soulstylz","infra seniors"))
        self.known_bad.add(("soulstylz","lydia senior solo"))
        self.known_bad.add(("soulstylz","lily senior solo"))

        self._import_dancers()
        if '' in self.Pieces:
            del self.Pieces['']     

    def update_order(self,order):
        self.Order = {"ACT I": order[:20], "ACT II": order[20:]}

    def quick_check(self, curr_piece, next_piece):
        return (curr_piece,next_piece) in self.known_bad

    def _import_assigned(self):
        self.Pieces = defaultdict(lambda: [])
        self.Dancers = defaultdict(lambda: [])
        f = codecs.open(DANCER_FILE, 'r', encoding='ascii', errors='ignore')
        reader = csv.reader(f)
        has_piece = False
        has_dancers = False
        dancers = []
        p = ""
        for row in reader:
            if len(row[0])==0 and len(row[1])==0:
                # end of the last piece
                self.Pieces[p] = dancers
                p = "" 
                has_piece = False
                has_dancers = False
                continue
            if has_piece is False:
                # beginning of a new piece
                p = row[0].lower()
                has_piece = True
                dancers = []
            else:
                # dancers for piece
                dancer = row[1].lower().strip()
                if len(dancer) != 0:
                    has_dancers = True
                    dancers.append(dancer)
                    self.Dancers[dancer].append(p)
                else:
                    if has_piece is False:
                        print("WE HAVE AN ERROR: no piece name")
                    if has_dancers is False:
                        print("WE HAVE AN ERROR: no dancers for piece")
                    self.Pieces[p] = dancers
                    has_piece = False
                    has_dancers = False

    def _import_dancers(self):
        '''Format: dancers, org'''
        self.Pieces = defaultdict(lambda: [])
        self.Dancers = defaultdict(lambda: [])
        f = codecs.open(DANCER_FILE, 'r', encoding='ascii', errors='ignore')
        reader = csv.reader(f)
        dancers = []
        p = ""
        for row in reader:
            # This is kinda a hotfix for formatting breaking - Christoph
            p = row[-1].lower().strip(' "')
            dancers = [d.lower().strip(' "') for d in row[:-1]]
            self.Pieces[p] = set(dancers)
            for dancer in dancers:
                self.Dancers[dancer].append(p)
        # for dancer in self.Dancers:
        #     print(dancer,self.Dancers[dancer],'\n\n')

    def _import_order(self):
        f = codecs.open(SHOW_ORDER_FILE, 'r', encoding='ascii', errors='ignore')
        reader = csv.reader(f)
        act1 = []
        act2 = []
        first = True
        for row in reader:
            if first is False:
                act1.append(row[0].lower())
                act2.append(row[1].lower())
            else:
                first = False
        self.Order = {"ACT I": act1, "ACT II": act2}

    def list_dancer_pieces(self, dancer):
        dancer = dancer.lower()
        pieces = self.Dancers[dancer]
        if dancer != []:
            print("Here are the pieces that '" + dancer + "' is in:")
            print_list(pieces)
            return pieces
        else:
            print("WE HAVE AN ERROR: Dancer not found\n")
            return []

    # list_conflicts: a class function to find a list of all dancers that conflict between two pieces
    # INPUT: two pieces (both strings)
    # OUTPUT: a list of dancers in both pieces (string list)
    def list_conflicts(self, piece1, piece2):
        piece1 = piece1.lower()
        piece2 = piece2.lower()
        conflicts = check_dancers(self.Pieces[piece1], self.Pieces[piece2])
        print("Here are all of the dancers that have a conflict with '" + piece1 + "' and '" + piece2 + "':")
        print_list(conflicts)
        return conflicts

    # helper function to find all pieces that don't conflict with a given piece
    def _find_good_pieces(self, piece):
        piece = piece.lower()
        piece_list = self.Pieces.keys()
        good_pieces = []
        for item in piece_list:
            if item != piece:
                conflicts = check_dancers(self.Pieces[piece], self.Pieces[item])
                if len(conflicts) == 0:
                    good_pieces.append(item)
        return good_pieces

    # helper function to find all pieces that conflict with a given piece
    def _find_bad_pieces(self, piece):
        piece = piece.lower()
        piece_list = self.Pieces.keys()
        bad_pieces = []
        for item in piece_list:
            if item != piece:
                conflicts = check_dancers(self.Pieces[piece], self.Pieces[item])
                if len(conflicts) != 0:
                    bad_pieces.append(item)
        return bad_pieces

    # list_good_pieces: a class function to list all pieces that don't conflict with a given piece
    # INPUT: a piece (string)
    # OUTPUT: a list of pieces without a conflict with this piece (string list)
    def list_good_pieces(self, piece):
        good_pieces = self._find_good_pieces(piece)
        print("Here are all of the pieces that don't have a conflict with '" + piece + "':")
        print_list(good_pieces)
        return good_pieces

    # list_bad_pieces: a class function to list all pieces that conflict with a given piece
    # INPUT: a piece (string)
    # OUTPUT: a list of pieces with a conflict with this piece (string list)
    def list_bad_pieces(self, piece):
        bad_pieces = self._find_bad_pieces(piece)
        print("Here are all of the pieces that have a conflict with '" + piece + "':")
        print_list(bad_pieces)
        return bad_pieces

    # most_conflicting: a class function to find the piece(s) with the most conflicts
    # INPUT: none
    # OUTPUT: a list of pieces with most conflicts with other pieces (string list)
    def most_conflicting(self):
        pieces = []
        max_conflicts = 0
        for item in self.Pieces.keys():
            conflicts = len(self._find_bad_pieces(item))
            if conflicts > max_conflicts:
                pieces = []
                pieces.append(item)
                max_conflicts = conflicts
            elif conflicts == max_conflicts:
                pieces.append(item)
        print("The pieces with the most conflicts will conflict with " + str(max_conflicts) + " other pieces. Here are the pieces with this number of conflicts:")
        print_list(pieces)
        return pieces

    # list_at_least: a class function to list all dancers in at least num pieces
    # INPUT: number of pieces to look for (int)
    # OUTPUT: a list of dancers that are in that many pieces or more (string list)
    def list_at_least(self, num):
        dlist = []
        print("These are all of the dancers in at least " + str(num) + " pieces:")
        for d in self.Dancers.keys():
            pieces = self.Dancers[d.lower()]
            if len(pieces) >= num:
                dlist.append(d)
                print("'" + d + "' (" + str(len(pieces)) + ")")
        print("There are " + str(len(dlist)) + " such dancers.")
        return dlist

    def dancer_most_pieces(self):
            dlist = []
            max_pieces = 0
            for item in self.Dancers.keys():
                pieces = len(self.Dancers[item.lower()])
                if pieces > max_pieces:
                    dlist = []
                    dlist.append(item)
                    max_pieces = pieces
                elif pieces == max_pieces:
                    dlist.append(item)
            print("The dancers with the most pieces have " + str(max_pieces) + " other pieces. Here are the dancers with this number of pieces: ")
            print_list(dlist)
            return dlist
    

    def check_act(self,act):
        act_safe = True
        for index in range(len(act)-1):
            current_piece = act[index]
            next_piece = act[index+1]
            
            if self.quick_check(current_piece,next_piece):
                return False


            if len(self.Pieces[next_piece])>0:
                current_list = self.Pieces[current_piece]
                next_list = self.Pieces[next_piece]

                # IMPORTANT: comment out this entire if statement if you want to allow senior solos as quick changes
                if "senior solo" in next_piece and (index<len(act)-2):
                    next_next_piece = act[index+2]
                    next_next_list = self.Pieces[next_next_piece]
                    next_list = next_next_list|next_list
                    next_piece = next_piece + "' and '" + next_next_piece
                conflicts = check_dancers(current_list, next_list)
                if len(conflicts) != 0:
                    act_safe = False
                    self.known_bad.add((current_piece,next_piece))
                    return False
                    # print("CONFLICT: There are conflicting dancers between '" + current_piece + "' and '" + next_piece + "'. Here are the conflicts:")
                    # print_list(conflicts)
            else:
                print(f'piece {next_piece} has no dancers listed')
        return act_safe

    def identify_quickchanges_act(self,act):
        num_quickchanges = 0
        for index in range(len(act)-2):
            current_piece = act[index]
            nn_piece = act[index+2]
            if len(nn_piece)>0:
                current_list = self.Pieces[current_piece]
                nn_list = self.Pieces[nn_piece]
                conflicts = check_dancers(current_list, nn_list)
                if len(conflicts) != 0:
                    num_quickchanges+=len(conflicts)
                    # res_string = f"Quick Change between '{current_piece}' and '{nn_piece}' for these dancers:\n"
                    # res_conflicts = conflicts
        return num_quickchanges
    

    def identify_quickchanges(self):
        act1 = self.Order["ACT I"]
        act2 = self.Order["ACT II"]
        # print("ACT I:")
        qc_act1 = self.identify_quickchanges_act(act1)
        # print("ACT II:")
        qc_act2 = self.identify_quickchanges_act(act2)
        # print("\n\n")
        return qc_act1 + qc_act2

    def check_show(self):
        act1 = self.Order["ACT I"]
        act2 = self.Order["ACT II"]
        # print("ACT 1: ",act1)
        act1_safe = self.check_act(act1)
        # act1_safe = True
        act2_safe = self.check_act(act2)
        # print("SUMMARY:")
        # if act1_safe:
        #     print("ACT I has no conflicts")
        # else:
        #     print("ACT I has conflicts")
        # if act2_safe:
        #     print("ACT II has no conflicts")
        # else:
        #     print("ACT II has conflicts")
        if act1_safe and act2_safe:
            print("GOOD SHOW ORDER!")
            return True
        else: return False

def generate_orders(used, order, fixed):
    iterations = 0
    # tried = [order]
    Show = PrepareShow()
    Show.update_order(order)
    # MAX_ITER = 5000000
    no_conflicts = False
    quick_thresh = 2
    quick_changes = Show.identify_quickchanges()
    while (no_conflicts==False or quick_changes > quick_thresh):
    # (iterations < MAX_ITER):

        # if(iterations==(MAX_ITER)//16):
        #     print("1/16 completed")
        # if(iterations==(MAX_ITER)//8):
        #     print("0.125 completed")
        # if(iterations==(MAX_ITER)//4):
        #     print("0.25 completed")
        # if(iterations==(MAX_ITER)//2):
        #     print("0.5 completed")
        # if(iterations==3*(MAX_ITER)//4):
        #     print("0.75 completed")
        all_pieces = list(Show.Pieces.keys())
        remaining = random.sample(subtract_lists(all_pieces,used),len(all_pieces)-len(used))
        for piece in range(40):
            if order[piece] not in fixed:
                order[piece] = remaining[0]
                remaining = remaining[1:]

        Show.update_order(order)
        if(Show.check_show()==True):
            quick_changes = Show.identify_quickchanges()
            if(quick_changes <= quick_thresh):
                print(Show.Order)
                with open("tmp.csv","w") as f:
                    f.writelines(f"Act 1, Act 2\n")
                    for i in range(20):
                        p1 = Show.Order["ACT I"][i]
                        p2 = Show.Order["ACT II"][i]
                        f.write(f"{p1},{p2}\n")
                print("number of quick changes is: ",quick_changes)

                print(iterations)
                return "GOOD"
        iterations+=1
    return "NOT POSSIBLE"

def subtract_lists(l1, l2):
    result = []
    for i in range(len(l1)):
        if l1[i] not in l2:
            result.append(l1[i])
    return result

    
def main():
    used = []

    for fa1 in FIXED_ACT1:
        if fa1 != "":
            used.append(fa1)
    for fa2 in FIXED_ACT2:
        if fa2 != "":
            used.append(fa2)

    pieces = random.sample(subtract_lists(ALL_PIECES,used),len(ALL_PIECES)-len(used))
    fixed = FIXED_ACT1+FIXED_ACT2

    initial_seed = copy.deepcopy(fixed)

    for i in range(40):
        if initial_seed[i]=="":
            initial_seed[i] = pieces[0]
            pieces = pieces[1:]

    # print(initial_seed)
    print(generate_orders(used,initial_seed,fixed))

main()