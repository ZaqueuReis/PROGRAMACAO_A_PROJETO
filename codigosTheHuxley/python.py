def ehPar(num) :
    if num % 2 == 0 :
        return True
    return False

def contarDigitosPares(n) :
    if n <= 0 :
        return 1
    else :
        if ehPar(n % 10) :
            return contarDigitosPares(n // 10) + 1
        else :
            return contarDigitosPares(n // 10)

n = int(input())
resultado = contarDigitosPares(n)
print(resultado)