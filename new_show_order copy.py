# SHOW ORDER 3.5
# Author: Sophia Holland
# Date: November 2024
# Last Updated: November 2024
import csv 
import codecs
from collections import defaultdict
import random

DANCER_FILE = 'new_s25_rosters.csv'
SHOW_ORDER_FILE = 'tmp.csv'

SHOW_LENGTH = 30

ALL_PIECES = random.sample(["soulstylz","en pointe","abhinaya","valia","juli","suzy","fsa","arcc","vera","tyler & kina",
                            "jianing & lydia","tricking seniors","kpdc","alex & alisa","alex senior solo","camille","paige","jiya","jillian",
                            "lydia senior solo","street seniors","infra","caroline","karina","helen","valia senior solo","tricking","stanley","infra seniors",
                            "helix seniors","sydney","sonya","nina senior solo","kina senior solo","lily senior solo","tiffany","helix","nina & lily",
                            "eleanor senior solo","alex"],SHOW_LENGTH)

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
    conflicts = []
    for dancer in list1:
        if dancer in list2:
            conflicts.append(dancer)
            # print(conflicts)
    return conflicts

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
        # helper function for creating a dictionary of dancers using DANCER_FILE
        self._import_dancers()
        # user function for creating a dictionary of show order using SHOW_ORDER_FILE
        self._import_order()
        if '' in self.Pieces:
            del self.Pieces['']     

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
            self.Pieces[p] = dancers
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

    
    # def get_overlaps(self):
    #     with open("tmp.csv","w") as f:
    #         for i in range(40):
    #             for j in range(i,40):
    #                 if i!=j:
    #                     roster1 = set(self.Pieces[ALL_PIECES[i]])
    #                     roster2 = set(self.Pieces[ALL_PIECES[j]])
    #                     f.write(f"{ALL_PIECES[i]},{ALL_PIECES[j]}: {len(roster1 & roster2)} overlaps: {roster1&roster2}\n")


    # def generate_order(self):
    #     all_pieces = list(self.Pieces.keys())
    #     random.shuffle(all_pieces)
    #     print("all pieces: ",all_pieces)

    #     act1, act2 = [], []
    #     used_pieces = set()
        
    #     for piece in all_pieces:
    #         if piece in used_pieces:
    #             continue
    #         if not act1 or not self._find_bad_pieces(act1[-1]):
    #             act1.append(piece)
    #         elif not act2 or not self._find_bad_pieces(act2[-1]):
    #             act2.append(piece)
    #         used_pieces.add(piece)

    #     self.Order = {"ACT I": act1, "ACT II": act2}
    #     print("Proposed order: ",self.Order)


    # def generate_order(self, fixed_pieces=None):
    #     """
    #     Generates a randomized show order while respecting fixed positions.
        
    #     :param fixed_pieces: Dict mapping pieces to (act, position) e.g. {"finale": ("ACT II", -1)}
    #     """
    #     all_pieces = list(self.Pieces.keys())
    #     random.shuffle(all_pieces)

    #     # Initialize acts with fixed piece slots
    #     act1 = [None] * (len(all_pieces)//2+(len(all_pieces)%2))
    #     act2 = [None] * (len(all_pieces)//2)

    #     used_pieces = set()

    #     # Place fixed pieces
    #     if fixed_pieces:
    #         for piece, (act, pos) in fixed_pieces.items():
    #             # if piece in self.Pieces:
    #             if act == "ACT I":
    #                 act1[pos] = piece
    #                 print("ACT ! SPECIAL : ",act1, pos)
    #             elif act == "ACT II":
    #                 act2[pos] = piece
    #             used_pieces.add(piece)
    #     # print("act 1: ",act1)

    #     # Fill remaining slots, ensuring no conflicts
    #     def assign_pieces(act_list):
    #         for i in range(len(act_list)):
    #             if act_list[i] is None:  # Fill only empty slots
    #                 for piece in all_pieces:
    #                     if piece not in used_pieces:
    #                             act_list[i] = piece
    #                             used_pieces.add(piece)
    #                             break

    #     assign_pieces(act1)
    #     assign_pieces(act2)

    #     # Remove None values (in case of empty slots)
    #     self.Order = {"ACT I": [p for p in act1 if p], "ACT II": [p for p in act2 if p]}

    # list_dancer_pieces: a class function to list the number of pieces a dancer is in
    # INPUT: a dancer (string)
    # OUTPUT: a list of pieces the dancer is in (string list)
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

    # dancer_most_pieces: a class function to list the dancer(s) in the most pieces
    # INPUT: none
    # OUTPUT: a list of dancers that are in the most pieces (string list)
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

    # check_act: a class function to check the show order for an act
    # INPUT: a list of the pieces in that act, in order (string list)
    # OUTPUT: a boolean for whether or not that act contains conflicts
    def check_act(self, act):
        act_safe = True
        for index in range(len(act)-1):
            current_piece = act[index]
            next_piece = act[index+1]
            if len(self.Pieces[next_piece])>0:
                current_list = self.Pieces[current_piece]
                next_list = self.Pieces[next_piece]

                # IMPORTANT: comment out this entire if statement if you want to allow senior solos as quick changes
                if "senior solo" in next_piece and (index<len(act)-2):
                    next_next_piece = act[index+2]
                    next_next_list = self.Pieces[next_next_piece]
                    next_list = next_next_list+next_list
                    next_piece = next_piece + "' and '" + next_next_piece
                conflicts = check_dancers(current_list, next_list)
                if len(conflicts) != 0:
                    act_safe = False
                    print("CONFLICT: There are conflicting dancers between '" + current_piece + "' and '" + next_piece + "'. Here are the conflicts:")
                    print_list(conflicts)
            else:
                print(f'piece {next_piece} has no dancers listed')
        return act_safe

    # identify_quickchanges_act: a class function to parse completed act for quickchanges
    # INPUT: a list of the pieces in that act, in order (string list)
    # OUTPUT: none. Prints all quickchanges if any
    def identify_quickchanges_act(self, act):
        act_safe = True
        for index in range(len(act)-2):
            current_piece = act[index]
            nn_piece = act[index+2]
            if len(nn_piece)>0:
                current_list = self.Pieces[current_piece]
                nn_list = self.Pieces[nn_piece]
                # IMPORTANT: comment out this entire if statement if you want to allow senior solos as quick changes
                conflicts = check_dancers(current_list, nn_list)
                if len(conflicts) != 0:
                    print("Quick Change between '" + current_piece + "' and '" + nn_piece + "' for these dancers:")
                    print_list(conflicts)
        return act_safe
    
    # identify_quickchanges: a class function to identify any quick changes in finished show order 
    # INPUT: none
    # OUTPUT: none. Prints all quickchanges if any
    def identify_quickchanges(self):
        act1 = self.Order["ACT I"]
        act2 = self.Order["ACT II"]
        print("ACT I:")
        self.identify_quickchanges_act(act1)
        print("ACT II:")
        self.identify_quickchanges_act(act2)
        print("\n\n")

    # check_show: a class function to check the entire show order 
    # INPUT: none
    # OUTPUT: a boolean for whether or not that show order contains conflicts
    def check_show(self):
        act1 = self.Order["ACT I"]
        act2 = self.Order["ACT II"]
        act1_safe = self.check_act(act1)
        # act1_safe = True
        act2_safe = self.check_act(act2)
        print("SUMMARY:")
        if act1_safe:
            print("ACT I has no conflicts")
        else:
            print("ACT I has conflicts")
        if act2_safe:
            print("ACT II has no conflicts")
        else:
            print("ACT II has conflicts")
        if act1_safe and act2_safe:
            print("GOOD SHOW ORDER!")
            return True
        else: return False
        print("\n\n")

# your main function that you use to run the whole program
def master_run():
    Show = PrepareShow()
    # Show.get_overlaps()
    Show.check_show()
    Show.identify_quickchanges()
    print("Order: ",Show.Order)


master_run()