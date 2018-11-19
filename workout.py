
name= input("What is your name?")
print ("What is your age?")
print ("What is your weight in pounfd?")

print("Hello "+name+" how are you?") 

t=str(input("how many days have you worked out?"))
s=str(input("How long you workout for?"))
n=str(input("How many push ups can you do?"))
w=str(input("How many sit ups/crunches can you do?"))

profile = []
information = []

def retriveInput(q):
    i = input(q)
    return i

a1 = retriveInput("What is your name?")
a2 = retriveInput("What is your age?")
a3 = retriveInput("What is your weight?")

profile.append(a1)
profile.append(a2)
profile.append(a3)
