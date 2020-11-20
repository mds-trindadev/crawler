# ^(\s|\t)+
import re

f = open('./quotes.xml', 'r')
temp = '' + f.read()
f.close()

# Remove as tags HTML
regex = r"""(class="tituloDisciplina"&gt;.*&lt;/span&gt;|class="turma" align="center"&gt;.*&lt;/td&gt;|class="anoPeriodo" align="center"&gt;.*&lt;/td&gt;|class="nome"&gt;.*&lt;/td&gt;|&lt;td&gt;[A-Z0-9\s]+\n)"""

# Armazena as funcoes em uma lista
lista = re.findall(regex, temp)

regexFormat = re.compile(r"""(class="tituloDisciplina"&gt;|&lt;/span&gt;|&lt;/td&gt;|class="anoPeriodo" align="center"&gt;|class="nome"&gt;|&lt;td&gt;|\n)""", re.IGNORECASE)
regexTurma = re.compile(r"""class="turma" align="center"&gt;""", re.IGNORECASE)

f = open('../finalTurmas', 'w')        
for i in lista:
	i = regexFormat.sub("", i)
	i = regexTurma.sub('class="turma"', i)
	f.writelines(i+'\n')
f.close()