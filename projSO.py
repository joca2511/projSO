import argparse
class processo():
    def __init__(self,nome, entrada,tempo,IOs):
        self.nome = nome
        self.entrada = int(entrada)
        self.saida = 0
        self.decorrido = 0
        self.tempo = int(tempo)
        self.historico = []
        if IOs == False:
            self.IOs = [0]
        else:
            self.IOs = IOs ##eh False caso esteja vazio!
        

    def __str__(self):
        return f"Nome: {self.nome}\nEntrada: {self.entrada}\nTempo: {self.tempo}\nInterrupcoes: {self.IOs}"
    
##criacao de parser para argumentos
parser = argparse.ArgumentParser(
    prog="projSO",
    description="Programa que simula Round-Robin"
)
parser.add_argument("-e","--entrada",help="Arquivo de entrada",default="listaprocessos.txt")
parser.add_argument("-s","--saida",help="Arquivo de saida",default="resultados.txt")
parser.add_argument("-q","--quantum",help="Valor de Quantum",default=4,type=int)
parser.add_argument("-g","--grafico",help="Arquivo de grafico",default="grafico.txt")
args = parser.parse_args()
print(args)


#argumentos que podem ser modificados
arquivoentrada = args.entrada ##nome do arquivo de entrada
arquivosaida = args.saida ##nome do arquivo de saida
arquivografico = args.grafico ##nome do arquivo de grafico
quantum = args.quantum ##variavel que controla quantum





processos = []
arq = open(arquivoentrada,"r")

for linha in arq:
    linha = linha.split(" ")
    paradas = False ##caso base de paradas
    if len(linha)>3: ##basicamente perguntando se tem IO!
        paradas = linha[3].split(",")

        for i in range(len(paradas)): ##transforma o conteudo de paradas em int!
            paradas[i] = int(paradas[i])

    print(linha) ##debug
    print(paradas) ##debug
    p1 = processo(linha[0],linha[1],linha[2],paradas)
    processos.append(p1)
arq.close()

for i in processos:
    print(i)
    
arqresposta = open(arquivosaida,"w")

print("\n\nESCALONANDO OS ROBINS REDONDOS!\n")
tempo = 0
stack = []
processando = False
esperas = []
quantumatual = 0
while(True): ##continua ate processos estiver vazio! 
    removidos = []
    arqresposta.write(f"TEMPO: {tempo}\n")
    print(f"TEMPO: {tempo}")

    if processando != False: ##caso tenha algo no processador!
        if processando.decorrido == processando.tempo: ##teminou processo!
            arqresposta.write(f"EVENTO: {processando.nome} TERMINOU DE PROCESSAR!\n")
            print(f"EVENTO: {processando.nome} TERMINOU DE PROCESSAR!")
            processando.saida = tempo ##adiciona o tempo do ultimo processo
            processando.historico.append(tempo) ##adiciona o tempo para o historico
            esperas.append(processando)

            processando = False
            quantumatual = 0
        elif processando.decorrido in processando.IOs: ##caso o tempo de processo atual seja igual um dos tempos dentro das interrupcoes
            arqresposta.write(f"EVENTO: IO DE {processando.nome}!\n")
            print(f"EVENTO: IO DE {processando.nome}!")
            stack.append(processando) ##joga de volta para a stack
            processando = False
            quantumatual = 0
        elif quantumatual == quantum: ##caso quantum == quantumatual
            arqresposta.write(f"EVENTO: PREEMPCAO DE {processando.nome}, FIM QUANTUM!\n")
            print(f"EVENTO: PREEMPCAO DE {processando.nome}, FIM QUANTUM!")
            stack.append(processando)
            processando = False
            quantumatual = 0
        
    if processando == False and len(stack) == 0 and len(processos) == 0: ##caso de fim!
        arqresposta.write("ACABOU!\n\n")
        print("ACABOU!\n")
        break
    for i in range(len(processos)): ##olha todos os processos e os introduz se o tempo atual eh igual ao tempo de entrada
        if processos[i].entrada == tempo:
            arqresposta.write(f"EVENTO: Adicionando {processos[i].nome} para a stack!\n")
            print(f"EVENTO: Adicionando {processos[i].nome} para a stack!")
            stack.append(processos[i])
            removidos.append(i)

    for i in removidos: ##remove todos os processos adicionados a stack
        ##print(f"Removendo {processos[i].nome} da lista de processos!")
        processos.pop(i)

    if processando == False: ##caso nada esteja processando! Tenta colocar algo em processando
        if len(stack) == 0:
            arqresposta.write("NENHUM PROCESSO EM CPU OU EM ESPERA!")
            print("NENHUM PROCESSO EM CPU OU EM ESPERA!")
        if len(stack) > 0:
            processando = stack[0] ##pega o 1o processo na stack
            stack.pop(0) ##remove o 1o processo da stack
            
        
   
       
    arqresposta.write("FILA: ")
    print("FILA: ")
    if len(stack) == 0: ##se stack esta vazia!
        arqresposta.write("VAZIA!\n")
        print("VAZIA!")
    else:
        for i in stack:
            arqresposta.write(f"{i.nome}({i.tempo-i.decorrido}) ")
            print(f"{i.nome}({i.tempo-i.decorrido}) ")
            
        
        arqresposta.write("\n")
        print("\n")
    
    if processando == False: ##se cpu estiver vazio
        arqresposta.write("CPU: VAZIO!\n")
        print("CPU: VAZIO!")
    else:
        arqresposta.write(f"CPU: {processando.nome}({processando.tempo - processando.decorrido})\n")
        print(f"CPU: {processando.nome}({processando.tempo - processando.decorrido})")
        processando.historico.append(tempo)
        processando.decorrido += 1
        quantumatual +=1
    tempo+=1
    arqresposta.write("\n")
    print("\n")
arqresposta.write("ESPERAS:\n")
print("ESPERAS:")
mediaespera = 0
for i in esperas:
    arqresposta.write(f"{i.nome}: {i.saida-i.entrada}\n")
    print(f"{i.nome}") ##esperas de cada processo
    print(f"Espera {i.nome}: {i.saida-i.entrada}")
    mediaespera += i.saida-i.entrada

mediaespera = mediaespera/len(esperas)
arqresposta.write(f"\nMedia: {mediaespera}")
print(f"\nMedia: {mediaespera}")
arqresposta.close()
arqgraf = open(arquivografico,"w")
for i in esperas:
    stringProcesso = ""
    ultimoProcesso=0
    print(f"{i.nome}:{i.historico}")
    for tempoProcesso in i.historico:
        for m in range(ultimoProcesso,tempoProcesso):
            stringProcesso +=" "
        if tempoProcesso == i.historico[-1]: ##ve se eh o ultimo, logo eh o caso de saida!
            stringProcesso+="!"
        else:
            stringProcesso += "#"
            
        ultimoProcesso=tempoProcesso+1
    arqgraf.write(f"{i.nome}:{stringProcesso}\n")
      
arqgraf.close()