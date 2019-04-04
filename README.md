SHOW ORDER CODE README

To run the new show order code, download show_order_new.py

Save the Assigned/Unassigned list as:
'F18 Assigned-Unassigned - Sheet1.csv'

The Outside Organization list as:
'Outside Orgs Sign-Up F18 - Sheet1.csv'

The Show Order list as:
'Show Order Format - F18.csv'

(update the semester and year in the .py file as well if you want to save in the updated name)

MAKE SURE TO SAVE AS A .csv FILE 

Then pray to the CS Gods that the code works

Things To Check For Issues (if you need to debug)
-Names spelled differently in Assigned List and Outside Org List (if there are issues, it’s easiest to change Assigned List)
-Pieces spelled differently in both lists and Show Order (can use piece_found function to see if a show order piece is in the lists)
-Pieces in Assigned List have exactly one blank line in between them
-Names with special characters (letters with accents for instance)

If all else fails, at random print and break statements everywhere and pray to the CS gods you find the problem

User Functions
import_pieces()
PARAMETERS: none
RETURNS: a dictionary with the pieces in the Assigned List and Outside Org List as keys and the values storing a list of dancers in their respective pieces

import_order()
PARAMETERS: none
RETURNS: a dictionary with “ACT I” and “ACT II” as the keys and their values storing lists of all of the pieces in those respective acts (in order)

check_show(Pieces, Order)
PARAMETERS: Pieces (a dictionary of the pieces in the show, as created by import_pieces()) and Order (a dictionary of the show order list, as created by import_order())
RETURNS: nothing
However, it will print("CONFLICT: There are conflicting dancers between '" + current_piece + "' and '" + next_piece + "'. Here are the conflicts:") and then print all of the dancers that have conflicts
It will also print a SUMMARY, telling if ACT I has conflicts and ACT II has conflicts.
If the show order has no conflicts, it will print GOOD SHOW ORDER

(If you want to allow senior solos as quick changes, comment out the if statement starting at line 143)

list_conflicts(Pieces, piece1, piece2)
PARAMETERS: Pieces (dictionary from import_pieces()), piece1 (the name of the first piece you want), and piece2 (the name of the second piece you want)
RETURNS: It will print("Here are all of the dancers that have a conflict with '" + piece1 + "' and '" + piece2 + "':") followed by all of the dancers that have conflicts.

list_good_pieces(Pieces, piece)
PARAMETERS: Pieces (dictionary from import_pieces()) and piece (the name of the piece you want)
RETURNS: print("Here are all of the pieces that don't have a conflict with '" + piece + "':") followed by all of the pieces that have no conflicts

piece_found(Pieces, piece)
PARAMETERS: Pieces (dictionary from import_pieces()) and piece (the name of the piece you want)
RETURNS: True or False if the piece is found in your dictionary
It will also print if the piece was found or not

import_dancers(Pieces)
PARAMETERS: Pieces (dictionary from import_pieces())
RETURNS: a dictionary dancer names as the keys and a list of the pieces theyre in as the values

list_dancer_pieces(Dancers, dancer)
PARAMETERS: Dancers (dictionary from import_dancers(Pieces)) and dancer (a dancer’s name)
RETURNS: it will print ("Here are the pieces that '" + dancer + "' is in:") followed by the list of pieces they are in. If they can’t find the dancer, an error message will come up.

list_bad_pieces(Pieces, piece)
PARAMETERS: Pieces (dictionary from import_pieces()) and piece (a piece name)
RETURNS: it will print ("Here are all of the pieces that have a conflict with '" + piece + "':) followed by the list of pieces that conflict with the given piece.

most_conflicting(Pieces)
PARAMETERS: Pieces (dictionary from import_pieces()) 
RETURNS: it will print ("The pieces with the most conflicts will conflict with " + str(max_conflicts) + " other pieces. Here are the pieces with this number of conflicts:”), which tells us the max number of conflicts any piece has, followed by a list of all of the pieces with this number of conflicts.

list_at_least(Dancers, num)
PARAMETERS: Dancers (dictionary from import_dancers(Pieces)) and num (number of pieces as the minimum)
RETURNS: it will print ("These are all of the dancers in at least " + str(num) + " pieces:") followed by the name of each dancer and the number of pieces they are in

dancer_most_pieces(Dancers)
PARAMETERS: Dancers (dictionary from import_dancers(Pieces))
RETURNS: it will print ("The dancers with the most pieces have " + str(max_pieces) + " other pieces. Here are the dancers with this number of pieces: ") followed by the names of each of the dancers that have the most number of pieces.


If you need any other function descriptions, check the code comments or ask me (Amy Zhang) 
