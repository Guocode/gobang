#!/usr/bin/python3
# -*- coding: utf-8 -*-
 
"""
Py40.com PyQt5 tutorial 
 
In this example, we create a simple
window in PyQt5.
 
author: Jan Bodnar
website: py40.com 
last edited: January 2015
"""
 
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton ,QLabel, QLineEdit, QCheckBox ,QRadioButton ,QComboBox
from PyQt5.QtGui import QPainter,QColor,QPen, QPixmap,QIcon
from PyQt5.QtCore import Qt
import numpy as np
from PyQt5.Qt import QFont,QDialog

class Chess():
    def __init__(self,owner=0,pos=0):
        self.owner = owner
        self.pos = pos

class Chessboard(object):
    status = np.zeros(225) #15*15的棋盘状态 0代表无棋 1代表黑棋 2代表白棋 黑先白后
    turn = 0 # 0代表未开始或已结束 1代表黑棋下 2代表白棋下
    step = -1 # 步数
    status_history = [] # 历史记录
    def __init__(self, status = np.zeros(225), turn = 0):
        self.status = status
        self.turn = turn
    def resetBoard(self):
        self.turn = 0
        self.step = -1
        self.status = np.zeros(225)
        self.status_history.clear()
    def oneStep(self,chess):
        self.status[chess.pos] = chess.owner
        self.step+=1
        if self.turn==1:
            self.turn = 2
        else:
            self.turn = 1
    def checkWin(self):

        #按行按列按斜对角搜索
        for i in range(15):
            l_count = 1
            c_count = 1
            for j in range(14):
                l = i * 15 + j #按行
                if(self.status[l]==self.status[l+1] and self.status[l]!=0):
                    l_count+=1
                else:
                    l_count = 1
                if l_count==5:
                    return self.status[l] 
                
                c = j * 15 + i #按列
                if(self.status[c]==self.status[c+15] and self.status[c]!=0):
                    c_count+=1
                else:
                    c_count = 1
                if c_count==5:
                    return self.status[c] 
        
        for i in range(11):#左斜对角线\
            ld_count = 1
            ld_count0 = 1
            j = 0
            while i<=13:
                if(self.status[i*15+j]==self.status[(i+1)*15+j+1] and self.status[i*15+j]!=0):
                    ld_count+=1
                else:
                    ld_count = 1
                if ld_count==5:
                    return self.status[i*15+j]
                
                if(self.status[j*15+i]==self.status[(j+1)*15+i+1] and self.status[j*15+i]!=0):
                    ld_count0+=1
                else:
                    ld_count0 = 1
                if ld_count0==5:
                    return self.status[j*15+i]
                j+=1
                i+=1

        for i in range(11):#右斜对角线/
            rd_count = 1
            rd_count0 = 1
            j = 0
            while i<=13:
                if(self.status[i*15+14-j]==self.status[(i+1)*15+14-j-1] and self.status[i*15+14-j]!=0):
                    rd_count+=1
                else:
                    rd_count = 1
                if rd_count==5:
                    return self.status[i*15+14-j]
                
                if(self.status[j*15+14-i]==self.status[(j+1)*15+14-i-1] and self.status[j*15+14-i]!=0):
                    rd_count0+=1
                else:
                    rd_count0 = 1
                if rd_count0==5:
                    return self.status[j*15+14-i]
                j+=1
                i+=1 
                       
        if ((self.status!=0).all()): #棋盘放满了 平局
            return 0
        return -1 #0表示平局 1表示黑棋胜 2表示白棋胜 -1表示未定胜负
    def regretOneStep(self):
        pass
    
class WuziqiUI(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI() #界面绘制交给InitUi方法
        self.Chessboard = Chessboard()
        self.Chess_group = []
        self.mode = 0 #0代表双人对战 1代表人机对战
        while():
            pass
        
    def initUI(self):
        self.chess_black = QPixmap("chess_black.png")
        self.chess_white = QPixmap("chess_white.png")
        #设置窗口的位置和大小
        self.setFixedSize(800,650)
        #设置窗口的标题
        self.setWindowTitle('五子棋')
        #设置窗口的图标，引用当前目录下的图片
        self.setWindowIcon(QIcon('cover.jpg'))        
        self.btn_start = QPushButton('开始游戏', self)
        self.btn_start.setGeometry(680,20,80,30)
        self.btn_start.clicked.connect(self.startGame)
        self.btn_reset = QPushButton('重置', self)
        self.btn_reset.clicked.connect(self.resetGame)
        self.btn_reset.setGeometry(680,80,80,30)
        self.btn_regret = QPushButton('悔棋', self)
        self.btn_regret.setGeometry(680,140,80,30)
        self.btn_regret.setVisible(False)
        #选择模式 人机对战还是人人对战
        self.modesele = QComboBox(self)
        self.modesele.addItem("双人对战")
        self.modesele.addItem("人机对战")
        self.modesele.move(680,260)
        self.modesele.activated[str].connect(self.selectMode)
        self.cb1 = QRadioButton('我先走',self)
        self.cb2 = QRadioButton('机器先走',self)
        self.cb1.move(680, 300)
        self.cb2.move(680, 320)
        self.cb1.toggle()
        self.cb1.setEnabled(False)
        self.cb2.setEnabled(False)
        self.setGeometry(300, 300, 250, 150)
        self.lbl = QLabel(self)
        self.lbl.move(680, 200)
        self.lbl.setText('请点击开始游戏！')
        self.lbl_turn = QLabel(self)
        self.lbl_turn.move(680, 222)
        self.lbl_turn.setText('')
        self.lbl_help = QLabel(self)
        self.lbl_help.move(700, 600)
        self.lbl_help.setText('作者:G_zh')
        #显示窗口
        self.show()
        
    def paintEvent(self, e): 
        qp = QPainter()
        qp.begin(self)
        self.paintBG(qp)
        self.paintLine(qp)
        qp.end()  
            
    def paintBG(self,qp):
        col = QColor()
        col.setNamedColor('#ffffff')
        qp.setPen(col)
        qp.setBrush(QColor(0, 120, 0))
        qp.drawRect(3, 3, 644, 644)
    
    def paintLine(self,qp):
        pen = QPen(Qt.black, 1, Qt.SolidLine)
        qp.setPen(pen)
        line_dis = 40
        for i in range(15):
            qp.drawLine(40, line_dis*(i+1), 600, line_dis*(i+1))
            qp.drawLine(line_dis*(i+1), 40, line_dis*(i+1), 600)
            
    def paintChess(self,qp,chess):
        lbl0 = QLabel(self)
        if chess.owner==1:
            lbl0.setPixmap(self.chess_black)
        else:
            lbl0.setPixmap(self.chess_white)
        lbl0.setScaledContents(True)
        lbl0.setFixedSize(40,40)
        lbl0.move(chess.pos%15 * 40 + 20,chess.pos//15 *40 + 20)
        lbl0.setVisible(True)
        self.Chess_group.append(lbl0)
        print('完成画棋子动作')
        return
    
    def mousePressEvent(self, e):
        if (e.x()>20 and e.x()<620)and(e.y()>20 and e.y()<620) and (self.Chessboard.turn!=0): #在棋盘内点击并且游戏已经开始
            new_x = ((e.x()%40>20)+e.x()//40)
            new_y = ((e.y()%40>20)+e.y()//40)
            new_pos=(new_y-1)*15+new_x-1
            if self.Chessboard.status[new_pos]!=0:#判断此处是否已经落子
                print('此处已经有落子')
                return
            new_chess = Chess(owner=self.Chessboard.turn,pos=new_pos)
            #画棋子
            qp = QPainter()
            qp.begin(self)
            self.paintChess(qp, new_chess)
            qp.end()
            #更新棋盘状态
            self.Chessboard.oneStep(new_chess) #下完一步棋
            text = '当前步数：'+self.Chessboard.step.__str__()
            self.lbl.setText(text) #当前步数 谁的回合
            #判断是否结束
            if self.Chessboard.checkWin()==-1:
                pass
            elif self.Chessboard.checkWin()==0:
                self.lbl_turn.setText('<平局！>')
                self.lbl_turn.adjustSize()
                self.Chessboard.turn = 0
                return
            elif self.Chessboard.checkWin()==1:
                self.lbl_turn.setText('<黑棋获胜！>')
                self.lbl_turn.adjustSize()
                self.Chessboard.turn = 0
                return
            elif self.Chessboard.checkWin()==2:
                self.lbl_turn.setText('<白棋获胜!>')
                self.lbl_turn.adjustSize()
                self.Chessboard.turn = 0
                return
            else:         
                return     

            if self.Chessboard.turn == 1:
                self.lbl_turn.setText('<黑棋回合>')
                self.lbl_turn.adjustSize()
            else:
                self.lbl_turn.setText('<白棋回合>')
                self.lbl_turn.adjustSize()  
                              
    def startGame(self):
        if(self.Chessboard.turn==0):
            self.Chessboard.turn = 1
            self.Chessboard.step = 0
            text = '当前步数：'+self.Chessboard.step.__str__()
            self.lbl.setText(text) #当前步数 谁的回合
            self.lbl_turn.setText('<黑棋回合>')
            self.lbl_turn.adjustSize()
            print('start!')
        else:
            print('already start!') 
        self.btn_start.setEnabled(False)
        
    def resetGame(self):
        self.Chessboard.resetBoard()
        for chess_ui in self.Chess_group:
            chess_ui.setVisible(False)
        self.Chess_group.clear()
        self.lbl.setText('请点击开始游戏！')
        self.lbl_turn.setText('')
        self.btn_start.setEnabled(True)
        return    
    
    def selectMode(self,str):
        if str=="双人对战":
            self.modesele = 0
            self.cb1.setEnabled(False)
            self.cb2.setEnabled(False)
        else:
            self.modesele = 1
            self.cb1.setEnabled(True)
            self.cb2.setEnabled(True)
            
if __name__ == '__main__':
    #每一pyqt5应用程序必须创建一个应用程序对象。sys.argv参数是一个列表，从命令行输入参数。
    app = QApplication(sys.argv)
    #QWidget部件是pyqt5所有用户界面对象的基类。他为QWidget提供默认构造函数。默认构造函数没有父类。
    w = WuziqiUI()
    sys.exit(app.exec_())