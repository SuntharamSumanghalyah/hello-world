#!/usr/bin/python
# -*- coding: utf-8 -*-

# xml und wordcloud packages importieren
import xml.etree.ElementTree as et
from glob import glob
import re

from wordcloud import WordCloud
import matplotlib.pyplot as plt
#editing this file to show changes in the 'create_a_copy' branch

#eine Datei erstellen in .csv Format, damit Endprodukt gespeichert werden kann.
outputfile = open("ThomasMann_Schlagwoerter.csv", "w", encoding="utf-8")

#Die .xml Datei von Thomas Mann einlesen
tree = et.parse("eth_tml.marc.xml")
root = tree.getroot()
#leere strings definieren, damit der Text gespeichert werden kann.
sword_string = ""
gnd_string = ""
titelstring = ""
#Liste erstellen, um dem wordcloud Format zu dienen
Liste = []



# Finde tag 245 > Titel des Werkes und schreibe ihn in titlestring
for record in root.findall('.//{http://www.loc.gov/MARC21/slim}datafield'):
    if record.get("tag")=="245":
        for titel in record.findall('{http://www.loc.gov/MARC21/slim}subfield'):
            if titel.get("code")=="a":
                titelstring = titel.text  
    #finde 650 mit code == a um Schlagwort zu erhalten
    if record.get("tag")=="650":
        for sword in record.findall('{http://www.loc.gov/MARC21/slim}subfield'):#variable ort zum Finden der entsprechenden Variable
            if sword.get("code")=="a":
            	sword_string = sword.text
    #650 mit code == 2 um gnd Schlagwort und nicht fast oder andere Schlagwörter zu finden mit string = gnd
    if record.get("tag")=="650":
       	for gndtm in record.findall('{http://www.loc.gov/MARC21/slim}subfield'):
        	if gndtm.get("code")=="2":
        		if str('gnd') in gndtm.text:
        			gnd_string = gndtm.text
                    #schreibe die strings in den outputfile, damit es im .csv korrekt angezeigt wird. 
        			outputfile.write(sword_string + '\t' + titelstring + '\t' + gnd_string + '\n')
                    #Schreibe die Schlagwörter in eine Liste mti einem whitespace zwischen den Schlagwörtern
        			Liste.append(sword_string)
        			text = ' '.join(Liste)
# Stelle die Schlagwörter, die in 'text' gespeichert sind, in einer Wordcloud dar: 
wordcloud = WordCloud(width=480, height=480, margin=0).generate(text)
fig = plt.figure()
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.margins(x=0, y=0)
fig.savefig("se_output"+".png")
plt.show()
plt.close()
#schliesse den outputfile > ThomasMann_Schlagwoerter.csv
outputfile.close()

