# Types of files
# Text files: .text, .pdf, .docx, .log etc
# Binary files: .mp4, .mov, .png, .jpeg etc

# open file
# openedFile = open("sample.text","r") # open a file
# data = openedFile.read() # read the data from opened file
# print("data", data)
# openedFile.close()

# writing to a file
# two modes: w, a
# w - write - overwrite the file and add new text
# a - append - append text at the end
# openedFile = open("sample.text","a") # open a file
# data = openedFile.write(" Updated text in file") 
# print("data", data)
# openedFile.close()

# with syntax
with open("sample.text","r") as f:
    data = f.read()
    # print(data)

# Note: here with automatically close the file so we no need to close file manually


# Deleting file
import os
# os.remove("sample.text")