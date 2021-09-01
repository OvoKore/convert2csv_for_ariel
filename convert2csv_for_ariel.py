#    M              OOOOOOOO
#    A            OO--------OO
#    D          OO--------VVVVOO
#    E        OOVVVV------VVVVVVOO
#             OOVVVV------VVVVVVOO
#    B      OOVVVVVV--------VVVV--OO
#    Y      OOVVVVVV--------------OO
#         OO----------VVVVVV--------OO
#    O    OO--------VVVVVVVVVV------OO
#    V    OOVVVV----VVVVVVVVVV------OO
#    O    OOVVVVVV--VVVVVVVVVV--VV--OO
#    K      OOVVVV----VVVVVV--VVVVOO
#    O      OOVVVV------------VVVVOO
#    R        OOOO--------------OO
#    E            OO--------OOOO
#    !              OOOOOOOO

import re
import pandas as pd

f = open("ariel.csv", "r")

txt = f.read()
txt = txt.replace("Data cad", "Data_cad")
txt = re.sub(r"\n([\w| ]+-\w{2})", r"\nEstado: \1", txt)
txt = re.sub(r"   +","\t", txt)
txt = re.sub(r"\n([\w| ]+)\t", r"\nCidade: \1\t", txt)
txt = re.sub(r"\t([^:]+: ?[^\t]*)", r"\1\n", txt)
txt = re.sub(r"(NFe/CTe.:[^\n]*)", r"\1\nseparador_de_linhas_ovokore", txt)

linhas = txt.split("separador_de_linhas_ovokore")

clientes = list()

for linha in linhas:
    results = re.findall(r"([^:]+): ?([^\n]*)", linha)
    if results:
        cliente = dict()
        is_endereco = False
        is_cobranca = False
        for r in results:
            nome = r[0].replace("\n",str())
            valor = r[1]
            if nome == 'Endereco':
                is_endereco = True
            elif nome == 'Cobranca':
                is_cobranca = True
                is_endereco = False
            elif nome == 'Telefone':
                is_cobranca = False
            
            ini = str()
            if is_endereco:
                ini = "Endereco_"
            elif is_cobranca:
                ini = "Cobranca_"

            cliente[ini+nome] = valor
        clientes.append(cliente)


final = pd.DataFrame(clientes)
final.to_csv("ovokore.csv", index=False)