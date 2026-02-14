import re
from random import randint as ri
from typing import List
from typing import Tuple

def separar(lista_dados) -> List[Tuple[str,str,str]]: # Sinal, numero de dados, dado

    dados_tupla = []

    if lista_dados[0][0] not in ["+", "-"]:
        lista_dados[0] = f"+{lista_dados[0]}"

    for item in lista_dados:
        sinal = item[0]
        corpo = item[1:].lower()
        nr, ld = corpo.split("d")
        if nr == "":
            nr = "1"
        dados_tupla.append((sinal, nr, ld))

    return dados_tupla

def rolar(lista_dados, mod): # -> int:
    dados = separar(lista_dados)
    lista_resultados = []

    print("\nResultado dos dados: ", end = "")
    for dado in dados:
        sinal = dado[0]
        num_rolagens = int(dado[1])
        num_dado = int(dado[2])
        for i in range(num_rolagens):
            print(resultado := ri(1, num_dado), end=" ")
            if sinal == "-":
                resultado *= -1
            lista_resultados.append(resultado)

    if mod != 0:
        if mod > 0:
            print(f" + {mod}")
        else:
            print(f" - {mod*-1}")

    return sum(lista_resultados)+mod

def pegar_dados_string(string_dados) -> List[str]:
    dados_limpos = re.split(r'(?=[+-])', string_dados.replace(" ", ""))
    return [dado for dado in dados_limpos if dado]

def verificar_rolagem_valida(lista_dados):
    padrao = r'^[+-]?\d*[dD]\d+$'
    valido = all(re.match(padrao, dado) for dado in lista_dados)
    return valido

def print_titulo():
    print("\n" + "=" * 30)
    print("   ROLADOR DE DADOS RPG   ")
    print("=" * 30 + "\n")

print_titulo()
while True:
    print("Digite 0d0 para sair do programa!")
    entrada = input("Insira a string de dados a serem rolados: ")

    if entrada.lower() == "0d0":
        print("Finalizando o programa!")
        break

    option = ""
    modificador = 0
    while option not in ["n","s"]:
        option = input("Há um modificador? s/n\n")
        if option.lower() == "n":
            modificador = 0
        elif option.lower() == "s":
            try:
                modificador = int(input("Insira o valor do modificador (Positivo ou Negativo): ").replace(" ", ""))
            except ValueError:
                print("Valor não é um número!")
                option = ""
        else:
            print("Opcao invalida!")

    dados = pegar_dados_string(entrada)
    rolagem_valida = verificar_rolagem_valida(dados)

    if rolagem_valida:
        try:
            res = rolar(dados, modificador)
            print(f"\nSomatorio das rolagens: {res}\n")
        except ValueError:
            print("\nNão é possível rolar dado de 0 lados!")
    else:
        print("\nRolagem invalida! Siga o padrão de dados:\n\tNumero + (\"d\" ou \"D\") + Numero")