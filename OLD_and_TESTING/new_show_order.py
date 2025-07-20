# WHOLE NEW SHOW ORDER ATTEMPT 3.0
# Author: Amy Zhang
# Date: January 10, 2019
# Last Updated: January 29, 2020
import csv 
import sys
import codecs
import string
from collections import defaultdict

DANCER_FILE = 's25_rosters.csv'
SHOW_ORDER_FILE = 'proposed_order.csv'

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
        # helper function for creating a dictionary of DS piece people using the DANCER_FILE
        # self._import_assigned()
        # helper function for creating a dictionary of outside org people using OUTSIDE_ORGS_FILE
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
                # if "senior solo" in next_piece and (index<len(act)-2):
                #     next_next_piece = act[index+2]
                #     next_next_list = self.Pieces[next_next_piece]
                #     next_list = next_next_list+next_list
                #     next_piece = next_piece + "' and '" + next_next_piece
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
        print("\n\n")

# your main function that you use to run the whole program
def master_run():
    Show = PrepareShow()
    Show.check_show()
    # Show.list_conflicts('Infra','Nina F & Amelia')

    # Show.list_good_pieces('rachel & heeyun')
    # Show.list_bad_pieces('abby & tejas')
    Show.identify_quickchanges()
    # Show.list_dancer_pieces('Sophia Holland')
    # Show.most_conflicting()
    # Show.list_at_least(2)
    # Show.dancer_most_pieces()

master_run()