import numpy as np
import os
import time
import cv2
import math
from app01 import find
from app01 import RoadInfo as R
start_manglu = {}
end_manglu = {}
def is_yongdu(x,y,flag):
    string = str(x)+','+str(y)
    if flag == 0:
        if string in start_manglu.keys():
            return start_manglu[string]
        else:
            return 0
    else:
        if string in end_manglu.keys():
            return end_manglu[string]
        else:
            return 0
class Point:
    def __init__(self, x,y,flag,d=None,h_n=0, g_n=0):#传入的是一个二元组
        self.x = x
        self.y = y
        self.flag = flag
        self.parent = None
        self.h_n = h_n
        self.g_n = g_n
        self.f_n = self.h_n + self.g_n
        self.dirs = [1,2,3,4,5,6,7,8]#一共八个方向
        self.d = []
    @property
    def pos(self):
        return self.x,self.y
    def pos_x(self):
        return self.x
    def pos_y(self):
        return self.y
    def get_coord(self, d):#如果是1，意味着向上走；如果是2，意味着向右走；如果是3，意味着向下走；如果是4，意味着向左走；
        if d<=4:
            x = self.x+(3-d) if d%2==0 else self.x
            y = self.y+(2-d) if d%2 else self.y
        else:
            x = self.x + 1 if d<=6 else self.x-1
            y = self.y + 1 if d == 8 or d==5 else self.y-1
        return x,y
    def get_dir(self, maze):#点的哪些方向可以经过
        for i in range(8):
            x, y = self.get_coord(self.dirs[i])
            if maze.get_val(x,y):
                continue
            else:
                self.d.append(self.dirs[i])
        return self.d

    def update_h_n(self, target):
        """
            计算h(n)
        """
        self.h_n = int(math.sqrt((target.x - self.x) ** 2 + (target.y - self.y) ** 2))
        return self.h_n

    def update_g_n(self, source):
        """
            计算g(n)
        """
        self.g_n = int(math.sqrt((source.x - self.x) ** 2 + (source.y - self.y) ** 2))
        return self.g_n
    def update_f_n(self, source, target):
        """
            计算f(n)
        """
        q = is_yongdu(self.x,self.y,self.flag)
        if q == 0:
            self.f_n = self.update_g_n(source) + self.update_h_n(target)
        elif q == '1':
            self.f_n = self.update_g_n(source) + self.update_h_n(target) + 6
        elif q == '2':
            self.f_n = self.update_g_n(source) + self.update_h_n(target) + 15
        elif q == '3':
            self.f_n = self.update_g_n(source) + self.update_h_n(target) + 25
        return self.f_n
    def get_adj_node(self, flag, source, target):
        """
            计算邻近的节点
        """
        if flag == 1:
            cur_node = Point(self.x, self.y+1,self.flag)
            cur_node.update_f_n(source, target)
            cur_node.parent = self
            return cur_node
        elif flag == 2:
            cur_node = Point(self.x+1, self.y,self.flag)
            cur_node.update_f_n(source, target)
            cur_node.parent = self
            return cur_node
        elif flag == 3:
            cur_node = Point(self.x, self.y - 1,self.flag)
            cur_node.update_f_n(source, target)
            cur_node.parent = self
            return cur_node
        elif flag == 4:
            cur_node = Point(self.x - 1, self.y,self.flag)
            cur_node.update_f_n(source, target)
            cur_node.parent = self
            return cur_node
        elif flag == 5:
            cur_node = Point(self.x + 1, self.y+1,self.flag)
            cur_node.update_f_n(source, target)
            cur_node.parent = self
            return cur_node
        elif flag == 6:
            cur_node = Point(self.x + 1, self.y-1,self.flag)
            cur_node.update_f_n(source, target)
            cur_node.parent = self
            return cur_node
        elif flag == 7:
            cur_node = Point(self.x -1, self.y-1,self.flag)
            cur_node.update_f_n(source, target)
            cur_node.parent = self
            return cur_node
        elif flag == 8:
            cur_node = Point(self.x - 1, self.y+1,self.flag)
            cur_node.update_f_n(source, target)
            cur_node.parent = self
            return cur_node
        else:
            return None
class Maze:
    def __init__(self, maze_str):
        maze_list = [[int(i) for i in x.strip().split(' ')] for x in maze_str] #将其变为二维列表
        self.maze = np.array(maze_list) #变成二维数组
        self.height, self.width = self.shape = self.maze.shape #分别获得高度和宽度的值

    def get_val(self,x,y):#返回maze对应的值
        return self.maze[x,y]

    def set_value(self, x,y,val):#将格子对应的值改成val
        self.maze[x,y] = val

class Solution:
    def __init__(self,maze_str,start,end,flag,save):
        self.maze = Maze(maze_str)#将字符串读入到Maze类
        self.start = Point(start[0],start[1],flag) #开始点
        self.end   = Point(end[0],end[1],flag) #结束点
        self.save = save
        self.open_list = {} #开表
        self.close_list = {} #闭表
    def save_maze1(self):
        os.system("cls")  # 清屏
        N = 10
        self.board = self.maze.maze.astype(np.uint8)  # 将二维数组里的数字转化为无符号整数，0 至 255
        self.board[self.board == 0] = 255
        self.board[self.board == 1] = 0
        self.board[self.board == 2] = 180  # 一开始不用 为了经过标记拓展路径
        self.board[self.board == 3] = 50  # 一开始不用 为了标记最佳路径
        self.board = self.board.repeat(N, 0).repeat(N, 1)  # 0意味着增加列数，1意味着增加行数
        cv2.imwrite('D:/ruanjian/image/1.jpg',self.board)  # 为了让大家看得清，把倍数扩大20，把图变大
        cv2.waitKey(1)
        # time.sleep(0.1)#给用户反应时间
    def save_maze2(self):
        os.system("cls")  # 清屏
        N = 10
        self.board = self.maze.maze.astype(np.uint8)  # 将二维数组里的数字转化为无符号整数，0 至 255
        self.board[self.board == 0] = 255
        self.board[self.board == 1] = 0
        self.board[self.board == 2] = 180  # 一开始不用 为了经过标记拓展路径
        self.board[self.board == 3] = 50  # 一开始不用 为了标记最佳路径
        self.board = self.board.repeat(N, 0).repeat(N, 1)  # 0意味着增加列数，1意味着增加行数
        cv2.imwrite('D:/ruanjian/image/2.jpg', self.board)  # 为了让大家看得清，把倍数扩大20，把图变大
        cv2.waitKey(1)
    def solve(self):
        self.open_list[str(self.start.pos_x) + '_' + str(self.start.pos_y)] = self.start#开表是字典，键对应的是坐标，值对应的是Point类
        self.maze.set_value(*self.start.pos,2) #把初始值设为2,数据类型为Maze类
        #self.print_maze()
        while self.open_list:
            tmp_dict = sorted(self.open_list.items(), key=lambda d: d[1].f_n)#根据开标中的Point类中的启发式函数的值，排序
            first_key = tmp_dict[0][0]  # 该点的位置
            #self.print_maze()
            first_point = self.open_list[first_key]  # 对应的point节点
            #self.maze.set_value(*first_point.pos, 2)
            if first_point.pos == self.end.pos:
                while first_point.pos != self.start.pos:#找回父亲节点找到正确路径
                    self.maze.set_value(*first_point.pos,2)
                    first_point = first_point.parent
                    #self.print_maze()
                if self.save == 0:
                    self.save_maze1()
                else:
                    self.save_maze2()
                print('done')
                break
            del self.open_list[first_key]#删除开表中这个节点
            if  first_key not in self.close_list:
                self.close_list[first_key] = first_point#如果闭表没有这个节点，加入闭表
            d = first_point.get_dir(self.maze)#获取该节点的四周可通过的方向
            for i in d:
                up_point = first_point.get_adj_node(i,self.start, self.end)#根据方向进行扩展节点
                index = str(up_point.x) + '_' + str(up_point.y)
                if index not in self.open_list and index not in self.close_list:#判断该点是否在表中
                    self.open_list[index] = up_point

#qlouti 前楼梯
#hlouti 后楼梯
def louti_panduan(start,end):#通过坐标计算欧几里得距离，判断从哪个楼梯走近
    S_q = int(math.sqrt((start[0]-2)**2+(start[1]-23)**2))
    S_h = int(math.sqrt((start[0]-21)**2+(start[1]-23)**2))
    E_q = int(math.sqrt((end[0]-2)**2+(end[1]-23)**2))
    E_h = int(math.sqrt((end[0] - 21) ** 2 + (end[1] - 23) ** 2))
    if (S_q+E_q)>=(S_h+E_h):
        return 1#返回1意味着从后楼梯下
    else:
        return 0
def main(start,end):
    panduan = 0
    start_float = find.getRoomInfo(start)#通过输入的教室判断起始教室坐标
    end_float = find.getRoomInfo(end)#通过输入的教室判断结束教室坐标
    if start_float[0] ==end_float[0]:#教室在同一层
        for i in range(len(R.Points)):
            if R.Points[i][0] == start_float[0]:
                start_manglu[R.Points[i].split("(")[1].split(")")[0]] = R.Points[i][-1] #字典 key：'x,y' value:'1/2/3'
        ss = 'D:/ruanjian/app01/A/maze'+ start_float[0]+'.txt'#打开这个起始楼层的01矩阵
        with open(ss, 'r') as foo:
            MAZE = foo.readlines()#把数据读入方阵里
        start = []
        end = []
        start.append(int(start_float[1].split("(")[1].split(",")[0]))#获取起始坐标x的值
        start.append(int(start_float[1].split(",")[1].split(")")[0]))#获取起始坐标y的值
        end.append(int(end_float[1].split("(")[1].split(",")[0]))#获取结束坐标x的值
        end.append(int(end_float[1].split(",")[1].split(")")[0]))#获取结束坐标y的值
        S = Solution(MAZE,start,end,0,0)#初始化Solution类
        S.solve()#解决问题
    else:#教室在不同一层
        panduan = panduan + 1
        for i in range(len(R.Points)):
            if R.Points[i][0] == start_float[0]:
                start_manglu[R.Points[i].split("(")[1].split(")")[0]] = R.Points[i][-1]
            elif R.Points[i][0] == end_float[0]:
                end_manglu[R.Points[i].split("(")[1].split(")")[0]] = R.Points[i][-1]
        start = []
        end = []
        start.append(int(start_float[1].split("(")[1].split(",")[0]))#获取起始坐标x的值
        start.append(int(start_float[1].split(",")[1].split(")")[0]))#获取起始坐标y的值
        end.append(int(end_float[1].split("(")[1].split(",")[0]))#获取结束坐标x的值
        end.append(int(end_float[1].split(",")[1].split(")")[0]))#获取结束坐标y的值
        if louti_panduan(start,end):#判断是否后楼梯近，否则用前楼梯
            ss = 'D:/ruanjian/app01/A/maze' + start_float[0] + '.txt'
            ee = 'D:/ruanjian/app01/A/maze' + end_float[0] + '.txt'
            louti = [21,23]#后楼梯坐标
            with open(ss, 'r') as foo:
                ss_MAZE = foo.readlines()#将开始层读入到其中
            with open(ee, 'r') as foo:
                ee_MAZE = foo.readlines()#将结束层读入到其中
            Solution(ss_MAZE, start,louti,0,save=0).solve()
            Solution(ee_MAZE, louti, end,1,save=1).solve()
        else:
            ss = 'D:/ruanjian/app01/A/maze' + start_float[0] + '.txt'
            ee = 'D:/ruanjian/app01/A/maze' + end_float[0] + '.txt'
            louti = [2, 23]#前楼梯近
            with open(ss, 'r') as foo:
                ss_MAZE = foo.readlines()
            with open(ee, 'r') as foo:
                ee_MAZE = foo.readlines()
            Solution(ss_MAZE, start, louti,flag=0,save=0).solve()
            Solution(ee_MAZE, louti, end,flag=1,save=1).solve()
    return panduan
