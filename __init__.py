from os import path,remove,unlink,rmdir,system,name
from time import sleep
# Before you go ahead,please create a .txt file to contain the customers that'll be recorded. After enter the path to it in the line below and uncomment it
# mainFilePath=[here you've to write down the path directly toward the file .txt which is gonna contain the costumers]
#Registration System
class Customer:
    def __init__(self,name,age,address,tel):
        self.__name=name
        self.__age=age
        self.__address=address
        self.__tel=tel

    @property
    def name(self):return self.__name

    @property
    def age(self):return self.__age

    @property
    def address(self):return self.__address

    @property
    def tel(self):return self.__tel

    @staticmethod
    def hasNumberInString(text):
        from string import digits
        for number in digits:
            for char in text:
                if number==char:return True
        return False

    def nameVerifier(self): #Verifica se o argumento nome é válidoe
        return  not (self.__name.isnumeric() or self.__name.isspace() or len(self.__name)==0 or self.hasNumberInString(self.__name))
        
    def invalidStringProperties(self): #Verifica se as strings address e tel são válidas
        return self.__address.isspace() or len(self.__address)==0 or self.__tel.isspace() or len(self.__tel)==0
        
#Files
def fileVerifier(nameFile):
    from os.path import exists  
    return exists(nameFile)

def fileCreator(nameFile):
    if not fileVerifier(nameFile): #If file does not exists,will be created
        try:
            newFile=open(nameFile,"x")
            newFile.close()
        except: return "Error"
        else:return "Created"
    else:return "File already exists"

#Tools
def erase():
    system("cls" if name=="nt" else "clear")

def title(text):
    row()
    print(text.center(50))
    row()

def bigTitle(text):
    bigRow()
    print(text.center(70))
    bigRow()

def row():print("-"*50)

def bigRow():
    print("-"*70)

def verificFileSize(file):
    quantRows=0
    try:f=open(file)
    except:return "Error"
    else:
        for rows in f:
            quantRows+=1
        f.close()
        return quantRows 

#Main Routines
def menu(*menu):
    mainFile=fileCreator(mainFilePath)
    while True:    
        title("Sistema de Cadastramento 1.0.1")
        for cont,data in enumerate(menu):
            print(f"{data:<30}",end="")
            if cont%2==1:print()
        row()    
        try:
            choice=int(input("--> "))
            erase()
        except(ValueError):
            erase()
            print("->[Escolha uma opção válida]<-")
            sleep(1)
        except(KeyboardInterrupt):
            erase()
            print("->[Por favor,é necessário escolher uma opção válida]<-")
            sleep(1)
        else:
            if choice<=0 or choice>4: #if option or choice is out of range
                print("->[Opção inválida]<-")
                sleep(1)
            else:
                return choice
        finally:erase()

def body():
    while True:    
        option=menu("[1] -> Registrar","[2] -> Ver clientes","[3] -> Limpar arquivo","[4] -> Sair")
        if option==1:
            register()
        elif option==2:
            showCustomers()
        elif option==3:
            clearFile(mainFilePath)
        else:
            finish("Finalizando...")
            return

#Registrar cliente
def writingDataInFile(file,obj):
    try:
        f=open(file,"a")
    except:return "Error"
    else:
        f.write("Nome:"+obj.name+";"+"Idade:"+str(obj.age)+";"+"Endereco:"+obj.address+";"+"Telefone:"+obj.tel+"\n")
        f.close()
        title("Registrado")
        sleep(1)
        del obj #obj é usado apenas para organização dos dados de cada cliente,após seu uso,é descartado
        return

def register():
    while True:    
        erase()
        title("Preencha os campos abaixo")
        try: #Instanciando a class Customer
            customer=Customer(str(input("Nome:")),int(input("Idade:")),str(input("Endereco:")),str(input("Telefone:")))
            erase()
        except(KeyboardInterrupt):
            erase()
            print("->[Por favor,é necessário preencher os campos]<-")
            sleep(1)
        except(ValueError):
            erase()
            print("->[Verifique seus dados]<-")
            sleep(1)
        else:# Validando os dados com os métodos nameVerifier e invalidStringProperties da classe Customer
            if not customer.nameVerifier() or customer.invalidStringProperties():
                print("->[Verifique seus dados]<-")
                sleep(1)
            else:
                writingDataInFile(mainFilePath,customer)#Passando o objeto instanciado como parâmetro para a função pois usaremos suas propriedades
                del customer
                return
        finally:erase()

#Ver clientes
def catchOption(fileRowsQuant): #Pega e valida a opção escolhida pelo usuário
    try:
        customerCode=int(input("Para mais detalhes,informe o código do cliente \n[-1 para voltar] -> "))
        erase()
    except:return "invalido"
    else:
        if customerCode!=-1 and (customerCode<=0 or customerCode>fileRowsQuant):return "invalido"
        return customerCode #Se o usuário escolher um código válido,essa linha acabará por ser executada

def findNameInFile(fileRow): #Encontra o nome de cada cliente a partir de sua linha no arquivo
    try:f=open(mainFilePath)
    except:return "Error"
    else:
        for counter,data in enumerate(f):
            if counter+1==fileRow:
                catchName=data.split(";")[0].split(":")
                '''data tem seus dados divididos entre [;];
                A posição [0] de data (onde temos -> Nome:[cliente]) é dividida em duas novas posições;
                O nome que queremos se encontra na posição [1].'''
                return catchName[1]

def customerData(customerCode,customerName): #Mostra informações específicas de cada cliente
    try:f=open(mainFilePath)
    except:return "Error"
    else:    
        erase()
        bigTitle(f"Dados de cliente: {customerName}")
        for counter,data in enumerate(f):
            if counter+1==customerCode:
                data=data.replace("\n","").split(";")
                for customerInfo in data: #data contém todos os dados do cliente com o código customerCode em formato de lista;customerInfor percorre data recebendo cada posição e,finalmente,sendo usado para mostrar seus dados 
                    print(customerInfo)
                break #Terminou de mostrar,o laço é encerrado
        bigRow()
        sleep(3)
        return 

def customersTable(file):
    while True:    
        try:
            f=open(file)
        except:return "Error"
        else:  
            bigTitle("Tabela de clientes")
            print(f"{'Código':<40}{'Nome'}")
            bigRow()
            for code,rowFile in enumerate(f.readlines()):
                '''code conta de acordo com as linhas do arquivo;cada cliente recebe sua posição no mesmo (em termos de linha) como código;
                rowFile recebe cada linha do arquivo em formato de lista (f.readlines() faz isso);
                rowFile recebe "" em lugar de sua "\n" e cada dado do cliente é separado pelo split();catchName recebe a posição 0 de rowFile (onde se se encontra-> Nome:[cliente],porém com o método split dividindo Nome e [cliente].Por fim,usa-se a posição 1 de catchName para mostrar no print,o nome que queremos;
                Por fim,tudo é mostrado em formato tabular'''
                rowFile=rowFile.replace("\n","").split(";")
                catchName=rowFile[0].split(":")
                print(f"{code+1:<40}{catchName[1]}")
            bigRow()
            option=catchOption(code+1) 
            '''Passando a quantidade de linhas do arquivo para a função catchOption para ela saber o intervalo de código de clientes que deva validar.Se o usuário pedir para ver os dados de um cliente com código superior à quantidade de linhas do arquivo registradas ou menor/igual a zero,dará erro.'''
            if option==-1:return #-1 faz com que a rotina do programa volte para o menu de opções
            elif option=="invalido":
                erase()
                print("->[Código inválido]<-")
                sleep(1)
            else:
                customerData(option,findNameInFile(option)) #Mostra os dados do cliente solicitado;findNameInFile procura o nome do cliente com o código digitado em option para usá-lo no cabeçalho de customerData
            f.close()
        finally: erase()
            
def showCustomers():
    erase()
    if verificFileSize(mainFilePath)==0: #Se customersData estiver vazio,não é possível mostrar uma tabela com clientes
        title("Você ainda não cadastrou ninguém")
        sleep(2)
    else:
        customersTable(mainFilePath)#Se customersData possuir clientes cadastrados,é possível mostrar uma tabela com os mesmos,o que customersTable é incumbida a fazer 
    erase()
    return

#Clean file
def clearFile(fileName):
    from os import unlink
    if verificFileSize(fileName)==0:
        erase()
        title("Seu arquivo já está vazio!")
        sleep(1)
        erase()    
    else:    
        erase()
        title("Limpando seu arquivo...")
        sleep(2)
        try:unlink(fileName)
        except:
            erase()
            title("Erro")
            sleep(2)
        else:
            erase()
            title("Limpo com sucesso!")
            sleep(1)
        finally:erase()

#Finish session
def finish(text):
    erase()
    title(text)
    sleep(2)
    erase()

body() #Calling the main function which is called body
