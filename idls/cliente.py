import sys
from omniORB import CORBA
import CosNaming, lista01

# Initialise the ORB
orb = CORBA.ORB_init(sys.argv, CORBA.ORB_ID)

# Obtain a reference to the root naming context
obj         = orb.resolve_initial_references("NameService")
rootContext = obj._narrow(CosNaming.NamingContext)

if rootContext is None:
    print "Failed to narrow the root naming context"
    sys.exit(1)

# Resolve the name "test.my_context/ExampleEcho.Object"
name = [CosNaming.NameComponent("lista1", "Funcionario"),
        CosNaming.NameComponent("Funcionario", "Object")]
try:
    obj = rootContext.resolve(name)

except CosNaming.NamingContext.NotFound, ex:
    print "Name not found"
    sys.exit(1)

# Narrow the object to an Example::Echo
funcionarioo = obj._narrow(lista01.Funcionario)

if funcionarioo is None:
    print "Object reference is not an lista01::Funcionario"
    sys.exit(1)

# Invoke the operation

print ("pode aposentar ",funcionarioo.pode_aposentar(10,10))

