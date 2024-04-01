#How to get list of parameters name from a function in Python
import inspect 
import numpy as np
print(inspect.signature(np.linspace))

# How to Print Multiple Arguments in Python

def func(*args,**kwargs):
    for i in args:
        print(i)
    for j in kwargs:
        print(f"{j}:{kwargs[j]}")
func(2,3,name="nobody",hobby="code")

# Python program to find the power of a number using recursion
def pow(num,power):
    if power==0:
        return 1
    return num*pow(num,power-1)
print(f"5 raised to power 3={pow(5,3)}")