"""Reads Jack program input and output XML tokenizer"""

# from typing_extensions import Literal
from typing import Literal, Optional
from pydantic import BaseModel, ValidationError, validator

# https://docs.python.org/3/library/xml.etree.elementtree.html
import xml.etree.ElementTree as ET

class Tokenizer:

    "Saves files to write pointer"
    file_to_write = ''

    "Checks if now parsing comment"
    is_comment = -1

    class Token(BaseModel):
        keyWord: Optional[
            Literal['class', 'method', 'function', 'constructor', 'int', 'boolean', 'char', 'void', 'var',
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

        todo = self.make_todo_list(line)

        tokens_list = self.get_tokens_list(todo, [])
        self.dump_to_xml(tokens_list)
        return tokens_list

    """ Generate todo list from string 
        Gets string renturns list of string"""

    def make_todo_list(self, line):
        # print("Line", line)
        todo = []
        line = self.split_by_string(line, [])
        for l in line:
            if l and l[0] != '"':
                new_list = l.split()
                todo.extend(new_list)
            else:
                todo.append(l)
        if "" in todo:
            todo.remove("")
        todo = self.split_by_symbol(todo, [])
        if "" in todo:
            todo.remove("")
        return todo

    """" Split given list by symbols
         List of string, returns list of string"""

    def split_by_symbol(self, todo, answ):
        if not todo:
            return answ
        coord = self.symbol_coord(todo[0])
        if coord > -1:
            if coord > 0:
                first_line = todo[0][:coord]
                answ.append(first_line)
            midle_line = todo[0][coord]
            answ.append(midle_line)
            rem_line = todo[0][coord+1:]
            return self.split_by_symbol([rem_line] + todo[1:], answ)
        else:
            if todo[0]:
                answ.append(todo[0])
            return self.split_by_symbol(todo[1:], answ)



    def symbol_coord(self, line):
        coord = -1
        find_coord = []
        if line and line[0] == '"':
            return coord
        for s in Tokenizer.Token.get_symbol():
            coord = line.find(s)
            if coord >= 0:
                find_coord.append(coord)
        if find_coord:
            coord = min(find_coord)
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
    def is_symbol(i):
        if i and i[0] == '"' or len(i) == 1:
            return False
        else:
            for s in Tokenizer.Token.get_symbol():
                if i.find(s) >= 0:
                    return True


    """ Get tokens list from string list
        Gets todo list, returns Tokens list """

    def get_tokens_list(self, todo, answ):

        if not todo:
            return answ
        if todo[0] in Tokenizer.Token.get_symbol():
            t = Tokenizer.Token(tokenType='symbol', symbol=todo[0])
            answ.append(t)
        elif todo[0] in Tokenizer.Token.get_keyword():
            t = Tokenizer.Token(tokenType='keyword', keyWord=todo[0])
            answ.append(t)
        elif todo[0].isdigit():
            t = Tokenizer.Token(tokenType='integerConstant', integerConstant=int(todo[0]))
            answ.append(t)
        elif todo[0][0] == '"':
            s = todo[0][1:-1]
            t = Tokenizer.Token(tokenType='stringConstant',stringConstant=s)
            answ.append(t)
        else:
            t = Tokenizer.Token(tokenType='identifier', identifier=todo[0])
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
            # text = self.change_symbols(text)
            xml.text = str(text)

            xml_str = ET.tostring(xml, encoding='unicode')
            if self.file_to_write: #hack for unit testing
                self.file_to_write.write(xml_str)
        return

    """
    Removes comments and spaces: // 
                    /* ... */
                    /** ... */
    Gets string, returns string

    """

    def remove_comments(self, line):

        rem_line = ''
        # - jeigu vis dar tesiasi komentaras tai trinti lauk iki komentaro galo
        if self.is_comment != -1:
            comment_end = line.find('*/')
            if comment_end == -1:
                return ""
            else:
                line = line[comment_end+2:]
            self.is_comment = -1
            return line.strip()
        # - rasti komentaru pradzia ir issisaugoti
        if line.find('/*') >= 0:
            self.is_comment = line.find('/*')
            rem_line = line[self.is_comment:]
            line = line[:self.is_comment]

        elif line.find('/**') >= 0:
            self.is_comment = line.find('/**')
            line = line[:self.is_comment]
        elif line.find("//") >= 0:
            line = line[:line.find("//")]
        if rem_line.find("*/") > -1:
            self.is_comment = -1
        line = line.strip()

        return line
