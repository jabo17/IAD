def ack(n,m):
    if n==0:
        return m+1
    elif m==0:
        return ack(n-1, 1)
    else:
        return ack(n-1, ack(n,m-1))

for n in range(4):
    for m in range(4):
        print("ack von n=",n," und m=",m,": ", ack(n,m))