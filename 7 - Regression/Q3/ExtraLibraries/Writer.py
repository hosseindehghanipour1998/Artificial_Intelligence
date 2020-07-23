class Writer :


    def __init__(self,filePath):
        self.filePath = filePath
        if ( self.__fileExists() == True):
            print("Handle Binded With Existing File Named : " + str(self.filePath))
        else :
            self.__createFile(self.filePath)
            print("New File Named " + str(self.filePath) + " Created !")



    def append(self,string):
        try:
            f = open(self.filePath, "a")
            f.write(str(string) + "\n")
            f.close()
        except:
            print("File Not Found")


    def __createFile(self,fileName):
        f = open(fileName, "w+")
        f.close()




    def readFile(self):
        try:
            f = open(self.filePath,"r")
            lines = f.read().split('\n')
            f.close()
            return lines
        except:
            return None



    def __fileExists(self):
        try:
            f = open(self.filePath,"r")
            f.close()
            return True

        except:
            return False



    def __contentExists(self,content):
        wordsList = self.readFile()
        wordsList = map(lambda x:x.lower(),wordsList)
        if(wordsList != None):
            if (str(content)).lower() in wordsList :
                return True
        return False



    def arrayToFile(self,arr):
        if(self.__fileExists() == False ):
            self.__createFile(self.filePath)
        for item in arr :
            self.append(item)


    def getLen(self):
        wordsList = self.readFile()
        if(wordsList != None):
            return len(wordsList)
        return None



    def createBackup(self):
        fileParts = self.filePath.split(".")
        backupFileName = str(str(fileParts[0]) + "-BackUp." + str(fileParts[1]))
        self.__createFile(backupFileName)
        arrList = self.readFile()
        for item in arrList :
            self.__append(backupFileName,item)
        print("Backup File Created")

    def __append(self,backupFileName,string):
        try:
            f = open(backupFileName, "a")
            f.write(str(string) + "\n")
            f.close()
        except:
            print("File Not Found")



    def appendNoneRepeated(self,content):
        if (self.__contentExists(content) == False and content != ""):
            self.append(content)
            return True # Successful Operation
        else :
            return False # Word Already Exists



    def deleteContent(self,contentList):
        lines = self.readFile()
        filter(lambda a: a != " ", lines)
        filter(lambda a: a != "", lines)
        newList = []

        for line in lines :
            if (not line in contentList ):
                newList.append(line)

        self.__createFile(self.filePath)
        for item in newList :
            self.append(item)

    def clearFile(self):
        self.__createFile(self.filePath)

    def removeRedundantData(self):
        lines = self.readFile()
        newList = []
        for item in lines :
            if ( not item in newList):
                newList.append(item)
        self.clearFile()

        for item in newList :
            self.append(item)
