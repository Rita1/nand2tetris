
import xml.etree.ElementTree as ET

class Compiler:

    tag_generator = ''
    next_tag = ''
    subroutine_tags = ('let','do')

    """ Helper function generate xml element and consume one element"""

    def generate_tag(self, xml, element):
        tag_key = self.next_tag[0]
        key = ET.SubElement(element, tag_key)
        key.text = self.next_tag[1]
        self.next_tag = next(self.tag_generator)
        return xml

    """ Returns Class XML ETree """

    def compile_class(self):

        # Class
        xml = ET.Element('class')
        class_key = ET.SubElement(xml, 'keyword')
        class_key.text = 'class'
        # Consume class
        self.next_tag = next(self.tag_generator)

        # Class Ident
        self.next_tag = next(self.tag_generator)
        self.generate_tag(xml, xml)
        # Class symbol
        self.generate_tag(xml, xml)

        # Check for class var declarations
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
            print("Next tag from class var decl end", self.next_tag)
            return xml
        class_var = ET.SubElement(xml, 'classVarDec')
        while True:
            xml = self.generate_tag(xml, class_var)
            if self.next_tag[1] == ';':
                xml = self.generate_tag(xml, class_var)
                break
        return self.compile_class_var_decl(xml)

    """ Subroutine compiler """
    def compile_subroutine(self, xml):
        if self.next_tag[1] == '}':
            return xml
        subroutine_dec = ET.SubElement(xml, 'subroutineDec')
        # kiti 4 bus subroutine declaration
        for i in range(4):
            xml = self.generate_tag(xml, subroutine_dec)
        print("From subroutine call parameter list", self.next_tag)
        xml = self.compile_parameter_list(xml, subroutine_dec)
        print("After subroutine call parameter list", self.next_tag)
        # Add )
        self.generate_tag(xml, subroutine_dec)

        # Compile subroutine
        s_body = ET.SubElement(subroutine_dec, 'subroutineBody')

        # Add (
        self.generate_tag(xml, s_body)

        if self.next_tag[1] == 'var':
            print("var decl from subroutine", self.next_tag)
            xml = self.compile_var_dec(xml, s_body)
        if self.next_tag[1] != '}':
            statements = ET.SubElement(s_body, 'statements')
            xml = self.compile_statements(xml, statements)
            print("Come back from statments", self.next_tag)
            # if self.next_tag[1] == ';': # Boza boza
            #     self.next_tag = next(self.tag_generator)
        # Add )
        xml = self.generate_tag(xml, s_body)

        return self.compile_subroutine(xml)

    """ Subroutine parameter list """
    def compile_parameter_list(self, xml, element):
        print("FROM PARAMETER LIST")
        parameter_dec = ET.SubElement(element, 'parameterList')
        while True:
            if self.next_tag[1] == ')':
                break
            xml = self.generate_tag(xml, parameter_dec)
        return xml

    """ Compile statments """

    def compile_statements(self, xml, element):
        print("From statments")
        if self.next_tag[1] == '}' or self.next_tag[1] == ';':
            return xml
        if self.next_tag[1] == 'let':
            xml = self.compile_let(xml, element)
        if self.next_tag[1] == 'do':
            xml = self.compile_do(xml, element)
        if self.next_tag[1] == 'return':
            xml = self.compile_return(xml, element)
        if self.next_tag[1] == 'if':
            xml = self.compile_if(xml, element)
        # self.next_tag = next(self.tag_generator)
        print("Next tag from statments", self.next_tag)
        return self.compile_statements(xml, element)

    """ Compile let """
    def compile_let(self, xml, element):
        print("FROM Let")
        let_statement = ET.SubElement(element, 'letStatement')
        print("current tag", self.next_tag)
        while True:
            xml = self.generate_tag(xml, let_statement)
            if self.next_tag[1] == '=':
                xml = self.generate_tag(xml, let_statement)
                xml = self.compile_expression(xml, let_statement)

                xml = self.generate_tag(xml, let_statement)
                return xml
            print("tag from while let", self.next_tag)
        return xml

    """ Compile var decl """
    def compile_var_dec(self, xml, element):
        if self.next_tag[1] in self.subroutine_tags or self.next_tag[1] == '}':
            return xml
        var = ET.SubElement(element, 'varDec')
        while True:
            xml = self.generate_tag(xml, var)
            if self.next_tag[1] == ';':
                xml = self.generate_tag(xml, var)
                break
        return self.compile_var_dec(xml, element)

    def compile_expression(self, xml, element):
        print("From Expression", self.next_tag)
        if self.next_tag[1] == ';' or self.next_tag[1] == ')':
            return xml
        expression = ET.SubElement(element, 'expression')
        xml = self.compile_term(xml, expression)
        if self.next_tag[1] == ',':
            xml = self.generate_tag(xml, element)

        return self.compile_expression(xml, element)

    """ Gets tag string and returns Term """
    def compile_term(self, xml, element):
        print("From term", self.next_tag)
        if self.next_tag[1] == ';' or self.next_tag[1] == ')' or self.next_tag[1] == ',':
            return xml
        term = ET.SubElement(element, 'term')
        xml = self.generate_tag(xml, term)
        return self.compile_term(xml, element)

    def compile_do(self, xml, element):
        print("From do", self.next_tag)
        do = ET.SubElement(element, 'doStatement')
        while True:
            print("From Do While, self.next_tag",self.next_tag)
            if self.next_tag[1] == ';':
                xml = self.generate_tag(xml, do)
                break
            if self.next_tag[1] == '(':
                xml = self.generate_tag(xml, do)
                exp_list = ET.SubElement(do, 'expressionList')
                xml = self.compile_expression_list(xml, exp_list)
            xml = self.generate_tag(xml, do)
        return xml

    def compile_expression_list(self, xml, element):
        print("From expression list", self.next_tag)
        if self.next_tag[1] == ')':
            return xml
        xml = self.compile_expression(xml, element)
        return self.compile_expression_list(xml, element)

    def compile_return(self, xml, element):
        return_tag = ET.SubElement(element, 'returnStatement')
        # Add return
        xml = self.generate_tag(xml, return_tag)
        if self.next_tag[1] != ';':
            xml = self.generate_tag(xml, return_tag)
        # Add ;
        xml = self.generate_tag(xml, return_tag)
        return xml

    def compile_if(self, xml, element):
        print("From compile if", self.next_tag)
        if_tag = ET.SubElement(element, 'ifStatement')
        while True:
            if self.next_tag[1] == '}':
                break

            tag_key = self.next_tag[0]
            key = ET.SubElement(if_tag, tag_key)
            key.text = self.next_tag[1]
            if self.next_tag[1] == '(':

                self.next_tag = next(self.tag_generator)
                self.compile_expression(xml, if_tag)
                # Add )
                tag_key = self.next_tag[0]
                key = ET.SubElement(if_tag, tag_key)
                key.text = self.next_tag[1]
            if self.next_tag[1] == '{':
                # ADD {
                tag_key = self.next_tag[0]
                key = ET.SubElement(if_tag, tag_key)
                key.text = self.next_tag[1]
                self.next_tag = next(self.tag_generator)

                self.compile_statements(xml, if_tag)
                print("Come back from statments to IF", self.next_tag)
            print("From While IF statment", self.next_tag)
            tag_key = self.next_tag[0]
            key = ET.SubElement(if_tag, tag_key)
            key.text = self.next_tag[1]
            self.next_tag = next(self.tag_generator)

        # Add }
        tag_key = self.next_tag[0]
        key = ET.SubElement(if_tag, tag_key)
        key.text = self.next_tag[1]
        self.next_tag = next(self.tag_generator)
        return xml
