def transpose(matr):
    res=[]
    if matr:
        n=len(matr)
        m=len(matr[0])
        for j in range(m):
            tmp=[]
            for i in range(n):
                tmp=tmp+[matr[i][j]]
            res=res+[tmp]
    return res
