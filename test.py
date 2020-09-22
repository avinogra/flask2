import random
r=[]
while len(r)<6: 
    n=random.randint(0, 11) 
    if n not in r :
        r.append(n)
print(r)