
import xml.etree.ElementTree as ET

class Compiler:

    tag_generator = ''

    """ Returns Class XML ETree """

    def compile_class(self):
        # Consume tag return class

        xml = ET.Element('class')
        class_key = ET.SubElement(xml, 'keyword')
        class_key.text = 'class'
        class_ident = ET.SubElement(xml, 'identifier')

        # 6 is eiles visada bus identifier
        next_tag = ''
        for i in range(6):
            next_tag = next(self.tag_generator)
        class_ident.text = next_tag
        # visada simbolis uzima 4 reiksmes
        for i in range(4):
            next(self.tag_generator)
        class_symbol = ET.SubElement(xml, 'symbol')
        class_symbol.text = '{'

        # Check for class var declarations
        next(self.tag_generator)
        next_tag = next(self.tag_generator)
        if next_tag == 'field' or next_tag == 'static':
            print("FROM FIELD")
            xml = self.compile_class_var_decl(xml)
        print("Next tag", next_tag)
        # Check for subroutines
        # End
        class_symbol1 = ET.SubElement(xml, 'symbol')
        class_symbol1.text = '}'
        return xml

    """ Class var declaration compiler """

    def compile_class_var_decl(self, xml):
        next(self.tag_generator)
        next_tag = next(self.tag_generator)
        if next_tag == '}' or next_tag in ('constructor', 'function', 'method'):
            print("Next tag from end", next_tag)
            return xml
        class_var = ET.SubElement(xml, 'classVarDec')
        ET.SubElement(xml, 'classVarDec')
        print("Next tag from declaration", next_tag)
        # for tag in next(self.tag_generator):
        #     if tag == ''
        print("Next tag", next_tag)
        return self.compile_class_var_decl(xml)

    """ Gets tag string and returns Var object """
    def compile_term(self, tag):
        return
