
import xml.etree.ElementTree as ET
from typing import Literal, Optional
from pydantic import BaseModel, ValidationError, validator
import VMWriter as VM

class Compiler:

    tag_generator = ''
    next_tag = ''
    "VMWriter object"
    vm = ''

    subroutine_tags = ('let','do','if','while')
    op_tags = ('+', '-', '*', '/', '&', '|', '<','&lt;','>', '&gt;', '=')
    current_if_tag = ''
    current_args = 0
    current_class_name = ''
    current_return_value = ''
    current_func_name = ''
    current_id = 0

    # List of Symbols objects (class)
    symbol_table = []
    symbol_table_method = []
    no_of_field = 0
    no_of_argument = 0
    no_of_static = 0
    no_of_local = 0

    def __init__(self):
        self.symbol_table = []
        self.current_class_name = ''

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
        self.current_class_name = self.next_tag[1]
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
            # print("Next tag from class var decl end", self.next_tag)
            return xml
        class_var = ET.SubElement(xml, 'classVarDec')
        # List Of Tags
        to_symbol_table = []
        while True:
            to_symbol_table.append(self.next_tag)
            xml = self.generate_tag(xml, class_var)
            if self.next_tag[1] == ';':

                # print("test", self.symbol_table)
                xml = self.generate_tag(xml, class_var)
                self.create_class_symbol_table(to_symbol_table)
                break
        return self.compile_class_var_decl(xml)

    """" Symbolic table

         Consume tag, save symbol table to class symbols list
         name:x, type:int, kind:field,
          no:0 """

    class Symbol(BaseModel):
        name: str
        type: str
        kind: Literal['field', 'static', 'argument', 'local']
        no: int

    """ Method level symbol table method level """
    def create_symbol_table(self, list_of_tags, kind=''):
        print("list of tags", list_of_tags)
        print("kind", kind)
        i = 2
        if kind == 'argument':
            print("start")
            i = 0
            while len(list_of_tags[i:]) > 0:
                type = list_of_tags[i][1]
                name = list_of_tags[i+1][1]
                no = self.no_of_argument
                self.no_of_argument += 1
                symbol = Compiler.Symbol(name=name, type=type, kind=kind, no=no)
                print("symbol", symbol)
                self.symbol_table_method.append(symbol)
                i += 3
            return
        type = list_of_tags[1][1]
        while len(list_of_tags[i:]) > 0:
            name = list_of_tags[i][1]
            no = self.no_of_local
            self.no_of_local += 1
            symbol = Compiler.Symbol(name=name, type=type, kind=kind, no=no)
            self.symbol_table_method.append(symbol)
            i +=2
        # print("symbol table", self.symbol_table)
        return

    def create_class_symbol_table(self, list_of_tags):
        i = 2
        no = 0
        type = list_of_tags[1][1]
        kind = list_of_tags[0][1]
        while len(list_of_tags[i:]) > 0:
            name = list_of_tags[i][1]
            if kind == 'field':
                no = self.no_of_field
                self.no_of_field += 1
            elif kind == 'static':
                no = self.no_of_static
                self.no_of_static += 1
            symbol = Compiler.Symbol(name=name, type=type, kind=kind, no=no)
            self.symbol_table.append(symbol)
            i +=2
        # print("symbol table", self.symbol_table)
        return

    """ Get index and scope in symbol table
        First search in method scope, than in class scope
        Return scope and index """

    def get_index_by_name(self, tag):
        no = 0
        kind = ''
        for s in self.symbol_table_method:
            # print("current s", s, s.kind)
            # Pirmiausia paieskom tarp local lauku
            if s.kind == 'local':
                if s.name == tag:
                    # print(s)
                    no = s.no
                    kind = s.kind
            # Tada tarp argument
            if s.kind == 'argument':
                if s.name == tag:
                    # print(s)
                    no = s.no
                    kind = s.kind
        if not kind:
            for s in self.symbol_table:
                if s.name == tag:
                    no = s.no
                    if s.kind == 'field':
                        kind = 'this'
                    else:
                        kind = 'static'
        # print("kind, no", kind, no)
        return (kind, no)

    def get_type_by_name(self, tag):
        type = ''
        for s in self.symbol_table_method:
            # print("current s", s, s.kind)
            # Pirmiausia paieskom tarp local lauku
            if s.kind == 'local':
                if s.name == tag:
                    type = s.type
            # Tada tarp argument
            if s.kind == 'argument':
                if s.name == tag:
                    type = s.type
        if not type:
            for s in self.symbol_table:
                if s.name == tag:
                    type = s.type
        return type

    """ Subroutine compiler """
    def compile_subroutine(self, xml):
        if self.next_tag[1] == '}':
            return xml
        # print("BEFORE", self.symbol_table_method)
        # Reset symbol table
        self.symbol_table_method = []
        self.no_of_argument = 0
        self.no_of_local = 0
        tags_list = []
        subroutine_dec = ET.SubElement(xml, 'subroutineDec')
        # kiti 4 bus subroutine declaration
        for i in range(4):
            tags_list.append(self.next_tag[1])
            xml = self.generate_tag(xml, subroutine_dec)
        self.current_return_value = tags_list[1]

        if tags_list[0] == 'method':
            print("self.current_args from method", self.no_of_argument)
            self.no_of_argument += 1
            print("Now", self.no_of_argument)
        # print("From subroutine call parameter list", self.next_tag)
        xml = self.compile_parameter_list(xml, subroutine_dec)
        # print("After subroutine call parameter list", self.next_tag)
        # Add )
        self.generate_tag(xml, subroutine_dec)

        # Compile subroutine
        s_body = ET.SubElement(subroutine_dec, 'subroutineBody')

        # Add (
        self.generate_tag(xml, s_body)

        if self.next_tag[1] == 'var':
            # print("var decl from subroutine", self.next_tag)
            xml = self.compile_var_dec(xml, s_body)
            # print("return from var decl from subroutine", self.next_tag)
        self.compile_function_vm(tags_list)
        if tags_list[0] == 'method':
            # Jeigu methodas, pirmas perduotas argumentas bus pointeris, kuri reikia issisaugoti
            self.vm.write_push('argument', 0)
            self.vm.write_pop('pointer', 0)
        # print("Tag list", tags_list)
        if tags_list[0] == 'constructor':
            # print("Found object")
            self.compile_object_vm()

        if self.next_tag[1] != '}':
            statements = ET.SubElement(s_body, 'statements')
            xml = self.compile_statements(xml, statements)
            # print("Come back from statments", self.next_tag)
            # if self.next_tag[1] == ';': # Boza boza
            #     self.next_tag = next(self.tag_generator)
        # Add )
        xml = self.generate_tag(xml, s_body)

        return self.compile_subroutine(xml)

    """ 44 """

    def compile_object_vm(self):
       fields_count = 0
       for s in self.symbol_table:
           if s.kind == 'field':
               fields_count += 1
       self.vm.write_push('constant', fields_count)
       self.vm.write_call('Memory.alloc', 1)
       self.vm.write_push('temp', 0)
       self.vm.write_pop('pointer', 0)
       return

    def compile_function_vm(self, tags_list):

        func_name = self.current_class_name + '.' + tags_list[2]
        self.current_func_name = func_name
        local_var_count = 0
        for s in self.symbol_table_method:
            if s.kind == 'local':
                local_var_count += 1
        self.vm.write_function(func_name, local_var_count)
        return

    """ Subroutine parameter list """
    def compile_parameter_list(self, xml, element):
        # print("FROM PARAMETER LIST")
        parameter_dec = ET.SubElement(element, 'parameterList')
        to_symbol_table = []
        # if self.currenct_funct_type == 'method':
        #     symbol = Compiler.Symbol(name="this", type=self.current_class_name, kind="argument", no=self.no_of_argument)
        #     self.symbol_table_method.append(symbol)
        #     self.no_of_argument += 1
        while True:
            if self.next_tag[1] == ')':
                self.create_symbol_table(to_symbol_table, kind="argument")
                break
            to_symbol_table.append(self.next_tag)
            xml = self.generate_tag(xml, parameter_dec)
        return xml

    def get_label(self, ):

        label = self.current_func_name + '.if.' + str(self.current_id)
        label_0 = label + '.0'
        label_1 = label + '.1'
        # print("Got label from tag", self.next_tag, label_0, label_1)
        return label_0, label_1

    """ Compile statments """

    def compile_statements(self, xml, element):
        # print("From statments start", self.next_tag)
        #OOO if_tag = ''

        if self.next_tag[1] == '}' or self.next_tag[1] == ';':
            return xml
        if self.next_tag[1] == 'let':
            xml = self.compile_let(xml, element)
        if self.next_tag[1] == 'do':
            xml = self.compile_do(xml, element)
        if self.next_tag[1] == 'return':
            xml = self.compile_return(xml, element)

        label_0 = ''
        label_1 = ''

        if self.next_tag[1] == 'if':
            label_0 = self.get_label()[0]
            label_1 = self.get_label()[1]
            # print("Got labels from statments if", label_0, label_1)
            xml = self.compile_if(xml, element)

        if self.next_tag[1] == 'else':

            self.vm.write_goto(label_1)
            self.vm.write_label(label_0)
            # print("Write goto and label from else", "goto", label_1, "label0", label_0,)
            xml = self.compile_if(xml, element, else_st=True)

            self.vm.write_label(label_1)
            # print("Write labels from else 2 ", label_1)

        else:
            if label_0:
                # print("Write label from statment if", label_0)
                self.vm.write_label(label_0)

        if self.next_tag[1] == 'while':
            xml = self.compile_while(xml, element)
        # print("Next tag from end statments", self.next_tag)
        return self.compile_statements(xml, element)

    """ Compile let """
    def compile_let(self, xml, element):
        # print("FROM Let")
        let_statement = ET.SubElement(element, 'letStatement')
        tag_list = []
        while True:
            tag_list.append(self.next_tag)
            xml = self.generate_tag(xml, let_statement)
            if self.next_tag[1] == '[':
                tag_list.append(self.next_tag)
                xml = self.generate_tag(xml, let_statement)
                xml = self.compile_expression(xml, let_statement)
                xml = self.generate_tag(xml, let_statement)
                # push arr ir add
                self.compile_let_array_to_vm(tag_list)
            if self.next_tag[1] == '=':
                xml = self.generate_tag(xml, let_statement)
                xml = self.compile_expression(xml, let_statement)
                xml = self.generate_tag(xml, let_statement)
                self.compile_let_vm(tag_list)
                return xml
            # print("tag from while let", self.next_tag)

        return xml

    """ Array access let arr[expression1] = expression2
    push arr
    push expression1 (VM code)
    add
    push expression2 (VM code)
    pop temp 0
    pop pointer 1
    push temp 0 
    pop that 0 """

    # compile push ARRAY and add - ties 133
    def compile_let_array_to_vm(self, tag_list):
        # print("tag_list from let", tag_list)

        kind, no = self.get_index_by_name(tag_list[1][1])
        self.vm.write_push(kind, no)
        self.vm.write_arit('add')
        # print("kind, no", kind, no)
        return

    def compile_let_vm(self, tag_list):
        # print("compile_let", tag_list)
        # print(tag_list[1][1])
        # reikia patikrinti ar kompiliuojam array
        if tag_list[-1][1] == '[':
            # print("Found array")
            self.vm.write_pop('temp', 0)
            self.vm.write_pop('pointer', 1)
            self.vm.write_push('temp', 0)
            self.vm.write_pop('that', 0)
        else:
            kind, no = self.get_index_by_name(tag_list[1][1])
            self.vm.write_pop(kind, no)
        return

    """ Compile var decl """
    def compile_var_dec(self, xml, element):
        if self.next_tag[1] in self.subroutine_tags or self.next_tag[1] == '}':
            return xml
        var = ET.SubElement(element, 'varDec')
        to_symbol_table = []
        while True:
            to_symbol_table.append(self.next_tag)
            xml = self.generate_tag(xml, var)
            if self.next_tag[1] == ';':
                xml = self.generate_tag(xml, var)
                self.create_symbol_table(to_symbol_table, kind='local')
                break
        return self.compile_var_dec(xml, element)

    """ expression: term (op term)* 
        term: integerConstant | stringConstant | keywordConstant | varName | varName '[' expression ']', 
              | subroutineCall | (expression) | unaryOp term 
        subroutineCall: subroutineName (expressionList) | (className | varName) . subroutineName '(' expressionList ')'
        expressionList (expression (',' expression)* )?
        op: +, -, *, /, &, |, <, >, =
        unaryOp: '-', '~'
        KeywordConstant: 'true' | 'false' | 'null' | 'this' """

    def compile_expression(self, xml, element):
        # print("From Expression", self.next_tag)
        symbol_before = False
        if self.next_tag[1] == ';' or self.next_tag[1] == ')' or self.next_tag[1] == ']':
            return xml
        if self.next_tag[1] == ',':
            # symbol_before = True
            xml = self.generate_tag(xml, element)
            return xml
        expression = ET.SubElement(element, 'expression')
        # print("Starting compile term from expresion", self.next_tag)
        xml = self.compile_term(xml, expression) #AAA
        if self.next_tag[1] == ',':
            symbol_before = True
            # print("KUKU", self.next_tag)
            self.current_args += 1
            # print("args", self.current_args)
            xml = self.generate_tag(xml, element)
        if self.next_tag[1] in self.op_tags:
            # print("Compile tag and term from expresion of op-tags", self.next_tag)
            # print("Symbol before", symbol_before)
            if symbol_before and self.next_tag[1] == '-':
                # print("Started compile term from -", self.next_tag)
                xml = self.compile_term(xml, expression)
                # print("Come back from term and -", self.next_tag)
                return self.compile_expression(xml, element)
            op_tag = self.next_tag[1]
            xml = self.generate_tag(xml, expression)
            xml = self.compile_term(xml, expression)
            self.generate_op_vm(op_tag)
        return self.compile_expression(xml, element)

    """ Gets tag string and returns Term 
        term: integerConstant | stringConstant | keywordConstant | varName | varName [ expression ] | 
        subroutineCall | ( expression ) | unaryOp term """

    def compile_term(self, xml, element):
        # print("From start term", self.next_tag)
        term = ET.SubElement(element, 'term')
        # Check if found urinary symbol
        # print("from compile term", self.next_tag)
        if self.next_tag[1] in ('~', '-'):
            # xml = self.generate_tag(xml, term)
            # return_xml = self.compile_term(xml, term)
            # print("From term urinary", self.next_tag)
            if self.next_tag[1] == '-':
                xml = self.generate_tag(xml, term)
                return_xml = self.compile_term(xml, term)
                self.vm.write_arit('neg')
                return return_xml
            if self.next_tag[1] == '~':
                xml = self.generate_tag(xml, term)
                return_xml = self.compile_term(xml, term)
                # print("WRITE ~")
                self.vm.write_arit('not')
                return return_xml
        # kiek tik nori expression
        if self.next_tag[1] == '(':
            # print("From term ( ", self.next_tag)
            xml = self.generate_tag(xml, term)
            xml = self.compile_expression(xml, term)
        # print("possible tags", self.next_tag)
        # sugris tag'as jeigu nerando symboliu lenteleje, reiskia tai funkcija
        # make_function_name_to_call = ''
        tag_list = []
        # if self.next_tag[0] == 'identifier':
        # # kazkas apie klases funkcija
        #     kind, _ = self.get_index_by_name(self.next_tag[1])
        #     if not kind:
        #         tag_list.append(self.next_tag)
            # Bus metodas jeigu nera tasko arba jeigu indetifier bus field symboliu lentelej
        tag_list.append(self.next_tag)
        self.generate_term_vm()

        xml = self.generate_tag(xml, term)
        if self.next_tag[1] == '[':
            xml = self.generate_tag(xml, term)
            xml = self.compile_expression(xml, term)
            ## Compile Array from Term
            self.vm.write_arit('add')
            self.vm.write_pop('pointer', 1)
            self.vm.write_push('that', 0)
            xml = self.generate_tag(xml, term)
        if self.next_tag[1] == '.': # ????
            # Add .
            # print("Add dot from term", self.next_tag)
            # make_function_name_to_call = make_function_name_to_call + self.next_tag[1]
            tag_list.append(self.next_tag)
            xml = self.generate_tag(xml, term)
            # Add subroutine name
            # print("Add subroutine name", self.next_tag)
            # make_function_name_to_call = make_function_name_to_call + self.next_tag[1]
            tag_list.append(self.next_tag)
            xml = self.generate_tag(xml, term)

            # Add symbol
            xml = self.generate_tag(xml, term)
            # print("From term urinary dot", self.next_tag)
            exp_list = ET.SubElement(term, 'expressionList')
            xml = self.compile_expression_list(xml, exp_list)
            xml = self.generate_tag(xml, term)
            # print("Start write call from term", self.next_tag)
            self.compile_call_vmcode(tag_list)
            # self.vm.write_call(make_function_name_to_call, self.current_args)
            # kadangi iskviesta args reikia nunulinti
            # print("Make current args from terms", self.current_args, "self.next_tag[1]", self.next_tag)
            # self.current_args = 0
            # jeigu visada kvieciamas sitas is let, tada i temp segmenta idedamas 0, jeigu ne tai neveiks ir reikia taisyti
            self.vm.write_push('temp', 0)
            return xml
            # return self.compile_expression_list(xml, term)
        if self.next_tag[0] == 'symbol':
            # print("return from term", self.next_tag)
            return xml
        return self.compile_term(xml, element)

    """ null - constant 0
        false - constant  0
        true - constant -1 """

    def generate_term_vm(self):
        # print("generate term vm", self.next_tag)
        if self.next_tag[0] == 'integerConstant':
            self.vm.write_push('constant', self.next_tag[1])
        if self.next_tag[1] == 'false':
            self.vm.write_push('constant', 0)
        if self.next_tag[1] == 'true':
            self.vm.write_push('constant', 1)
            self.vm.write_arit('neg')
        # push constatnt stringlen + 1
        # call String.new 1
        # push constant ascii value
        # call String.appendChar 2
        if self.next_tag[0] == 'stringConstant':
            str_len = len(self.next_tag[1])
            self.vm.write_push('constant', str_len)
            self.vm.write_call('String.new', 1)
            self.vm.write_push('temp', 0)
            for char in self.next_tag[1]:
                self.vm.write_push('constant', ord(char))
                self.vm.write_call('String.appendChar', 2)
                self.vm.write_push('temp', 0)
                # print(char)
        if self.next_tag[1] == 'this':
            self.vm.write_push('pointer', 0)

        if self.next_tag[0] == 'identifier':
            # print("From Term find kind and index", self.next_tag)
            kind, no = self.get_index_by_name(self.next_tag[1])
            if kind:
                self.vm.write_push(kind, no)
        # print("return false")
        return False

    def generate_op_vm(self, op_tag):
        self.vm.write_arit(op_tag)
        return

    """ do subroutineCall """
    def compile_do(self, xml, element):
        # print("From do", self.next_tag)
        do = ET.SubElement(element, 'doStatement')
        xml = self.generate_tag(xml, do)
        tag_list = []
        found_dot = False
        while True:
            # print("From Do While, self.next_tag",self.next_tag)
            if self.next_tag[1] == ';':
                xml = self.generate_tag(xml, do)
                print("start compile from do", tag_list)
                self.compile_call_vmcode(tag_list)
                break
            if self.next_tag[1] == '(':
                if not found_dot:
                    # tikriausiai 0 ? kadangi pushinam pointeri nes radom metoda +1 prie argumentu
                    self.vm.write_push('pointer', 0)
                # a) var.draw() - var bus field symboliu lenteleje
                if found_dot:
                    kind, no = self.get_index_by_name(tag_list[0][1])
                    if kind:
                        self.vm.write_push(kind, no)
                xml = self.generate_tag(xml, do)
                exp_list = ET.SubElement(do, 'expressionList')
                xml = self.compile_expression_list(xml, exp_list)
            # reikia patikrinti ar metodas, jeigu metodas push;int pointeri
            # a) var.draw() - var bus field symboliu lenteleje
            # b) be taskiuko, tai bus klases metodas
            if self.next_tag[1] == '.':
                found_dot = True
            tag_list.append(self.next_tag)
            xml = self.generate_tag(xml, do)
        return xml

    """ Subroutine Call subroutineName | (className | varName) . subroutineName"""
    def compile_call_vmcode(self, tag_list):
        # print("tag_list from call", tag_list)
        func_name = tag_list[0][1]
        if tag_list[1][1] == '.':
            # kartais gali buti kad gautas tagas yra varName, tada jo reikia paieskoti
            kind, no = self.get_index_by_name(tag_list[0][1])
            if kind:
                self.current_args += 1
                type = self.get_type_by_name(tag_list[0][1])
                func_name = type + '.' + tag_list[2][1]
            else:
                func_name = func_name + tag_list[1][1] + tag_list[2][1]
        else:
            self.current_args += 1
            func_name = self.current_class_name + '.' + tag_list[0][1]
        self.vm.write_call(func_name, self.current_args)
        self.current_args = 0
        # print("Make current args from do", self.current_args, "tag", self.next_tag[1])
        return

    def compile_expression_list(self, xml, element):
        # print("From expression list", self.next_tag)
        if self.next_tag[1] == ')':
            return xml
        self.current_args += 1
        # print("Update current args from exp. list", self.current_args, "tag", self.next_tag[1])
        xml = self.compile_expression(xml, element)
        # print("come back from expreesion list", self.next_tag, self.current_args)
        return self.compile_expression_list(xml, element)

    def compile_return(self, xml, element):
        return_tag = ET.SubElement(element, 'returnStatement')
        xml = self.generate_tag(xml, return_tag)
        if self.next_tag[1] != ';':
            xml = self.compile_expression(xml, return_tag)
        # print("current return value", self.current_return_value)
        # Todo veikia tik klasei ir void
        # jeigu return value lygi klasei, tai bus objekto konstruktorius ir reikia sugrazinti pointeri
        # if self.current_return_value == self.current_class_name:
        #     self.vm.write_push('pointer', 0)
        # print(self.current_return_value)
        # Add return
        self.vm.write_return(self.current_return_value)
        # Add;
        xml = self.generate_tag(xml, return_tag)
        return xml

    """ if(expression)
            statments1
        else
            statments2 
            
        VM code:
        
        compiled(expresion)
        not
        if-goto L0
        compiled (statments1)
        goto L1
        label L0
        compiled (statments2)
        label L1 """

    # exp
    # not
    # if -goto L0
    # comp stm1
    # L0

    def compile_if(self, xml, element, else_st = False):
        # print("From compile if", self.next_tag)
        if_tag = self.current_if_tag
        if self.next_tag[1] == 'if':
            if_tag = ET.SubElement(element, 'ifStatement')
            self.current_if_tag = if_tag
        # print("self.next_tag",self.next_tag)
        label_0 = ''
        if not else_st:

            label_0, _ = self.get_label()
            self.current_id += 1
            # print("got label from main if", label_0)

        while True:
            if self.next_tag[1] == '}':
                break
            xml = self.generate_tag(xml, if_tag)
            if self.next_tag[1] == '(':
                xml = self.generate_tag(xml, if_tag)
                self.compile_expression(xml, if_tag)

                self.vm.write_arit('not')
                self.vm.write_if_goto(label_0)
                # print("write label from if", label_0)
                # Add )
                xml = self.generate_tag(xml, if_tag)
            if self.next_tag[1] == '{':
                # ADD {
                xml = self.generate_tag(xml, if_tag)
                statements = ET.SubElement(if_tag, 'statements')
                self.compile_statements(xml, statements)

                # print("Come back from statments to IF", self.next_tag)
            # print("From While IF statment", self.next_tag)
        # Add }
        xml = self.generate_tag(xml, if_tag)
        return xml

    """ While (expresion) (statments) 
        VM code:
        
        label L1
        compiled (expresion)
        not
        if-goto L2
        compiled (statments)
        goto L1
        label L2
        """

    def compile_while(self, xml, element):
        while_tag = ET.SubElement(element, 'whileStatement')
        xml = self.generate_tag(xml, while_tag)
        label = self.current_func_name + '.while.' + str(self.current_id)
        self.current_id += 1
        label_0 = label + '.0'
        label_1 = label + '.1'
        self.vm.write_label(label_0)
        while True:
            # Add (
            xml = self.generate_tag(xml, while_tag)
            # print("From While to compile expressions", self.next_tag)
            xml = self.compile_expression(xml, while_tag)
            # Add )

            self.vm.write_arit('not')
            self.current_func_name + '.while.' + str(self.current_id) + '.1'
            self.vm.write_if_goto(label_1)

            xml = self.generate_tag(xml, while_tag)
            # ADD {
            xml = self.generate_tag(xml, while_tag)
            statements = ET.SubElement(while_tag, 'statements')
            # print("From While to compile statments", self.next_tag)
            xml = self.compile_statements(xml, statements)
            self.vm.write_goto(label_0)
            self.vm.write_label(label_1)
            # ADD }
            xml = self.generate_tag(xml, while_tag)
            break
        return xml