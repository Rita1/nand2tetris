
class VMWriter:

    file_to_write = ''
    index = 0

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

    def write_arit(self, command):
        s_to_write = ''
        if command == '+':
            s_to_write = 'add' + '\n'
        if command == '*':
            s_to_write = 'call Math.multiply 2' + '\n'
        if command == 'neg':
            s_to_write = 'neg' + '\n'
        with open(self.file_to_write, 'a') as fw:
            fw.write(s_to_write)

    def write_label(self, label):
        s_to_write = 'label ' + label + '.' + self.index + '\n'
        index += 1
        with open(self.file_to_write, 'a') as fw:
            fw.write(s_to_write)
