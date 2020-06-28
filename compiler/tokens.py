"""Reads Jack program input and output XML tokenizer"""

# from typing_extensions import Literal
from typing import Literal, Optional
from pydantic import BaseModel, ValidationError, validator

# https://docs.python.org/3/library/xml.etree.elementtree.html
import xml.etree.ElementTree as ET

class Tokenizer:

    token_before = ''
    token_before_before = ''

    "Saves files to write pointer"
    file_to_write = ''

    class Token(BaseModel):
        keyWord: Optional[
            Literal['class', 'method', 'function', 'constructor', 'integer', 'boolean', 'char', 'void', 'var',
                    'static', 'field', 'let', 'do', 'if', 'else', 'while', 'return', 'true', 'false', 'null', 'this']]
        symbol: Optional[
            Literal['{', '}', '(', ')', '[', ']', '.', ',', ';', '+', '-', '*', '/', '&', '|', '<', '>', '=', '~']]
        identifier: Optional[str]
        tokenType: Literal['keyword', 'symbol', 'identifier', 'int_const', 'string_const']

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
            return v

        #  https://pydantic-docs.helpmanual.io/usage/types/#literal-type

        """ Get keyWord field values to run """

        @staticmethod
        def get_keyword():
            for i in Tokenizer.Token.schema()['properties']['keyWord']['anyOf']:
                yield i['const']

        """ Get keyWord field values to run """

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
        print("Line", line)
        todo = line.split(" ")
        if "" in todo:
            todo.remove("")
        to_check = todo.copy()
        for i in range(len(to_check)):
            s = to_check[i]
            last_symbol = to_check[i][-1]
            if s and last_symbol in Tokenizer.Token.get_symbol():
                index = todo.index(s)
                todo.pop(index)
                todo.insert(index, s[:-1])
                todo.insert(index+1, last_symbol)
        if "" in todo:
            todo.remove("")
        print("MY TODO from make_todo_list", todo)
        return todo

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

        return self.get_tokens_list(todo[1:], answ)

    """ Creates string XML from Tokens list """

    def dump_to_xml(self, tokens_list):
        for token in tokens_list:
            if type(token) != Tokenizer.Token:
                raise TypeError("Token expected")
            tag = token.tokenType
            xml = ET.Element(tag)
            if 'keyword' == tag:
                print("FIND ONE KEYWORD")
                xml.text = token.keyWord
            if 'symbol' == tag:
                print("FIND ONE SYMBOL")
                xml.text = token.symbol
            if 'identifier' == tag:
                print("FIND ONE IDEN")
                xml.text = token.identifier
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
        # After class always id
        if answ and answ[-1] and answ[-1].keyWord == 'class':
            print("RETURN WITH TRUE")
            return True
        # Jeigu eilute prasideda var, tai visi tagai nuo trecio yra identifier - jeigu ne symbol
        if answ and answ[0].keyWord == 'var' and len(answ) > 1:
            print("RETURN WITH TRUE from VAR")
            return True
        return False