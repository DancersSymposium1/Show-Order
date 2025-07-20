SHOW ORDER CODE README

In the past (up until Spring 2025), we always made the show order by hand and checked its validity using code. In spring 2025, I (sophia holland) built out show order generation code on top of that existing validation program so that we don't have to create the show order by hand. 

To run in terminal:
    python ./generate_orders.py

Relevant files:

    generate_orders.py
        Handles all show order generation and validation.
        If you have a full show order you want to validate, just put that into the "fixed pieces" list. Documentation within this file should be sufficient to figure that part out.

    <semester>_rosters.csv
        Column format:
            name, name, name, name, ...etc, Piece Name
        
        NOTE: validation can be a NIGHTMARE. You have to make sure that across all pieces, one individual has the same listed name. For example, if someone goes by both "Catherine" and "Cathy" and is listed by a partner org as "Cathy" but is listed in all DS pieces as "Catherine", this will show up as two different people until you realize they're the same and you have to go back and manually change their name in all instances :))))))
        --> partner org rosters are given by each partner org. As soon as they're accepted into showcase, ask them to confirm discrepancies (PLEASE).
        --> DS piece rosters are updated by the Directors weekly. Spelling of all names is supposed to be confirmed by choreographers, but a lot of them don't do that, so we do that work too.
        --> Make sure there aren't random spaces after names or the piece name. This could, unfortunately, make a difference.
            --> same with capitalization
        
    tmp.csv
        Outputs the final proposed show order into a more readable format for manual validation
        Gets overwritten each time generate_orders is run, so be ready to save any promising orders before re-running
