import os
from os import path

class XMLHelper():
# veikia tik UTF-8 XML'ams

    @staticmethod
    def xml_tag(file_name):

        between = False # arba reiksme tarp tag'u
        found = False   # arba tag'as
        with open(file_name, 'r') as f:
            while True: # kol nesibaige failas
                tag = ""
                c = f.read(1)
                if not c:
                    break
                tag = tag + c
                if c == "<":
                    found = True
                    between = False
                while between: #kai baigsis reiksme tarp tag'u
                    where_i_am = f.tell() # issisaugom, reikes pagrizti atgal, kad < nuskaitytume dar karta
                    c = f.read(1)
                    if c == "<":
                        f.seek(where_i_am) # griztam per simboli
                        between = False
                        break
                    if not c:
                        break
                    tag = tag + c
                while found: # kol rasim pabaiga
                    c = f.read(1)
                    tag = tag + c
                    if c == ">":
                        found = False
                        between = True
                        break
                yield tag

    """ Gets file path, returns generator and first two tags tuple
        Exmpl.: (keyword, field), (symbol, ;) """

    @staticmethod
    def read_xml_tags(file_name):

        tag_reader = XMLHelper.xml_tag(file_name)
        # Always skip first element
        next(tag_reader)
        while tag_reader:
            # Get first tag
            first_tag = ""
            while not first_tag.strip():  # Enteriai
                first_stag_wth_spaces = tag_reader.__next__()
                # print(first_stag_wth_spaces, "first_stag_wth_spaces")
                first_tag = first_stag_wth_spaces.strip()
            first_tag = first_tag[1:-1]
            # Get second tag
            second_tag_wth_spaces = tag_reader.__next__()
            # print("second_tag_wth_spaces", second_tag_wth_spaces, len(second_tag_wth_spaces))
            second_tag = second_tag_wth_spaces
            if second_tag == '&lt;':
                second_tag = '<'
            if second_tag == '&gt;':
                second_tag = '>'
            if second_tag == '&amp;':
                second_tag = '&'
            # Skip closing tag
            next(tag_reader)
            yield first_tag, second_tag
