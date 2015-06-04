DANCER_FILE = 'S15 Assigned-Unassigned - Sheet1.csv'
OUTSIDE_ORGS_FILE = '[DS] Outside Orgs Sign-Up S15 - Sheet1.csv'
SHOW_ORDER_FILE = 'DS Show Order S15 - Sheet1.csv'

def conflict(dancers1, dancers2):
    for dancer in dancers1:
        if dancer in dancers2:
            return True
    return False

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
showOrder_file = open(SHOW_ORDER_FILE, 'rU')
for i, line in enumerate(showOrder_file):
    text = line.strip().split(",")

    pieceName = text[4]
    if len(pieceName) > 0:
        if pieceName == "ACT I":
            act = 1
            ShowOrder["ACT I"] = []
        elif pieceName == "ACT II":
            act = 2
            ShowOrder["ACT II"] = []
        elif act == 1:
            ShowOrder["ACT I"].append(pieceName)
        elif act == 2:
            ShowOrder["ACT II"].append(pieceName)
        else:
            assert(False)
showOrder_file.close()

errors = False
print "ACT 1:"
for i in xrange(1, len(ShowOrder["ACT I"])):
    previousPiece, currentPiece = ShowOrder["ACT I"][i - 1], ShowOrder["ACT I"][i]
    if previousPiece in conflictMap[currentPiece]:
        errors = True
        print "Conflict occured with #%d and #%d: %s and %s share dancers" % (i - 1,
                                                                              i,
                                                                              previousPiece,
                                                                              currentPiece)
print "\nACT 2:"
for i in xrange(1, len(ShowOrder["ACT II"])):
    previousPiece, currentPiece = ShowOrder["ACT II"][i - 1], ShowOrder["ACT II"][i]
    if previousPiece in conflictMap[currentPiece]:
        errors = True
        print "Conflict occured with #%d and #%d: %s and %s share dancers" % (i - 1 + len(ShowOrder["ACT I"]),
                                                                              i + len(ShowOrder["ACT I"]),
                                                                              previousPiece,
                                                                              currentPiece)

if not errors: print "\nVerdict: This schedule works!"
else: print "\nVerdict: Review previous errors"

    


