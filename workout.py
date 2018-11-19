
name= input("What is your name?")
age=input("What is your age?")
weight=input("What is your weight in pounds?")
height=input("How tall are you in inches?")

print("Hello "+name+" Welcome to Beyond Fitness!")

t=str(input("how many days have you worked out in the past week?"))
s=str(input("How long do you usually workout for in minutes ?"))

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
