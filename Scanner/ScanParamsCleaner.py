import os
import xml.etree.ElementTree as et

xml_dir = "C:\\Users\\awise\\Desktop\\ScannerInfo\\"
new_txt = "C:\\Users\\awise\\Desktop\\ScannerInfo\\cleanScan.txt"
print('Working in: ', xml_dir)

tree = et.parse(xml_dir+'scanner.xml')
root = tree.getroot()

sc_tags = ['displayName', 'scanCode', 'instruments', 'access']
stk_sc_types = []

sc_types_elems = root.findall('./ScanTypeList/ScanType')
with open(new_txt,'w') as cleanFile:
        for st in sc_types_elems:
                if 'STK' in st.find('instruments').text:
                        stk_sc_types.append(st)
                        print(sc_tags[0], st.find(sc_tags[0]).text)
                        for a in sc_tags:
                                try:
                                        myTry= a+' '+st.find(a).text+'\n'
                                        cleanFile.write(myTry)
                                except AttributeError:
                                        pass #print(a,'[element not found]')

        elems = root.findall('./FilterList/RangeFilter')
        # print(len(elems))
        elems.extend(root.findall('./FilterList/SimpleFilter'))
        # print(len(elems))

        # for e in elems:
                # try:
                #         print('id: ', e.find('./Columns/Column/name').text)
                # except AttributeError:
                #         print('id: ', e.find('./id').text)