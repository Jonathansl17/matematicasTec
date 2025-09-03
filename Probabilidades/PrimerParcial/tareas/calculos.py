
import math

universo = math.comb(35,12)

caso1 = math.comb(4,1)*math.comb(33,10)
caso2 = math.comb(4,2)*math.comb(31,8)
caso3 = math.comb(4,3)*math.comb(29,6)
caso4 = math.comb(4,4)*math.comb(27,4)

resultado = universo-(caso1-caso2+caso3-caso4)

print(resultado)


