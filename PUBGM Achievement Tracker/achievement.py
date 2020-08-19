#Attributes:

#Completed checkbox
#Planned checkbox
#    When pulling up the achievement info for a leveled achievement, these checkboxes will be the variables for 
#    both the overall checkbuttons and the lvl 5 buttons. When starting up the program, there will have to be a method called
#    that makes sure the checkboxes are in line with the boolean value. This should be the same method as the one used when clicking
#    checkboxes in the program. So, I would start with initializing the highest level and calling the method as soon as
#    the information says to check all checkboxes under that specific level.
#Line_num
#    Stores line number in file for quick access
#Achievement title
#Leveled? Y/N
#    If leveled, will store number of items needed to do for that level
#List? Y/N
#Category



#For class structure for leveled achievements, I was thinking that lower levels should be children of the higher levels. Whenever
#a checkbox is checked, there will be a method in achievement that sets all the children classes to off. For this, I'll need to keep a
#reference to the level lower.

#Text file format:
#    Achievement Title, Leveled? Y, category, <(num5, reward, reward type),(num4, reward, reward type), etc...>, linenum, completed?

