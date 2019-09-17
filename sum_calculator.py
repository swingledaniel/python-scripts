
def sum(f, n, k=0):
    s = 0
    for i in range(k, n+1):
        print (i, end=' ')
        s += f(i)
    print ("=", s)
    return s
"""
def double_sum(f, n1, n2, k1=0, k2=0, inner_start_dep=False, inner_end_dep=False):
    s = 0
    if inner_start_dep:
        for i in range(k1, n1+1):
            print ("Summing with i ={}:".format(i))
            s += sum(f, n2, i+k2)
    elif inner_end_dep:
        for i in range(k1, n1+1):
            print ("Summing with i ={}".format(i))
            s += sum(f, i+n2, k2)
    else:
        for i in range(k1, n1+1):
            print ("Summing with i ={}".format(i))
            s += sum(f, n2, k2)
    return s"""

n = 1
s = 0
for j in range(-3, n-2):
    for k in range(j+3, n+3):
        print ()
        s += k-3

print ("New sum", s)

formula = lambda x: (x+1)*(x*(x+44)-72)/12
print ("The formula produces {} for n = {}".format(formula(n), n))

print ("Add up:")
print ([k-3 for k in range(0, 5+1)])
print ([k-3 for k in range(1, 5+1)])
print ([k-3 for k in range(2, 5+1)])
