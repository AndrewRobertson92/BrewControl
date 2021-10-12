'''mash class for creating saving and loading mash recipes '''



class Mash_Recipe:
    #mash class have properties
    def __init__(self,mash_time,target_temp,logging_on):
        self.mash_time = mash_time
        self.target_temp = target_temp
        self.logging_on = logging_on
    def list_atributes(self):
        #returns the recipe atributes as list for iteration
        #
        atribute=[self.mash_time,self.target_temp,self.logging_on]
        return(atribute)
        
    def read_mash_file(self,address):
        mash_config=open(address, "r")      
        ##im sure theres a much more ellegant way to loop through the atributes of mash_recipe
        line=(mash_config.readline())
        equals_index = line.find("=")
        self.mash_time = line[equals_index+2:-1]
        line=(mash_config.readline())
        equals_index = line.find("=")
        self.target_temp = line[equals_index+2:-1]
        line=(mash_config.readline())
        equals_index = line.find("=")
        self.logging_on = line[equals_index+2:-1]
        mash_config.close()
               
    def save_mash_file(self,address):
        #saves the current mash settings 
        mash_config=open(address, "r")

        #coppy old config into a list
        mash_config=open(address, "r")
        old_file=[]
        mash_config=mash_config.readlines()
        for line in mash_config:
            
            old_file.append(line.strip())
        # again this is ugly but funtional, 
        # if I want to add more atributes an interative method is definately needed
        line=old_file[0]
        equals_index = line.find("=")
        line =line[:equals_index+1] +" " + str(self.mash_time)
        old_file[0]=line

        line=old_file[1]
        equals_index = line.find("=")
        line =line[:equals_index+1] + " " + str(self.target_temp)
        old_file[1]=line

        line=old_file[2]
        equals_index = line.find("=")
        line =line[:equals_index+1] + " " + str(self.logging_on)
        old_file[2]=line

        #Overwrite the old file
        with open(address,"w+") as f:
            for item in old_file:
                f.writelines("%s\n" % item)




      
      

        