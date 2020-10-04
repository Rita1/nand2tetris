
class VMWriter:

    file_to_write = ''

    """ Args to call function
        Always store return value to temp """

    def write_call(self, name, nArgs):
        s_to_write = 'call ' + name + ' ' + str(nArgs) + '\n'
        s_to_write = s_to_write + 'pop temp 0' + '\n'
        with open(self.file_to_write, 'a') as fw:
            fw.write(s_to_write)

    """ If return value, function should return 0"""

    def write_return(self, return_value):
        # print("Found void", return_value)
        s_to_write = ''
        if return_value == 'void':
            s_to_write = 'push constant 0' + '\n'
        # if return_value == 'this':
        #     s_to_write = 'push pointer 0' + '\n'
        s_to_write = s_to_write + 'return' + '\n'
        with open(self.file_to_write, 'a') as fw:
            fw.write(s_to_write)

    """ nArgs = Local variables """

    def write_function(self, name, nArgs):
        s_to_write = 'function ' + name + ' ' + str(nArgs) + '\n'
        with open(self.file_to_write, 'a') as fw:
            fw.write(s_to_write)

    def write_push(self, segment, index):
        s_to_write = 'push ' + segment + ' ' + str(index) + '\n'
        with open(self.file_to_write, 'a') as fw:
            fw.write(s_to_write)

    def write_pop(self, segment, index):
        s_to_write = 'pop ' + segment + ' ' + str(index) + '\n'
        with open(self.file_to_write, 'a') as fw:
            fw.write(s_to_write)

    """ add, sub, neg, eq, gt, lt, and, or, not, * """

    def write_arit(self, command):
        s_to_write = ''
        if command == '+' or command == 'add':
            s_to_write = 'add'
        if command == '*':
            s_to_write = 'call Math.multiply 2'
        if command == '/':
            s_to_write = 'call Math.divide 2'
        if command == 'neg':
            s_to_write = 'neg'
        if command == 'not' or command == '~':
            s_to_write = 'not'
        if command == '-':
            s_to_write = 'sub'
        if command == '=':
            s_to_write = 'eq'
        if command == '>':
            s_to_write = 'gt'
        if command == '<':
            s_to_write = 'lt'
        if command == '&':
            s_to_write = 'and'
        if command == 'or' or command == '|':
            s_to_write = 'or'

        s_to_write = s_to_write + '\n'
        with open(self.file_to_write, 'a') as fw:
            fw.write(s_to_write)

    def write_label(self, label):
        s_to_write = 'label ' + label + '\n'
        with open(self.file_to_write, 'a') as fw:
            fw.write(s_to_write)

    def write_if_goto(self, label):
        s_to_write = 'if-goto ' + label + '\n'
        with open(self.file_to_write, 'a') as fw:
            fw.write(s_to_write)

    def write_goto(self, label):
        s_to_write = 'goto ' + label + '\n'
        with open(self.file_to_write, 'a') as fw:
            fw.write(s_to_write)


# Methods are called using
#     method(...), or
#     variable.method(...)
# The first version calls method passing the current object. Think this.method(...), except that Jack doesn't allow access to the this variable.
#
# Functions and constructors are called using
#     ClassName.function(...)
#
# So, if it doesn't have a ".", this is a method call.
# If it has a ".", you need to see if the symbol on the left is a variable. If it is, this is a method call.
# Otherwise, this is function (or constructor) call.