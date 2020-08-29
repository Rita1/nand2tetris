
class VMWriter:

    file_to_write = ''

    def write_call(self, name, nArgs):
        s_to_write = 'call ' + name + ' ' + str(nArgs) + '\n'
        with open(self.file_to_write, 'a') as fw:
            fw.write(s_to_write)