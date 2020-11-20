# ^(\s|\t)+
# DISCIPLINA\n[0-9]+([a-zA-Z\s])\n
import re

f = open('./quotes.xml', 'r')
temp = '' + f.read()
f.close()

# Remove as tags HTML
regex = r"""&lt;td&gt;[\w\s\.\(\)";=áàâãéèêíïóôõöúçñÁÀÂÃÉÈÍÏÓÔÕÖÚÇÑ&\r\n\/-]+&lt;\/td&gt;"""

# Armazena as funcoes em uma lista
lista = re.findall(regex, temp)

regexIn = re.compile(r"&lt;td&gt;", re.IGNORECASE)
regexOut = re.compile(r"&lt;\/td&gt;", re.IGNORECASE)
regexSpace = re.compile(r"^\s+", re.IGNORECASE)

f = open('../finalDisciplinas', 'w')        
for i in lista:
	i = regexIn.sub("", i)
	i = regexOut.sub("\n", i)
	i = regexSpace.sub("", i)
	f.writelines(i)
f.close()