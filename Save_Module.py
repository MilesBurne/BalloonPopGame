#File Handling Class by Miles Burne 8/3/19
#class used to save the game, takes no values to initilise, has two public methods, save and load, and one private method load_data_handle
class Save_Game():
    #init
    def __init__(self):
        self.filename = "save_file.txt" #save file name
        #importing os locally
        import os
        self.os = os

    #method to delete the save file
    def delete(self):
        #uses os.remove to remove file
        self.os.remove(self.filename)
        
    #method used to save the players score and level, takes input of score,level
    def save(self, score, level):
        #wipes the save file
        file = open(self.filename, 'w+')
        file.truncate(0)
        file.close()

        #imports datetime locally
        import datetime
        self.datetime = datetime
        
        #preparing necessary variables for the saving
        time_stamp = str(self.datetime.datetime.now())
        total_check = str(((score+level)**3)/2) #used to check the total of score and level as (total**3)/2 to verify file
        save_score = str(score)
        save_level = str(level)
        
        #opens file again to insert data into file
        file = open(self.filename,"w+")
        file.write(time_stamp+"\n"+save_score+"\n"+save_level+"\n"+total_check)
        file.close()

    #load function, returns 0 if the file is invalid or not present, or [score,level] in every other case
    def load(self):
        #reads file contents and closes it, also checks if file is present #FileNotFoundError
        file_present = True
        try:
            file = open(self.filename,"r")
        except FileNotFoundError:
            file_present = False
            
        #returns 0 if file is not present, otherwise continues program
        if file_present != True: 
            return(0)
        else:
            content = file.read()
            file.close()

        #return statement, if file is not present program does not reach this line
        return(self.__load_data_handle(content))
            
    #function to display if file present, returns False if false
    def is_file_present(self):
        #reads file contents and closes it, also checks if file is present #FileNotFoundError
        file_present = True
        try:
            file = open(self.filename,"r")
            file.close()
        #file not present
        except FileNotFoundError:
            file_present = False
        return(file_present)
            
    #private method to handle the content handling of the load class, returns [score,level], or 0 if data is invalid 
    def __load_data_handle(self,content):
        #strips superflous data and makes it readable ###ValueError
        content_array = content.split("\n")
        content_array.pop(0) #removes time_stamp from file
        
        #checks for invalid data
        data_valid = True
        try:
            load_score = int(content_array[0])
            load_level = int(content_array[1])
            load_total_check = float(content_array[2])
            if load_total_check != float((load_score+load_level)**3)/2:
                data_valid = False
            else:
                pass

        except ValueError:
                data_valid = False

        #returning data, returns (0) if data invalid or file is not present
        if data_valid == False:
            return(0)
        else:
            return(load_score,load_level)

