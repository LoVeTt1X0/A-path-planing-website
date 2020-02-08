Points=[]
#列表元素形如“2（2,2）2”第一个数字表示楼层，第二三个数字表示坐标
#第四个数字表示拥堵程度，1代表轻微，2代表中度，3表示严重
def addInfo(floor,position,level):
    if level == "轻微拥堵":
        level = "1"
    elif level == "中度拥堵":
        level = "2"
    elif level == "严重拥堵":
        level = "3"
    if position=="a":
        for i in range(4,23):
            str1=floor+"(3,%s)"%i+level
            str2=floor+"(4,%s)"%i+level
            Points.append(str1)
            Points.append(str2)
    if position=="b":
        for i in range(25,44):
            str1=floor+"(3,%s)"%i+level
            str2=floor+"(4,%s)"%i+level
            Points.append(str1)
            Points.append(str2)
    if position=="c":
        for i in range(4,23):
            str1=floor+"(19,%s)"%i+level
            str2=floor+"(20,%s)"%i+level
            Points.append(str1)
            Points.append(str2)
    if position=="d":
        for i in range(25,44):
            str1=floor+"(19,%s)"%i+level
            str2=floor+"(20,%s)"%i+level
            Points.append(str1)
            Points.append(str2)
    if position=="e":
        for i in range(5,19):
            str1=floor+"(%s,3)"%i+level
            str2=floor+"(%s,4)"%i+level
            Points.append(str1)
            Points.append(str2)

    if position=="f":
        for i in range(5,19):
            str1=floor+"(%s,23)"%i+level
            str2=floor+"(%s,24)"%i+level
            Points.append(str1)
            Points.append(str2)
    if position=="g":
        for i in range(5,19):
            str1=floor+"(%s,43)"%i+level
            str2=floor+"(%s,44)"%i+level
            Points.append(str1)
            Points.append(str2)

