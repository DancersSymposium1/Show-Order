from Tkinter import *

DANCER_FILE = 'F16 Assigned-Unassigned - Sheet1.csv'
OUTSIDE_ORGS_FILE = '[DS] Outside Orgs Sign-Up F16 - Sheet1.csv'
SHOW_ORDER_FILE = 'Show Order Format - F16.csv'

DRINK_NAMES = ["Amy Lee", "Sarah Deluty", "Sabrina Liu", "Tusher Gabhane", "Lisa Natale"]
DRINK_LIST = [] #editable

def make_list(dic):
    s = []
    for act in dic:
        for piece in dic[act]:
            s.append(piece)
    return s

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
                for drink_val in DRINK_LIST:
                    if (previousPiece == drink_val[0]) and (currentPiece == drink_val[1]):
                        print "Take a shot! (Thanks %s)" % drink_val[2]

        print "\nACT 2:"
        for i in xrange(1, len(self.ShowOrder["ACT 2"])):
            previousPiece, currentPiece = self.ShowOrder["ACT 2"][i - 1], self.ShowOrder["ACT 2"][i]
            if previousPiece in self.conflictMap[currentPiece]:
                errors = True
                print "Conflict occured with #%d and #%d: %s and %s share dancers" % (i - 1 + len(self.ShowOrder["ACT 1"]),
                                                                                      i + len(self.ShowOrder["ACT 1"]),
                                                                                      previousPiece,
                                                                                      currentPiece)
                for drink_val in DRINK_LIST:
                    if (previousPiece == drink_val[0]) and (currentPiece == drink_val[1]):
                        print "Take a shot! (Thanks %s)" % drink_val[2]

        return (not errors)

    def switch(self, dance1, dance2):
        if dance1 in self.ShowOrder["ACT 1"]: dance1_i, act_i_d1 = self.ShowOrder["ACT 1"].index(dance1), "ACT 1"
        elif dance1 in self.ShowOrder["ACT 2"]: dance1_i, act_i_d1 = self.ShowOrder["ACT 2"].index(dance1), "ACT 2"
        else: print "%s is not in the ShowOrder\nCheck spelling" % dance1

        if dance2 in self.ShowOrder["ACT 1"]: dance2_i, act_i_d2 = self.ShowOrder["ACT 1"].index(dance2), "ACT 1"
        elif dance2 in self.ShowOrder["ACT 2"]: dance2_i, act_i_d2 = self.ShowOrder["ACT 2"].index(dance2), "ACT 2"
        else: print "%s is not in the ShowOrder\nCheck spelling" % dance2

        self.ShowOrder[act_i_d2][dance2_i], self.ShowOrder[act_i_d1][dance1_i] = self.ShowOrder[act_i_d1][dance1_i], self.ShowOrder[act_i_d2][dance2_i]
        print "Switch between %s and %s complete!" % (dance1, dance2)

    def no_conflict(self, piece):
        result = []
        for act in self.ShowOrder:
            for piece_i in self.ShowOrder[act]:
                if piece_i not in self.conflictMap[piece]:
                    result.append(piece_i)
        return result

    def help(self):
        print "List of functions:"
        print "\tSO.ShowOrder\t\t\t- dictionary of the show order, organized by Act Number"
        print "\t\t\t\t\t  which stores a list of the pieces in order"
        print "\tSO.conflictMap\t\t\t- dictionary of the conflict map, organized by Act Number"
        print "\t\t\t\t\t  which stores a list of each piece that conflicts with the"
        print "\t\t\t\t\t  corresponding piece in ShowOrder"
        print "\tSO.check_order()\t\t- checks the order of the given ShowOrder"
        print "\tSO.switch(dance1, dance2)\t- switches 'dance1' with 'dance2' in ShowOrder"
        print "\tSO.no_conflict(self, piece)\t- returns a list of all the pieces that do not conflict with 'piece'"

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
                drink_list_create(Pieces, piece1, piece2)
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
    else: print "\nVerdict: Review previous errors (call 'SO.help() for details')"
    return SO

def drink_list_create(Pieces, piece1, piece2):
    for drink_dancer in DRINK_NAMES:
        if (drink_dancer in Pieces[piece1]):
            if (drink_dancer in Pieces[piece2]): 
                DRINK_LIST.append([piece1, piece2, drink_dancer])

def walk(SO):

    def points_to_pixels(pt): # techically (pt*4/3) but was making things too big on the page
        return round(pt * 4 / 5) 

    def get_maxCellWidth(pp_list):
        maxCellWidth = 0
        for piece in pp_list:
            if maxCellWidth < len(piece): 
                maxCellWidth = len(piece)
        return maxCellWidth
        
    def make_possible_pieces(SO):
        possible_pieces = []
        for act in SO.ShowOrder:
            for piece in SO.ShowOrder[act]:
                possible_pieces.append(piece)
        possible_pieces.sort()
        possible_pieces.insert(0, "Possible Pieces")
        return possible_pieces

    def inside_rect(x, y, corners):
        return (corners[0] <= x) and (corners[1] <= y) and (x <= corners[2]) and (y <= corners[3])

    def init():
        data.possible_pieces = make_possible_pieces(SO)
        maxCellWidth = get_maxCellWidth(data.possible_pieces)
        # x is width, y is height
        font_size = 8

        data.cellWidth = points_to_pixels(maxCellWidth * font_size)
        data.cellHeight_pp, data.cellHeight_final = 3*font_size, 4*font_size

        total_cellHeight_pp = data.cellHeight_pp*(len(data.possible_pieces)+1) 
        total_cellHeight_final = data.cellHeight_final*(max(len(SO.ShowOrder["ACT 1"]), len(SO.ShowOrder["ACT 2"])) + 1)

        data.borderMargin, data.middleMargin = 5, 20
        data.winWidth = 2*data.borderMargin + 4*data.cellWidth + 2*data.middleMargin
        data.winHeight = 2*data.borderMargin + max(total_cellHeight_pp, total_cellHeight_final)

        data.final_ShowOrder = []
        data.functionButtons = ["RESET", "UNDO", "____"]
        maxFunCellWidth = get_maxCellWidth(data.functionButtons)
        font_size_fun = 12
        data.funCellWidth = points_to_pixels(maxFunCellWidth * font_size_fun * 1.5)
        data.funCellHeight = 4 * font_size_fun

        data.corners_pp, data.corners_pp_corners = [], []
        for i in xrange(1, len(data.possible_pieces)):
            cpp = (data.borderMargin, 
                   data.borderMargin + ((2*i+1) * data.cellHeight_pp) / 2,
                   data.borderMargin + data.cellWidth,
                   data.borderMargin + ((2*i+3) * data.cellHeight_pp) / 2) #x0, y0, x1, y1
            data.corners_pp.append(cpp)
        
        # figure out the large dimensions of the possible pieces
        data.corners_pp_corners = (data.borderMargin, 
                                   data.borderMargin + (3 * data.cellHeight_pp) / 2,
                                   data.borderMargin + data.cellWidth,
                                   data.borderMargin + ((2 * len(data.possible_pieces) + 3) * data.cellHeight_pp) / 2)

        data.corners_f1, data.corners_f2 = [], []
        for i in xrange(1, len(SO.ShowOrder["ACT 1"])):
            cf1 = (data.borderMargin + data.cellWidth + data.middleMargin, 
                   data.borderMargin + i * data.cellHeight_final,
                   data.borderMargin + 2 * data.cellWidth + data.middleMargin,
                   data.borderMargin + (i+1) * data.cellHeight_final) #x0, y0, x1, y1
            data.corners_f1.append(cf1)
        for i in xrange(1, len(SO.ShowOrder["ACT 2"])):
            cf2 = (data.borderMargin + 2 * data.cellWidth + data.middleMargin, 
                   data.borderMargin + i * data.cellHeight_final,
                   data.borderMargin + 3 * data.cellWidth + data.middleMargin,
                   data.borderMargin + (i+1) * data.cellHeight_final) #x0, y0, x1, y1
            data.corners_f2.append(cf2)

        data.corners_function = []
        for i in xrange(len(data.functionButtons)):
            cf = (data.winWidth - data.borderMargin - data.funCellWidth, 
                  data.winHeight - data.borderMargin - (len(data.functionButtons) - i) * data.funCellHeight,
                  data.winWidth - data.borderMargin,
                  data.winHeight - data.borderMargin - (len(data.functionButtons) - 1 - i) * data.funCellHeight) #x0, y0, x1, y1
            data.corners_function.append(cf)

    def mousePressed(event): #@TODO: Finish mousePressed and its helper functions
        x, y = event.x, event.y
        if inside_rect(x, y, data.corners_function[0]): # pushed reset button
            reset()
        elif inside_rect(x, y, data.corners_function[1]): # pushed undo button
            undo()
        elif inside_rect(x, y, data.corners_function[2]): # pushed ____ button
            pass

        elif inside_rect(x, y, data.corners_pp_corners):
            for i in xrange(len(data.corners_pp)):
                if inside_rect(event.x, event.y, data.corners_pp):
                    select_pp(data.corners_pp(i))
                                
    def timerFired(): pass

    def redrawAll(canvas):
        # possible pieces
        canvas.create_text(data.borderMargin + data.cellWidth / 2,
                           data.borderMargin + data.cellHeight_pp,
                           text=data.possible_pieces[0], font="Arial 12 bold")
        for i in xrange(1, len(data.possible_pieces)):
            canvas.create_text(data.borderMargin + data.cellWidth / 2, 
                               data.borderMargin + (i+1) * data.cellHeight_pp,
                               text=data.possible_pieces[i])
            corners_pp = (data.borderMargin, 
                          data.borderMargin + ((2*i+1) * data.cellHeight_pp) / 2,
                          data.borderMargin + data.cellWidth,
                          data.borderMargin + ((2*i+3) * data.cellHeight_pp) / 2) #x0, y0, x1, y1
            canvas.create_rectangle(corners_pp)

        # final ShowOrder (@TODO: Implement with new list)
        canvas.create_text(data.borderMargin + 3 * data.cellWidth / 2 + data.middleMargin,
                           data.borderMargin + data.cellHeight_final / 2,
                           text="ACT 1", font="Arial 12 bold")
        for i in xrange(1, len(SO.ShowOrder["ACT 1"])):
            canvas.create_text(data.borderMargin + 3 * data.cellWidth / 2 + data.middleMargin,
                               data.borderMargin + (data.cellHeight_final * (2*i + 1)) / 2,
                               text=SO.ShowOrder["ACT 1"][i])
            corners_final_1 = (data.borderMargin + data.cellWidth + data.middleMargin, 
                               data.borderMargin + i * data.cellHeight_final,
                               data.borderMargin + 2 * data.cellWidth + data.middleMargin,
                               data.borderMargin + (i+1) * data.cellHeight_final) #x0, y0, x1, y1
            canvas.create_rectangle(corners_final_1)

        canvas.create_text(data.borderMargin + 5 * data.cellWidth / 2 + data.middleMargin,
                           data.borderMargin + data.cellHeight_final / 2,
                           text="ACT 2", font="Arial 12 bold")
        for i in xrange(1, len(SO.ShowOrder["ACT 2"])):
            canvas.create_text(data.borderMargin + 5 * data.cellWidth / 2 + data.middleMargin,
                               data.borderMargin + (data.cellHeight_final * (2*i + 1)) / 2,
                               text=SO.ShowOrder["ACT 2"][i])
            corners_final_2 = (data.borderMargin + 2 * data.cellWidth + data.middleMargin, 
                               data.borderMargin + i * data.cellHeight_final,
                               data.borderMargin + 3 * data.cellWidth + data.middleMargin,
                               data.borderMargin + (i+1) * data.cellHeight_final) #x0, y0, x1, y1
            canvas.create_rectangle(corners_final_2)

        # bottom-right three buttons
        for i in xrange(len(data.functionButtons)):
            canvas.create_text(data.winWidth - data.borderMargin - data.funCellWidth / 2,
                               data.winHeight - data.borderMargin - ((2 * (len(data.functionButtons) - 1 - i) + 1) * data.funCellHeight) / 2,
                               text=data.functionButtons[i], font="Arial 12")
            corners_function = (data.winWidth - data.borderMargin - data.funCellWidth, 
                                data.winHeight - data.borderMargin - (len(data.functionButtons) - 1 - i) * data.funCellHeight,
                                data.winWidth - data.borderMargin,
                                data.winHeight - data.borderMargin - (len(data.functionButtons) - i) * data.funCellHeight) #x0, y0, x1, y1
            canvas.create_rectangle(corners_function)

    def redrawAllWrapper(canvas):
        canvas.delete(ALL)
        redrawAll(canvas)
        canvas.update()

    def mousePressedWrapper(event, canvas):
        mousePressed(event)
        redrawAllWrapper(canvas)

    def keyPressedWrapper(event, canvas):
        keyPressed(event)
        redrawAllWrapper(canvas)

    def timerFiredWrapper(canvas):
        timerFired()
        redrawAllWrapper(canvas)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas)
        
    # Set up data and call init
    class Struct(): pass
    data = Struct()
    data.timerDelay = 100 # milliseconds
    init()
    # create the root and the canvas
    root = Tk()
    root.wm_title("Walk Algorithm")
    canvas = Canvas(root, width=data.winWidth, height=data.winHeight)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event: mousePressedWrapper(event, canvas))
    timerFiredWrapper(canvas)
    # and launch the app
    root.mainloop() # blocks until window is closed
    print("Walk done.")

SO = master_run()
