
import xml.etree.ElementTree as ET

class Compiler:

    tag_generator = ''
    next_tag = ''

    """ Returns Class XML ETree """

    def compile_class(self):

        # Class
        xml = ET.Element('class')
        class_key = ET.SubElement(xml, 'keyword')
        class_key.text = 'class'

        # Consume class
        next(self.tag_generator)

        # Class Ident
        class_ident = ET.SubElement(xml, 'identifier')
        class_ident.text = next(self.tag_generator)[1]

        # Class symbol
        next(self.tag_generator)
        class_symbol = ET.SubElement(xml, 'symbol')
        class_symbol.text = '{'

        # Check for class var declarations
        self.next_tag = next(self.tag_generator)
        if self.next_tag[1] == 'field' or self.next_tag[1] == 'static':
            xml = self.compile_class_var_decl(xml)
        # Check for subroutines
        # self.next_tag = next(self.tag_generator)
        if self.next_tag[1] in ('constructor', 'function', 'method'):
            xml = self.compile_subroutine(xml)

        # End
        class_symbol1 = ET.SubElement(xml, 'symbol')
        class_symbol1.text = '}'
        return xml

    """ Class var declaration compiler """

    def compile_class_var_decl(self, xml):
        if self.next_tag[1] == '}' or self.next_tag[1] in ('constructor', 'function', 'method'):
            print("Next tag from end", self.next_tag)
            return xml
        class_var = ET.SubElement(xml, 'classVarDec')
        while True:
            tag_key = self.next_tag[0]
            key = ET.SubElement(class_var, tag_key)
            key.text = self.next_tag[1]
            if self.next_tag[1] == ';':
                break
            self.next_tag = next(self.tag_generator)
        self.next_tag = next(self.tag_generator)
        return self.compile_class_var_decl(xml)

    """ Subroutine compiler """
    def compile_subroutine(self, xml):
        if self.next_tag[1] == '}':
            return xml
        subroutine_dec = ET.SubElement(xml, 'subroutineDec')
        # kiti 4 bus subroutine declaration
        for i in range(4):
            tag_key = self.next_tag[0]
            key = ET.SubElement(subroutine_dec, tag_key)
            key.text = self.next_tag[1]
            self.next_tag = next(self.tag_generator)
        xml = self.compile_parameter_list(xml, subroutine_dec)
        # Add )
        symbol = self.next_tag[0]
        s_key = ET.SubElement(subroutine_dec, symbol)
        s_key.text = self.next_tag[1]
        self.next_tag = next(self.tag_generator)

        # Compile subroutine
        s_body = ET.SubElement(subroutine_dec, 'subroutineBody')

        # Add (
        symbol = self.next_tag[0]
        s_key = ET.SubElement(s_body, symbol)
        s_key.text = self.next_tag[1]
        self.next_tag = next(self.tag_generator)
        if self.next_tag[1] == 'var':
            xml = self.compile_var_dec(xml, s_body)
        elif self.next_tag[1] != '}':
            statments = ET.SubElement(s_body, 'statements')
            xml = self.compile_statments(xml, statments)
        # Add )
        symbol = self.next_tag[0]
        s_key = ET.SubElement(s_body, symbol)
        s_key.text = self.next_tag[1]
        self.next_tag = next(self.tag_generator)

        # xml = self.compile_subroutine_body(xml)
        # self.next_tag = next(self.tag_generator)
        return self.compile_subroutine(xml)

    """ Subroutine parameter list """
    def compile_parameter_list(self, xml, element):
        print("FROM PARAMETER LIST")
        parameter_dec = ET.SubElement(element, 'parameterList')
        while True:
            if self.next_tag[1] == ')':
                break
            tag_key = self.next_tag[0]
            key = ET.SubElement(parameter_dec, tag_key)
            key.text = self.next_tag[1]
            self.next_tag = next(self.tag_generator)
        return xml

    """ Compile statments """

    def compile_statments(self, xml, element):
        print("From statments")
        if self.next_tag[1] == '}':
            return xml
        if self.next_tag[1] == 'let':
            xml = self.compile_let(xml, element)
        print("Next tag from statments", self.next_tag)
        self.next_tag = next(self.tag_generator)
        return self.compile_statments(xml, element)

    """ Compile let """
    def compile_let(self, xml, element):
        print("FROM Let")
        let_statement = ET.SubElement(element, 'letStatement')
        print("current tag", self.next_tag)
        while True:
            tag_key = self.next_tag[0]
            key = ET.SubElement(let_statement, tag_key)
            key.text = self.next_tag[1]
            if self.next_tag[1] == '=':
                self.next_tag = next(self.tag_generator)
                xml = self.compile_expression(xml, let_statement)
                # Add last symbol

                tag_key = self.next_tag[0]
                key = ET.SubElement(let_statement, tag_key)
                key.text = self.next_tag[1]
                # self.next_tag = next(self.tag_generator)
                return xml
            self.next_tag = next(self.tag_generator)
            print("taf from while let", self.next_tag)
        return xml

    """ Compile var decl """
    def compile_var_dec(self, xml, element):
        return xml

    def compile_expression(self, xml, element):
        print("From Expression")
        if self.next_tag[1] == ';':
            return xml
        expression = ET.SubElement(element, 'expression')
        xml = self.compile_term(xml, expression)
        # self.next_tag = next(self.tag_generator)
        return self.compile_expression(xml, element)

    """ Gets tag string and returns Var object """
    def compile_term(self, xml, element):
        print("From term")
        if self.next_tag[1] == ';':
            return xml
        term = ET.SubElement(element, 'term')
        tag_key = self.next_tag[0]
        key = ET.SubElement(term, tag_key)
        key.text = self.next_tag[1]

        self.next_tag = next(self.tag_generator)
        return self.compile_term(xml, element)
