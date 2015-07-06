DANCER_FILE = 'S15 Assigned-Unassigned - Sheet1.csv'
OUTSIDE_ORGS_FILE = '[DS] Outside Orgs Sign-Up S15 - Sheet1.csv'
SHOW_ORDER_FILE = 'Show Order Format - S15.csv'

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

errors = False
print "ACT 1:"
for i in xrange(1, len(ShowOrder["ACT 1"])):
    previousPiece, currentPiece = ShowOrder["ACT 1"][i - 1], ShowOrder["ACT 1"][i]
    if previousPiece in conflictMap[currentPiece]:
        errors = True
        print "Conflict occured with #%d and #%d: %s and %s share dancers" % (i - 1,
                                                                              i,
                                                                              previousPiece,
                                                                              currentPiece)
print "\nACT 2:"
for i in xrange(1, len(ShowOrder["ACT 2"])):
    previousPiece, currentPiece = ShowOrder["ACT 2"][i - 1], ShowOrder["ACT 2"][i]
    if previousPiece in conflictMap[currentPiece]:
        errors = True
        print "Conflict occured with #%d and #%d: %s and %s share dancers" % (i - 1 + len(ShowOrder["ACT I"]),
                                                                              i + len(ShowOrder["ACT I"]),
                                                                              previousPiece,
                                                                              currentPiece)

if not errors: print "\nVerdict: This schedule works!"
else: print "\nVerdict: Review previous errors"

    


