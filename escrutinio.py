# Obtener los XML de todas las mesas para la categoría Gobernador

import urllib2

mesas = {}
i = 1
exep = False
while i < 8000:
    try:
        resultado = urllib2.urlopen("http://elecciones.santafe.gov.ar/mesaXml/gobernador/%d/N" %i)
        mesas[i] = resultado.read()
        print i
        i += 1
    except:
        i += 1
        
# Parsear los XML para obtener nombre del partido y cantidad de votos

import xml.etree.ElementTree as ET

resultados = {}
for k in mesas:
    xml = mesas[k]
    r = ET.fromstring(xml)
    resultado = {}
    for x in r.findall("detalle"):
        resultado[x.find("nombre").text] = int(x.find("cantidad").text)
        resultados[k] = resultado

# Función para encontrar las mesas en las que un partido tiene 0 votos

def mesas_con_0(nombre):
    mesas = []
    for k in resultados:
        if resultados[k][nombre] == 0:
            mesas.append(k)
    return mesas

# Si en una mesa los tres principales partidos tiene 0 votos
# asumo que es una mesa con telegrama desestimado

pro = mesas_con_0("UNION PRO FEDERAL")
fpcs = mesas_con_0("FRENTE PROGRESISTA CIVICO Y SOCIAL")
fpv = mesas_con_0("FRENTE JUSTICIALISTA PARA LA VICTORIA")

desestimadas = (set(fpcs) & set(pro) & set(fpv))

set(pro) - desestimadas   # set([1725, 270, 5351])
set(fpcs) - desestimadas  # set([6852, 1478, 134, 7591, 5485, 4501, 6555, 1845])
set(fpv) - desestimadas   # set([1478, 7591, 5545, 4912, 7601, 1845, 4950, 4729, 6555, 6333])

# Finalmente me guardo una copia de los archivos XML para futuras revisiones

for x in mesas:
    archivo = open("mesa_%d.xml" % x, "w")
    archivo.write(mesas[k])
    archivo.close()