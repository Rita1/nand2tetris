"""Reads Jack program input and output XML tokenizer"""

# from typing_extensions import Literal
from typing import Literal, Optional
from pydantic import BaseModel, ValidationError, validator

# https://docs.python.org/3/library/xml.etree.elementtree.html
import xml.etree.ElementTree as ET

class Tokenizer:

    "Saves files to write pointer"
    file_to_write = ''

    class Token(BaseModel):
        keyWord: Optional[
            Literal['class', 'method', 'function', 'constructor', 'integer', 'boolean', 'char', 'void', 'var',
                    'static', 'field', 'let', 'do', 'if', 'else', 'while', 'return', 'true', 'false', 'null', 'this']]
        symbol: Optional[
            Literal['{', '}', '(', ')', '[', ']', '.', ',', ';', '+', '-', '*', '/', '&', '|', '<', '>', '=', '~']]
        identifier: Optional[str]
        integerConstant: Optional[int]
        stringConstant: Optional[str]
        tokenType: Literal['keyword', 'symbol', 'identifier', 'integerConstant', 'stringConstant']

        @validator('tokenType')
        def validate_keyword(cls, v, values):
            if 'keyword' in v:
                if not values['keyWord']:
                    raise ValueError('keyWord is none')
            if 'symbol' in v:
                if not values['symbol']:
                    raise ValueError('Symbol is none')
            if 'identifier' in v:
                if not type(values['identifier']) == str:
                    raise ValueError('String type for identifier required')
            if 'integerConstant' in v:
                if not type(values['integerConstant']) == int:
                    raise ValueError('Integer type for int constant required')
            if 'stringConstant' in v:
                if not values['stringConstant'] or not type(values['stringConstant']) == str:
                    raise ValueError('String type for int constant required')
            return v

        #  https://pydantic-docs.helpmanual.io/usage/types/#literal-type

        """ Get keyWord field values to run """

        @staticmethod
        def get_keyword():
            for i in Tokenizer.Token.schema()['properties']['keyWord']['anyOf']:
                yield i['const']

        """ Get Symbol field values to run """

        @staticmethod
        def get_symbol():
            for i in Tokenizer.Token.schema()['properties']['symbol']['anyOf']:
                yield i['const']

    """ Generate XML string
        Gets Token obj. list returns XML string """



    """
    Create Tokens XML
    Takes string, pointer to write file, writes XML tag
    """

    def make_tokens(self, line):

        print("Check_line", line)
        todo = self.make_todo_list(line)

        tokens_list = self.get_tokens_list(todo, [])
        print("Tokens list", tokens_list)
        self.dump_to_xml(tokens_list)
        return tokens_list

    """ Generate todo list from string 
        Gets string renturns list of string"""

    def make_todo_list(self, line):
        # print("Line", line)
        todo = []
        line = self.split_by_string(line, [])
        print("split_by_string", line)
        for l in line:
            if l and l[0] != '"':
                new_list = l.split()
                todo.extend(new_list)
            else:
                todo.append(l)
        print("after spaces", todo)
        if "" in todo:
            todo.remove("")
        todo = self.split_by_symbol(todo)
        if "" in todo:
            todo.remove("")
        print("MY TODO from make_todo_list", todo)
        return todo

    """" Split given list by symbols
         List of string, returns list of string"""

    def split_by_symbol(self, todo):
        print("START todo", todo)
        while self.is_symbol(todo):
            for i in range(len(todo)):
                line = todo[i]
                last_symbol = ''
                if len(line) > 1:
                    last_symbol = line[-1]
                found_one = self.found_one_symbol(line)
                if len(line) > 1 and found_one >= 0 and last_symbol != '"':
                    todo.pop(i)
                    if line[:found_one]:
                        todo.insert(i, line[:found_one])
                        todo.insert(i+1, line[found_one])
                        if line[found_one+1:]:
                            todo.insert(i+2, line[found_one+1:])
        return todo

    def found_one_symbol(self, line):
        coord = -1
        for s in Tokenizer.Token.get_symbol():
            coord = line.find(s)
            if coord >= 0:
                return coord
        return coord

    """ Extracts string from given string
        Get string, empty list, returns string list
        Exmpl." let length = Keyboard.readInt("HOW MANY NUMBERS? ");
                ['let length = Keyboard.readInt("','HOW MANY NUMBERS? ',');' ]"""

    def split_by_string(self, line, answ):
        if not self.is_string(line):
            answ.append(line)
            return answ
        start, end = self.string_coord(line)
        first_s = line[:start]
        midle_s = line[start:end+1]
        end_s = line[end+1:]
        answ.append(first_s)
        answ.append(midle_s)
        # answ.append(end_s)
        return self.split_by_string(end_s, answ)
        #
        # print(start, end)

        # print("FIRST", first_s, "+Midle", midle_s, "+END", end_s)
        # print("line", line, answ)
        # return answ

    """ Gets string, checks if not extracted string is in line
        If " and " is not first and second, where is string 
        There is NO cases as: ["Test1", " String""] and [""String ", "Test1"] 
        Expl: ["("HOW MANY NUMBERS? ");"], True """

    @staticmethod
    def is_string(line):
        if line and (line.find('"', 1) != -1):
            if line.find('"', len(line)-1) >= 0:
                return False
            return True
        return False

    """" Gets string coordinates x and y 
         Gets list of string, returns first string first and last symbol"""

    @staticmethod
    def string_coord(line):
        start = -1
        end = -1
        if line and line.find('"') > 0:
            start = line.find('"')
            end = line.find('"', start+1)
            return (start, end)
        return (start, end)
    
    """ Returns True if is symbol in line """
    
    @staticmethod
    def is_symbol(todo):
        found = False
        if todo:
            for i in todo:
                if i and i[0] == '"' or len(i) == 1:
                    found = False
                else:
                    for s in Tokenizer.Token.get_symbol():
                        if i.find(s) >= 0:
                            return True
        return found


    """ Get tokens list from string list
        Gets todo list, returns Tokens list """

    def get_tokens_list(self, todo, answ):

        if not todo:
            return answ
        print("GOT TODO", todo, todo[0])
        if todo[0] in Tokenizer.Token.get_symbol():
            t = Tokenizer.Token(tokenType='symbol', symbol=todo[0])
            answ.append(t)
        elif todo[0] == "int":
            t = Tokenizer.Token(tokenType='keyword', keyWord='integer')
            answ.append(t)
        elif self.check_identifier(todo, answ, todo[0]):
            t = Tokenizer.Token(tokenType='identifier', identifier=todo[0])
            answ.append(t)
        elif todo[0] in Tokenizer.Token.get_keyword():
            t = Tokenizer.Token(tokenType='keyword', keyWord=todo[0])
            answ.append(t)
        elif todo[0].isdigit():
            t = Tokenizer.Token(tokenType='integerConstant', integerConstant=int(todo[0]))
            answ.append(t)
        return self.get_tokens_list(todo[1:], answ)

    """ Creates string XML from Tokens list """

    def dump_to_xml(self, tokens_list):
        for token in tokens_list:
            if type(token) != Tokenizer.Token:
                raise TypeError("Token expected")
            tag = token.tokenType
            xml = ET.Element(tag)

            # TokenType nereikia
            tag_dict = token.dict(exclude_none=True)
            del tag_dict['tokenType']

            #Likes vienas laukas bus tekstas
            text = tag_dict[next(iter(tag_dict))]
            xml.text = text

            xml_str = ET.tostring(xml, encoding='unicode')
            if self.file_to_write: #hack for unit testing
                self.file_to_write.write(xml_str)
        return

    """
    Removes comments and spaces: // 
                    /* ... */
                    /** ... */
    Gets string, returns string

    TODO
    """

    @staticmethod
    def remove_comments(line):

        line = line.split("//")[0]
        line = line.split("/*")[0]
        line = line.split("/**")[0]
        line = line.strip()
        return line

    """
    Change symbols to XML allowed symbols
    From < - &lt
         > - &gt
         & - &amp

    TODO
    """

    def change_symbols(self, s):

        return s

    """ Returns True, if string is identifier 
        Gets strings todo list, answ Tokens list, current string """

    def check_identifier(self, todo, answ, current_s):
        # print("My token before", self.token_before)
        print("todo, answ, current_s", todo, answ, current_s)
        # After class and let always id
        if answ and answ[-1] and (answ[-1].keyWord == 'class' or answ[-1].keyWord == 'let'):
            print("RETURN WITH TRUE")
            return True
        # Jeigu eilute prasideda var, tai visi tagai nuo trecio yra identifier
        #                           antras tagas arba keyword, arba identifier
        if answ and answ[0].keyWord == 'var':
            if len(answ) > 1:
                print("RETURN WITH TRUE from VAR")
                return True
            if len(answ) == 1 and current_s not in Tokenizer.Token.get_keyword():
                return True
        # Jeigu eilute prasideda var, tai vis
        # jeigu  eilute prasideda function, tai trecias bus identifier
        if answ and answ[0].keyWord == 'function' and len(answ) == 2:
            print("RETURN TRUE FROM FUNCTION")
            return True
        return False
