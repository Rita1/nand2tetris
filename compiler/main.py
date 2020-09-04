
import sys
import os

import xml.etree.ElementTree as ET

# https://docs.python.org/3/library/xml.etree.elementtree.html
import tokens as T
import xml_helper as XML_H
import compile_jack as C
import VMWriter

PATH = "/tests/files/"

class Main():

    """ 
    Path to Virtual machine .jack file to parse or directory
    Return .xml file
    """

    def main(self, to_parse):

        # Files to parse consists of file path to parse and file name to write
        files_to_parse = []
        # print("to_parse", to_parse, to_parse[-4:])
        # If file
        if to_parse[-4:] == "jack":

            for_parsing = self.get_files(to_parse)
            files_to_parse.append(for_parsing)

        # If directory
        else:
            get_path = self.get_file_path(to_parse)[1]
            to_check = os.listdir(get_path)
            for f in to_check:
                if f[-4:] == "jack":
                    new_p = to_parse + "/" + f
                    for_parsing = self.get_files(new_p)
                    files_to_parse.append(for_parsing)

        for f in files_to_parse:

            # reset server for unit tests
            self.reset(f[1], f[2], f[3])
            # print("current f", f)
            #
            try:
                t = T.Tokenizer()
                # Read
                with open(f[0]) as f1:
                    with open(f[2], 'a') as fw:
                    # Write Tokens file
                        T.Tokenizer.file_to_write = fw
                        for line in f1:
                            ln = t.remove_comments(line)
                            if ln:
                                t.make_tokens(ln)
                        # END
                        def end():
                            return "</tokens>"
                        fw.write(end())


                vm = VMWriter.VMWriter()
                vm.file_to_write = f[3]
                c = C.Compiler()
                c.vm = vm
                # Write compiled code
                with open(f[1], 'a') as fw:
                    c.tag_generator = XML_H.XMLHelper.read_xml_tags(f[2])
                    xml = c.compile_class()
                    xml_str = ET.tostring(xml, encoding='unicode', short_empty_elements=False)
                    fw.write(xml_str)
            except IOError:
                print("File or directory is missing")
            # return c

    """ 
    Return path's to files or directories
    If file, return full file path to open and directory to file
        First check in testing dir, if not in working dir
    if directory, only full dir path

    """

    def get_file_path(self, file_to_parse):
        
        path = ''
        file_to_open = ''
        # If file:
        if file_to_parse[-4:] == "jack" or file_to_parse[-3:] == "xml" or file_to_parse[-2:] == 'vm':
            # 1. Path in testing dir
            path = os.getcwd() + PATH
            file_to_open = os.getcwd() + PATH + file_to_parse
            file_to_open_w = os.getcwd() + '/' + file_to_parse
            # 2. File is in working dir
            # print("file_to_parse, exits?", file_to_parse, os.path.exists(file_to_open_w), os.getcwd())
            if file_to_parse and os.path.exists(file_to_open_w):
                file_to_open = file_to_open_w
                path = os.getcwd() + '/'
        # If directory
        else:
            # First try in testing dir
            path = os.getcwd() + PATH + file_to_parse
        return file_to_open, path


    """
    Generate 3 files paths for future: file_name.jack file, file_nameT.xml file for tokens and file_name.xml for compiled code
    
    Gets file to parse, returns list of 3 files
    """

    def get_files(self, to_parse):
        file_list = []
        file_to_open = self.get_file_path(to_parse)[0]
        to_tokens = to_parse[:-5] + "T.xml"
        file_tokens = self.get_file_path(to_tokens)[0]
        to_write = to_parse[:-4] + "xml"
        file_to_write = self.get_file_path(to_write)[0]
        to_write_vm = to_parse[:-4] + "vm"
        file_to_write_vm = self.get_file_path(to_write_vm)[0]
        file_list.append(file_to_open)
        file_list.append(file_to_write)
        file_list.append(file_tokens)
        file_list.append(file_to_write_vm)
        return file_list

    """
    Reset script - delete old files, add <Token> tags
    """

    @staticmethod
    def reset(file_to_write, file_to_write_tokens, file_to_write_vm):

        # remove old file
        if os.path.exists(file_to_write):
            os.remove(file_to_write)

        if os.path.exists(file_to_write_tokens):
            os.remove(file_to_write_tokens)

        if os.path.exists(file_to_write_vm):
            os.remove(file_to_write_vm)

        # Open File to write open tag
        with open(file_to_write_tokens, 'a+') as fw:
            code = "<tokens>"
            fw.write(code)
