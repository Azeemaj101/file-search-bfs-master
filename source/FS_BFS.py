'''
Created on 2 Mar 2014

Title: File search program using BFS
Description: BFS real world application for the completion of assignment in Artificial Intelligence
Author: Ryan Gilera
'''

import os
import fnmatch
from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askdirectory
root = Tk()
# Global variables
nodes = []
file_to_search = ""
isWithExt = False
ask_path = True
ask_file = True


# Class declaration for folder objects
class Folder:
    def __init__(self,path,name,index):
        self.path = path
        self.name = name
        self.index = index
        self.children = []
        self.sub_dir = []



# The main function
def startSearch():
    global file_to_search, path, ask_path, ask_file

    displayTitle()

    while True:
        # Skip the full GUI window, keeping the root window pane from appearing
        Tk().withdraw() 

        while ask_path == True: 
            path = askdirectory(initialdir = 'x:\\',title='Please select a directory to search', mustexist = True) # show an "Open" dialog box and return the path to the selected file
            if not path:
                response = input("Are you sure you want to cancel the program? (y/n): ")
                if response == "y" or response == "yes":
                    return None # Exits the program, if user selected "y" or "yes"
            else:
                ask_path = False    
        # Asks for user input for string matching
        while ask_file == True:
            file_to_search = input("Enter a file to search (file extension optional): ")
            if not file_to_search:
                print("No filename detected. Please try again.\n")
            else:
                ask_file = False

        # Function calls
        file_to_search = analyseFileToSearch(file_to_search)
        initialNode = generateNodes(path)
        breadthFirstSearch(initialNode)
        
        print("\n")
        exit_response = input("Exit program? (y/n): ")
        
        if exit_response == "y":
            return None
        else:
            resetVar()

# Resets global variables
def resetVar():
    global nodes, isWithExt,ask_path, ask_file

    del nodes[:]
    isWithExt = False
    ask_file = True
    ask_path = True


def displayTitle():
    print("**************************************************************\n")
    print("A file search program utilising Breadth First Search Algorithm\n")
    print("Version: 2.0")
    print("Author: Muhammad Azeem")
    print("Date: 05 May 2022\n")
    print("**************************************************************\n")

# Detects if the string input has a file extension included,
# if not, it formats the string input as as "<string>.*"
# It sets the filename to search for any file types that shares the same name
def analyseFileToSearch(filename):
    global isWithExt
    
    if not ("." in filename):
        filename += ".*"
    else:
        isWithExt = True
    
    return filename


def generateNodes(directory):
    global nodes, start

    # Creates instances of class Folder from all possible folders inside the "path" directory 
    # including the root directory "path"
    for i, dir_folder in enumerate(os.walk(directory)):
        nodes.append(Folder(dir_folder[0],getFolderName(dir_folder[0]),i+1))

    # Initialise all children or relationships of each node(folder)
    # This loop sets children with subfolders only to children
    # The reason for that is because os.walk only return subfolders
    for i, dir_folder in enumerate(os.walk(directory)):
        for folder_name in dir_folder[1]:
            for objct in nodes:
                if objct.path == (nodes[i].path + "\\" + folder_name):
                    nodes[i].children.append(objct.index)
    
    # This loop includes the parent folder as the child of children
    for i, ob in enumerate(nodes):
        for child in ob.children:
            for obj in nodes:
                # If this child is the same with this folder and not already in children
                # then add it to children attribute
                if obj.index == child and (not((i+1) in obj.children)):
                    obj.children.append(i+1)
                    break
        
    # Initialises the children name
    for i, dir_folder in enumerate(os.walk(directory)):
        nodes[i].sub_dir.extend(dir_folder[1])
    
    print("\n\n#####################")
    print("Folders detected:")
    print("#####################\n")
    
    # For dry run purposes only
    # Using '_' will let the interpreter you're not using the variable (for later use)
    # otherwise it will keep saying warning: unused variable
    for i, _ in enumerate(nodes):
        print("Folder Name:",nodes[i].name)
        print("Folder Path:",nodes[i].path)
        print("Folder sub-folders:",nodes[i].sub_dir)
        print(" ")
    
    # Sets and returns the start location at root folder
    # For later use in BFS
    begin = nodes[0]
    
    return begin

# Parses folder names from the list
def getFolderName(fname):
    element = 0
    for indx, z in enumerate(fname):
        if z == "/":
            element = indx  
        
        if z == "\\":
            element = indx
            
    folder_name = fname[element+1:]
    return folder_name


def breadthFirstSearch(start):
    in_queue_result = False
    queue = [start]
    result = []
    file_result = []


    print("\n\n\n#################################")
    print("Breadth First Search commencing..")
    print("##################################\n")

    while queue:
        pointer = queue[0]
        queue.pop(0)
        
        print("Pointer now points to folder: ", pointer.path)

        file_result.extend(find_file(file_to_search, pointer.path))
        print("file_result", file_result)
        result.append(pointer)
        print("children:", pointer.children)
        
        for neighbor in pointer.children:
            in_queue_result = False
            for obj in queue:
                # Prints "neighbor:", neighbor+1, "queue:", i.index+1
                if neighbor == obj.index:
                    in_queue_result = True
                        
            for obj in result:
                # Prints "neighbor:", neighbor+1, "result:", j.index+1
                if neighbor == obj.index:
                    in_queue_result = True
            
            # If child is not in queue or result, 
            # append it to queue after the last element of queue
            if in_queue_result == False:
                for obj in nodes:
                    if obj.index == neighbor:
                        queue.append(nodes[obj.index-1])
                        break  
        
        print("queue: ")
        for q in queue:
            print(q.index)
        print(" ")
        
        print("result: ")
        for r in result:
            print(r.index)                 
        print(" \n\n")
        
        
    print("\n\n#####################")
    print("Search Result:")
    print("#####################\n")
    
    # Sorting the possible outcomes and displays it
    if file_result:
        if len(file_result) > 1:
            if isWithExt == False:
                print("Multiple files of \"" + file_to_search[:-2] + "\" are found!")
            else:
                print("Multiple duplicates of " + file_to_search + " are found!")
            
            for document in file_result:
                print(document)
        else:
            if isWithExt == False:
                print("A file bearing the name \"" + file_to_search[:-2] + "\" is found!")
            else:
                print(file_to_search + " is found!")
            print(file_result[0])
    else:
        print("No such file exist. Sorry.")

# Searches for the file in a particular node/folder
def find_file(filename, directory):
    search_result = []
    
    # Searches for the file inside a praticular folder and all matches are save to a list
    filename = fnmatch.filter(os.listdir(os.path.abspath(directory)), filename)

    # All save matches are concatinated with their corresponding path address
    for fn in filename:
        search_result.append(os.path.join(directory, fn))
    
    print("File/s found: ", search_result)
    
    return search_result



# Program starts here
startSearch()