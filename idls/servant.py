import sys
from omniORB import CORBA, PortableServer
import CosNaming, lista01, lista01__POA


class Funcionario_i(lista01__POA.Funcionario):
    def reajuste(self, nome, cargo, salario):
        if cargo == "programador":
            reajuste = salario * 0.18
        if cargo == "operador":
            reajuste = salario * 0.2
        return salario + reajuste

    def salario_liquido(self, nome, nivel, salario_bruto, numero_dependentes):
        if nivel == "A":
            if numero_dependentes == 0:
                desconto = 0.03
            if numero_dependentes > 0:
                desconto = 0.08
        if nivel == "B":
            if numero_dependentes == 0:
                desconto = 0.05
            if numero_dependentes > 0:
                desconto = 0.1

        if nivel == "C":
            if numero_dependentes == 0:
                desconto = 0.08
            if numero_dependentes > 0:
                desconto = 0.15
        if nivel == "D":
            if numero_dependentes == 0:
                desconto = 0.1
            if numero_dependentes > 0:
                desconto = 0.17
        return salario_bruto - (salario_bruto * desconto)

    def pode_aposentar(self, idade, tempo_de_servico):
        if idade >= 65:
            return True
        if tempo_de_servico >= 30:
            return True
        if idade >= 60 and tempo_de_servico >= 25:
            return True
        return False


orb = CORBA.ORB_init(sys.argv, CORBA.ORB_ID)
poa = orb.resolve_initial_references("RootPOA")

funcionarioi = Funcionario_i()
funcionarioo = funcionarioi._this()

obj = orb.resolve_initial_references("NameService")
rootContext = obj._narrow(CosNaming.NamingContext)

if rootContext is None:
    print ("Failed to narrow the root naming context")
    sys.exit(1)

name = [CosNaming.NameComponet("lista1", "funcionario")]

try:
    lista1_Funcionario = rootContext.bind_new_context(name)
    print ("novo contexto lista1.funcionario vinculado")
except CosNaming.NamingContext.AlreadyBound, ex:
    print "lista1 funcionario ja exite"
    obj = rootContext.resolve(name)
    lista1_Funcionario = obj._narrow(CosNaming.NamingContext)
    if lista1_Funcionario is None:
        print("lista1.funcionario existe mas nao e um contexto de nomes")
        sys.exit(1)
name = [CosNaming.NameComponent("Funcionario", "Object")]
try:
    lista1_Funcionario.bind(name, funcionarioo)
    print("novo objeto funcionario vinculado")

except CosNaming.NamingContext.AlreadyBound:
    lista1_Funcionario.rebind(name, funcionarioo)
    print "vinculacao a funcionario ja existia -- revinculando"

poaManager = poa._get_the_POAManager()
poaManager.activate()

orb.run()
# print ("pode aposentar ",funcionarioo.pode_aposentar(10,10))
