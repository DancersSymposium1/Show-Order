DANCER_FILE = 'S16 Assigned-Unassigned - Sheet1.csv'
OUTSIDE_ORGS_FILE = '[DS] Outside Orgs Sign-Up S16 - Sheet1.csv'
SHOW_ORDER_FILE = 'Show Order Format - S16.csv'

class Show_Order(object):
    
    def __init__(self, ShowOrder, conflictMap):
        self.ShowOrder = ShowOrder
        self.conflictMap = conflictMap

    def __repr__(self):
        for act in self.ShowOrder:
            print act
            for dance in self.ShowOrder[act]:
                print dance
            print
        return "ShowOrder & conflictMap wrapper class"

    def check_order(self):
        errors = False
        print "ACT 1:"
        for i in xrange(1, len(self.ShowOrder["ACT 1"])):
            previousPiece, currentPiece = self.ShowOrder["ACT 1"][i - 1], self.ShowOrder["ACT 1"][i]
            if previousPiece in self.conflictMap[currentPiece]:
                errors = True
                print "Conflict occured with #%d and #%d: %s and %s share dancers" % (i - 1,
                                                                                      i,
                                                                                      previousPiece,
                                                                                      currentPiece)
        print "\nACT 2:"
        for i in xrange(1, len(self.ShowOrder["ACT 2"])):
            previousPiece, currentPiece = self.ShowOrder["ACT 2"][i - 1], self.ShowOrder["ACT 2"][i]
            if previousPiece in self.conflictMap[currentPiece]:
                errors = True
                print "Conflict occured with #%d and #%d: %s and %s share dancers" % (i - 1 + len(self.ShowOrder["ACT 1"]),
                                                                                      i + len(self.ShowOrder["ACT 1"]),
                                                                                      previousPiece,
                                                                                      currentPiece)
        return ~errors

    def switch(self, dance1, dance2):
        if dance1 in self.ShowOrder["ACT 1"]: dance1_i, act_i_d1 = self.ShowOrder["ACT 1"].index(dance1), "ACT 1"
        elif dance1 in self.ShowOrder["ACT 2"]: dance1_i, act_i_d1 = self.ShowOrder["ACT 2"].index(dance1), "ACT 2"
        else: print "%s is not in the ShowOrder\nCheck spelling" % dance1

        if dance2 in self.ShowOrder["ACT 1"]: dance2_i, act_i_d2 = self.ShowOrder["ACT 1"].index(dance2), "ACT 1"
        elif dance2 in self.ShowOrder["ACT 2"]: dance2_i, act_i_d2 = self.ShowOrder["ACT 2"].index(dance2), "ACT 2"
        else: print "%s is not in the ShowOrder\nCheck spelling" % dance2

        self.ShowOrder[act_i_d2][dance2_i], self.ShowOrder[act_i_d1][dance1_i] = self.ShowOrder[act_i_d1][dance1_i], self.ShowOrder[act_i_d2][dance2_i]
        print "Switch between %s and %s complete!" % (dance1, dance2)

def conflict(dancers1, dancers2):
    for dancer in dancers1:
        if dancer in dancers2:
            return True
    return False

def import_ShowOrder():
    Pieces = {}
    last_choreographer = ""
    dancer_file = open(DANCER_FILE, 'rU')
    for i, line in enumerate(dancer_file):
        text = line.strip().split(",")

        try:
            parse_attempt = int(text[0])
            dancer = text[1].strip()
            Pieces[last_choreographer].append(dancer)
            #print "Successfully added %s to %s's piece" % (dancer, last_choreographer)
        except:
            last_choreographer = text[0].strip()
            Pieces[last_choreographer] = [] #create piece in map
            #print "Successfully created %s's piece" % last_choreographer    
    dancer_file.close()

    outside_file = open(OUTSIDE_ORGS_FILE, 'rU')
    for i, line in enumerate(outside_file):
        text = line.strip().split(",")
        
        pieceName = text[-1]
        performers = text[0:-1]
        for i_p in xrange(len(performers)): performers[i_p] = performers[i_p].strip()
        if len(pieceName) != 0: #if valid pieceName
            Pieces[pieceName] = performers
    outside_file.close()

    del Pieces[""]

    conflictMap = {}
    for piece1 in Pieces:
        conflictMap[piece1] = []
        for piece2 in Pieces:
            if (piece1 != piece2) and (conflict(Pieces[piece1], Pieces[piece2])):
                conflictMap[piece1].append(piece2)

    ShowOrder = {}
    ShowOrder["ACT 1"], ShowOrder["ACT 2"] = [], []
    showOrder_file = open(SHOW_ORDER_FILE, 'rU')
    for i, line in enumerate(showOrder_file):
    
        text = line.strip().split(",")
        if len(text[0]) > 0: ShowOrder["ACT 1"].append(text[0]) 
        if len(text[1]) > 0: ShowOrder["ACT 2"].append(text[1])

        #assert correctness in ACT1 and ACT2
        #ACT1[i] = text[0]
        #ACT2[i] = text[1]
    showOrder_file.close()

    # pop headers
    ShowOrder["ACT 1"].pop(0)
    ShowOrder["ACT 2"].pop(0)

    return (ShowOrder, conflictMap)

def master_run():
    (ShowOrder, conflictMap) = import_ShowOrder()
    SO = Show_Order(ShowOrder, conflictMap)

    if SO.check_order(): print "\nVerdict: This schedule works!"
    else: print "\nVerdict: Review previous errors"

    return SO

master_run()
