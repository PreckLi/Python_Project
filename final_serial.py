import serial
import tkinter as tk
from tkinter.messagebox import showinfo
from tkinter import ttk
import sqlite3
from tkinter import *
from serial import serialutil

#  连接响应
ser = serial.Serial()
ser.timeout = 2
CmdName = []
CmdCode = []
Cmd = []
NeedChange = []
#  建立幕布
top = tk.Tk()
top.title("Final Serial Port Debugging Assistant")
top.minsize(540, 600)
# open database
conn = sqlite3.connect('command.db')
#  showinfo("助手提示","连接数据库成功!")
c = conn.cursor()
cursor = c.execute("SELECT CmdName,CmdCode,Cmd,NeedChange from cmdlist")
for row in cursor:
    CmdName.append(row[0])
    CmdCode.append(row[1])
    Cmd.append(row[2])
    NeedChange.append(row[3])
conn.close()

def Connect(ser):
    ser.baudrate = 19200
    if comboxlist.current() == 0:
        ser.port = 'COM9'
        ser.open()
        if (ser.is_open == True):
            showinfo('连接', '已打开串口9！')
    if comboxlist.current() == 1:
        ser.port = 'COM10'
        ser.open()
        if (ser.is_open == True):
            showinfo('连接', '已打开串口10！')
    if comboxlist.current() == 2:
        ser.port = 'COM7'
        ser.open()
        if (ser.is_open == True):
            showinfo('连接', '已打开串口7！')
    if comboxlist.current() == 3:
        ser.port = 'COM4'
        ser.open()
        if (ser.is_open == True):
            showinfo('连接', '已打开串口4！')
    if comboxlist.current() == 4:
        ser.port = 'COM5'
        ser.open()
        if (ser.is_open == True):
            showinfo('连接', '已打开串口5！')
    if comboxlist.current() == 5:
        ser.port = 'COM6'
        ser.open()
        if (ser.is_open == True):
            showinfo('连接', '已打开串口6！')
    # else:
    # showinfo('连接', '连接失败，请检查连接！')

def PrintCmd(Cmd):
    # value2 = entry2.get()
    # print(value2)
    print("comboxlist的值：",comboxlist1.get())
    # Num=comboxlist1.current()
    #  connect database
    conn = sqlite3.connect('command.db')
    c = conn.cursor()
    cursor=c.execute("SELECT Cmd from cmdlist where CmdName='"+comboxlist1.get()+"'")
    rs=cursor.fetchone()
    # 转换元组类型为字符串
    print(type(rs))
    rs=list(rs)
    "".join(list(rs))
    print("rs:",rs)
    for i in rs:
        str(i)
    print("i:",i)
    cursor1 = c.execute("SELECT NeedChange from cmdlist where CmdName='" + comboxlist1.get() + "'")
    rs1=cursor1.fetchone()
    rs1 = list(rs1)
    "".join(list(rs1))
    for i1 in rs1:
        str(i1)
    print("i1",i1)
    if i1=='1':
        label6 = ttk.Label(top, text="需要添加指令代码", width=15)
        label6.place(x=70, y=228)
    if i1=='0':
        label6 = ttk.Label(top, text="可直接使用代码", width=15)
        label6.place(x=70, y=228)
    entry2.delete(0, 100)  # deletes the current value
    entry2.insert(0, i)  # inserts new value assigned by 2nd parameter

def Judgescore(top):
    txt = '100'
    entry8.delete(0, 100)
    entry8.insert('0', txt)

def ClearText(top):
    textfield.delete(0.0,5000.0)

def ClearCmd():
    entry2.delete(0,100)
    label6 = ttk.Label(top, text="", width=15)
    label6.place(x=70, y=228)

def Senddata(ser):
    # #  置空闲状态
    # cmd1 = [0xAA, 0xBB, 0x03, 0x12, 0x00, 0x11]
    # #  置工作状态
    # cmd2 = [0xAA, 0xBB, 0x03, 0x11, 0x03, 0x11]
    # #  1区1块学号
    # cmd3 = [0xAA, 0xBB, 0x0A, 0x21, 0x00, 0x04, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0x2F]
    # #  1区2块学号
    # cmd4 = [0xAA, 0xBB, 0x0A, 0x21, 0x00, 0x05, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0x2E]
    # #  0区0块
    # cmd5 = [0xAA, 0xBB, 0x0A, 0x21, 0x00, 0x00, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0x2B]
    # #  0区1块
    # cmd6 = [0xAA, 0xBB, 0x0A, 0x21, 0x00, 0x01, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0x2A]
    # #  2区0块钱包一
    # cmd7 = [0xAA, 0xBB, 0x0A, 0x21, 0x00, 0x08, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0x23]
    # #  2区1块钱包二
    # cmd8 = [0xAA, 0xBB, 0x0A, 0x21, 0x00, 0x09, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0x22]
    cmd=entry2.get()
    cmdlist=cmd.split(' ')
    for i in cmdlist:
        print(i)
    cmdlist1=[]
    print(cmdlist)
    for i in cmdlist:
        i=int(i,16)
        cmdlist1.append(i)
    print(cmdlist1)
    print(type(cmdlist1))
    if ser.is_open == True:
        res=send_cmd(ser,cmdlist1)
        print('res:',res)
        textfield.insert(INSERT, res)


# 发送指令的完整流程
def send_cmd(ser, cmd):
    ser.write(cmd)
    response = ser.readall()
    response = convert_hex(response)
    return response

# 转成16进制的函数
def convert_hex(string):
    res = []
    result = []
    for item in string:
        res.append(item)
    for i in res:
        result.append(hex(i))
    return result

#  标签
label1 = ttk.Label(top, text="RFID串口调试助手", font=30)
label1.place(x=170, y=30)
label2 = ttk.Label(top, text="选择串口:", width=10)
label2.place(x=10, y=82)
label3 = ttk.Label(top, text="得分:", width=10)
label3.place(x=280, y=82)
label4 = ttk.Label(top, text="选择指令:", width=10)
label4.place(x=10, y=140)
label5 = ttk.Label(top, text="指令代码:", width=10)
label5.place(x=10, y=200)
label7 = ttk.Label(top, text="指令接收:", width=10)
label7.place(x=10, y=280)
# label9 = ttk.Label(top, text="签名:", width=10)
# label9.place(x=300, y=150)

#  文本框
entry8 = ttk.Entry(top)
entry8.place(x=320, y=80, width=50)
entry2 = ttk.Entry(top)
entry2.place(x=70, y=200,width=450)
textfield=tk.Text(top, wrap='word', width=50, height=15)
textfield.place(x=70, y=280,height=200,width=450)
# entry4 = ttk.Entry(top)
# entry4.place(x=60, y=140)
# entry5 = ttk.Entry(top)
# entry5.place(x=60, y=170)
# entry6 = ttk.Entry(top)
# entry6.place(x=60, y=200)
# entry7 = ttk.Entry(top)
# entry7.place(x=60, y=230)
# entry8 = ttk.Entry(top)
# entry8.place(x=350, y=50)
# entry9 = ttk.Entry(top)
# entry9.place(x=350, y=150)

#  按钮
button1 = ttk.Button(top, text="连接", command=lambda: Connect(ser), width=10)
button1.place(x=142, y=78)
button2 = ttk.Button(top, text="清空代码", command=lambda: ClearCmd(), width=10)
button2.place(x=350, y=230)
button3 = ttk.Button(top, text="评分", command=lambda: Judgescore(top), width=10)
button3.place(x=390, y=78)
button4 = ttk.Button(top, text="确认", command=lambda: PrintCmd(Cmd), width=10)
button4.place(x=430, y=138)
button6 = ttk.Button(top, text="发送指令", command=lambda: Senddata(ser), width=10)
button6.place(x=440, y=230)
button5 = ttk.Button(top, text="清空接收框", command=lambda: ClearText(top), width=10)
button5.place(x=440, y=490)

number1 = tk.StringVar()
comboxlist = ttk.Combobox(top, values=('com9', 'com10', 'com7', 'com4', 'com5', 'com6'),
                          state='readonly', width=6, textvariable=number1)
comboxlist.current(3)
comboxlist.place(x=70, y=80)

number2 = tk.StringVar()
comboxlist1 = ttk.Combobox(top, values=CmdName, state='readonly', width=45, textvariable=number2)
comboxlist1.current(0)
# comboxlist1.bind("<<ComboboxSelected>>", go)
comboxlist1.place(x=70, y=140)

if __name__ == "__main__":
    # 进入消息循环
    top.mainloop()
