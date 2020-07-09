

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

