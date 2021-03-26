Name:       			Amrutha Kenchanagowdra
StudentID:  			1001861876
Programming language used: 	Python3 (Tried with 3.7 and 3.8)



code structure:    
Code is modularized into functions, below are the functions and their respective tasks:
readInputFile: this will read and parse the input file and returns a map
parseHeuristicFile: this will read the heuristic file and returns a map
nodeInfo: is a data structure built to store the node information
gen_succesors: function used to generate successors
printRoute: the function used to print the formatted output route



How to run the code:

Please make sure find_route.py, input_filename and heuristic_filename are in the same directory where you will run the below commands

For Uninformed search:
python3 find_route.py input_filename origin_city destination_city

Example                   
python3 find_route.py input1.txt London  Kassel


For Informed search:
python3 find_route.py input_filename origin_city destination_city heuristic_filename

Example                   
python3 find_route.py input1.txt London  Kassel h_kassel.txt