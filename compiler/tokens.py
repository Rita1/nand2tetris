"""Reads Jack program input and output XML tokenizer"""

# from typing_extensions import Literal
from typing import Literal, Optional
from pydantic import BaseModel, ValidationError, validator

# https://docs.python.org/3/library/xml.etree.elementtree.html
import xml.etree.ElementTree as ET

class Tokenizer:
    token_before = ''

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
        Gets Token obj. returns string """

    @staticmethod
    def get_xml(token):
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
        return ET.tostring(xml, encoding='unicode')

    """
    Create Tokens XML
    Takes string, pointer to write file, writes XML tag
    """

    def get_token(self, line, write_file):

        check_line = line.split(" ")
        print("Check_line", check_line)
        for s in check_line:
            t = ''
            if self.check_if_needs_identifier():
                t = Tokenizer.Token(tokenType='identifier', identifier=s)
            elif s in Tokenizer.Token.get_keyword():
                t = Tokenizer.Token(tokenType='keyword', keyWord=s)
            elif s in Tokenizer.Token.get_symbol():
                t = Tokenizer.Token(tokenType='symbol', symbol=s)
            print("Brand new Token", t)
            Tokenizer.token_before = t
            xml = Tokenizer.get_xml(t)
            write_file.write(xml)
        return line

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

    def check_if_needs_identifier(self):
        # print("My token before", self.token_before)
        if self.token_before:
            if self.token_before.keyWord == 'class':
                return True
        return False