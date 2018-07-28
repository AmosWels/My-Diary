"""validation class with regular expressions"""
import re


class Validate():
    """valiation class for diary inputs"""
    def __init__(self, name,purpose,):
        self.name = name
        self.purpose = purpose

    def validate_entry(self):
        """method to validate my input """
        result = ""
        if(not re.search("[a-zA-Z0-9]", self.name) or not
                re.search("[a-zA-Z0-9]", self.purpose)):
            result = "INCORRECT INPUT OR EMPTY INPUT. NAME AND PURPOSE SHOULD BE PROVIDED!"
        else:
            result = True
        return result