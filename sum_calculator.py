def summation(f, n, k=0):
    s = 0
    for i in range(k, n+1):
        print (f(i), end=' ')
        s += f(i)
    print ("=", s)
    return s

def double_sum(f, n1, n2, k1=0, k2=0, inner_start_dep=False, inner_end_dep=False):
    s = 0
    if inner_start_dep:
        for i in range(k1, n1+1):
            print ("Summing with i ={}:".format(i))
            s += summation(f, n2, i+k2)
    elif inner_end_dep:
        for i in range(k1, n1+1):
            print ("Summing with i ={}".format(i))
            s += summation(f, i+n2, k2)
    else:
        for i in range(k1, n1+1):
            print ("Summing with i ={}".format(i))
            s += summation(f, n2, k2)
    return s
