ch=100
h=[0,1,2,3,4,5,6,7,8,180]
max = 20
min = 0
for i in range(0,len(h)):
    print(ch-(h[-1-i]/(max-min))*ch)

