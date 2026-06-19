#cedulas
money = int(input())
centena = money // 100
cincoDezena = (money % 100) // 50
duasDezena = ((money % 100) % 50) // 20
umaDezena = (((money %100) % 50) % 20) // 10
cinco = ((((money %100) % 50) % 20) % 10) // 5
dois = (((((money %100) % 50) % 20) % 10) % 5) // 2
um = ((((((money %100) % 50) % 20) % 10) % 5)) // 1
print(f"{centena} nota(s) de R$ 100,00")
print(f"{cincoDezena} nota(s) de R$ 50,00")
print(f"{duasDezena} nota(s) de R$ 20,00")
print(f"{umaDezena} nota(s) de R$ 10,00")
print(f"{cinco} nota(s) de R$ 5,00")
print(f"{dois} nota(s) de R$ 2,00")
print(f"{um} nota(s) de R$ 1,00")
