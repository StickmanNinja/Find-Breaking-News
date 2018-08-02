# Made required imports
import types


# This function figures out what type of value x is
def varType(x):
    if type(x) == list or type(x) == tuple:
        return "list" #For practical purposes, tuples are lists.
    if type(x) == str:
        return "string"
    if type(x) == int or type(x) == float:
        return "number"
    else:
        return "unknown"

class Convert:
    # This is a reference to the class itself, allowing me to use self.AddName() and so on.
    def __init__(self):
        # This is the most important variable. It stores the JSON string.
        self.var = ""

    # This method function is basically the same as AddString, except it doesn't add quotation marks.
    def AddNum(self, givennumber):
        self.var = self.var + str(givennumber)

    # Returns string back with quotation marks.
    def StringSyntax(self, string):
        return '"' + str(string) + '"'

    # Adds string values to the JSON string variable.
    def AddStr(self, givenstring):
        self.var = self.var + self.StringSyntax(givenstring)

    # This method takes a name argument and adds it as the name to the JSON string (self.var).
    def AddName(self, name):
        self.var = self.var + self.StringSyntax(name) + ":"

     # This function handles lists.  
    def List(self, givenlist):
        length = len(givenlist)
        index = 0
        self.var = self.var + "{"
        for i in givenlist:
            if varType(i) == "string":
                self.AddStr(i)
            if varType(i) == "number":
                self.AddNum(i)
            if varType(i) == "list":
                self.List(i)
            if varType(i) == "dictionary":
                self.Dictionary(i)
            index = index + 1
            if index == length:
                self.var = self.var + "}"
            else:
                self.var = self.var + ","

    # This method function handles dictionaries.
    def Dictionary(self, x, name=0):
        if name != 0:
            self.AddName(name)
        self.var = self.var + "{"
        length = len(x)
        index = 0
        for i in x.keys():
            if varType(x[i]) == "string":
                self.AddName(str(i))
                self.AddStr(x[i])
            if varType(x[i]) == "number":
                self.AddName(str(i))
                self.AddNum(x[i])
            if varType(x[i]) == "list":
                self.AddName(str(i))
                self.List(x[i])
            if varType(x[i]) == "dictionary":
                self.AddName(str(i))
                self.Dictionary(x[i], name=str(i))
            index = index + 1
            if index == length:
                self.var = self.var + "}"
            else:
                self.var = self.var + ","

    # Use this method to start converting dictionaries into JSON.
    def Begin(self, x, name=0):
        # The name argument isn't required.
        if name != 0:
            self.Dictionary(x, name)
            return self.var
        else:
            self.Dictionary(x)
            return self.var
