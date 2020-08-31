import tkinter as tk
from tkinter import *
from tkinter import font
from PIL import Image, ImageTk

class Achievement(tk.Frame):

    def __init__(parent, category, title, desc, level_below, level_rom_num, is_planned, is_completed, num_tasks, points_img, reward_amount, reward_img, info):
        
        self.parent = parent
        self.category = category
        self.title = title
        self.desc = desc
        self.level_below = level_below
        self.level_rom_num = level_rom_num
        self.num_tasks = num_tasks
        self.points_img = points_img
        self.reward_amount = reward_amount
        self.reward_img = reward_img

        # Create two Checkboxes and assign them values here

        # Create the frame
    def get_level_below(self):
        pass
        if self.level_rom_num == 'I':
            return self
        
             





#Attributes:

#Completed checkbox
#Planned checkbox
#    When pulling up the achievement info for a leveled achievement, these checkboxes will be the variables for 
#    both the overall checkbuttons and the lvl 5 buttons. When starting up the program, there will have to be a method called
#    that makes sure the checkboxes are in line with the boolean value. This should be the same method as the one used when clicking
#    checkboxes in the program. So, I would start with initializing the highest level and calling the method as soon as
#    the information says to check all checkboxes under that specific level.
#
#   There should be a binding in AchievementFrame to a method of this class when the checkboxes are checked and therefore the achievement
#   needs to be moved to "completed". This method will delete the frame attribute of the achievement (BUT ONLY THE FRAME, the rest of 
#   the achievement attributes will remain. Once this is done, there will be a call to from Achievement Frame to Completed Frame to 
#   reinitialize the achievement with all the achievement attributes. Next, the file will be updated for these updated boolean values.
#   I'm thinking that the achievement info will have to be re-initialized as well, since changing the parents is impossible and I figure 
#   that you can't raises a widget above it's parent either.
#
#   Once a checkbox is checked, there will be need to be a call to Overview frame where all the data is stored. If checked, update the
#   following: total achievements completed, total points, total achievements out of category, reward. once unchecked, subtract these values.


#Achievement title
#Leveled? Y/N
#    If leveled, will store number of items needed to do for that level
#List? Y/N
#Category
#Reward Image
#    This will be the actual image itself. Passed in to the init_fuction will be the location of where to find it (name must match icon file name)
#Parent
#    This is the parent frame which the achievement frame is a child of. When achievement is not completed, this will be the achievement frame. When
#    completed, this will be the completed frame.
#List of tasks:
#    Each list achiivement will need a list of the tasks to do
#Number of Points:
#   Will need to store an int of how many points the achievement has under completion
#Points picture:
#   Won't need to store this but will need to use this temporarily to initalize the frame.
#Completed?
#   Completed will be true if the maximum level of the achievement is completed.
#Next
#   Each leveled achievement should have reference to the one below it

#For class structure for leveled achievements, I was thinking that lower levels should be children of the higher levels. Whenever
#a checkbox is checked, there will be a method in achievement that sets all the children classes to off. For this, I'll need to keep a
#reference to the level lower.

#Text file format:
#    Achievement Title, Leveled? Y, category, <(V, C?, P?, reward, reward type),(IV, C?, P?, reward, reward type), etc...>
#                                           , if list: <task1, task2, task3, etc>, C?, P?
#                                           
  


    #Updating line in file:
    #    Read entire file into memory using file reader. Store as a list so you can access the ith row.
    #    If checkboxes are both checked: update the file by writing the same line but with both Ys. For this,
    #    a function will need to be created to return the correctly formatted string needed to update the line. 
    #    For unchecking, vice versa. I think that there should be some other function that handles the boolean values of
    #    the achievements before the create string method is used. In the function, lets try saving immediately and see
    #    how much processing power that takes.

