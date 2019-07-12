import serial
import tkinter as tk
from tkinter.messagebox import showinfo
from tkinter import ttk
from serial import serialutil

if __name__ == "__main__":
    #  连接响应
    ser = serial.Serial()
    ser.timeout = 2


    def Connect(ser):
        ser.baudrate = 19200
        if comboxlist.current()==0:
            ser.port = 'COM1'
            ser.open()
            if (ser.is_open == True):
                showinfo('连接', '已打开串口1！')
        if comboxlist.current()==1:
            ser.port = 'COM2'
            ser.open()
            if (ser.is_open == True):
                showinfo('连接', '已打开串口2！')
        if comboxlist.current()==2:
            ser.port = 'COM3'
            ser.open()
            if (ser.is_open == True):
                showinfo('连接', '已打开串口3！')
        if comboxlist.current()==3:
            ser.port = 'COM4'
            ser.open()
            if (ser.is_open == True):
                showinfo('连接', '已打开串口4！')
        if comboxlist.current()==4:
            ser.port = 'COM5'
            ser.open()
            if (ser.is_open == True):
                showinfo('连接', '已打开串口5！')
        if comboxlist.current()==5:
            ser.port = 'COM6'
            ser.open()
            if (ser.is_open == True):
                showinfo('连接', '已打开串口6！')
        ##else:
           ## showinfo('连接', '连接失败，请检查连接！')


    def Judgescore(top):
        txt = '100'
        entry8.delete(0, 100)
        entry8.insert('0', txt)


    def Sign(top):
        txt = '李坤豪 匡成'
        entry9.delete(0, 100)
        entry9.insert('0', txt)


    def Readdata(ser):
        #  置空闲状态
        cmd1 = [0xAA, 0xBB, 0x03, 0x12, 0x00, 0x11]
        #  置工作状态
        cmd2 = [0xAA, 0xBB, 0x03, 0x11, 0x03, 0x11]
        #  1区1块学号
        cmd3 = [0xAA, 0xBB, 0x0A, 0x21, 0x00, 0x04, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0x2F]
        #  1区2块学号
        cmd4 = [0xAA, 0xBB, 0x0A, 0x21, 0x00, 0x05, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0x2E]
        #  0区0块
        cmd5 = [0xAA, 0xBB, 0x0A, 0x21, 0x00, 0x00, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0x2B]
        #  0区1块
        cmd6 = [0xAA, 0xBB, 0x0A, 0x21, 0x00, 0x01, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0x2A]
        #  2区0块钱包一
        cmd7 = [0xAA, 0xBB, 0x0A, 0x21, 0x00, 0x08, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0x23]
        #  2区1块钱包二
        cmd8 = [0xAA, 0xBB, 0x0A, 0x21, 0x00, 0x09, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0x22]
        if (ser.is_open == True):
            d1=send_cmd(ser, cmd1)
            print("置空闲：",d1)
            data = send_cmd(ser, cmd2)
            print("置工作：",data)
            data1 = send_cmd(ser, cmd3)
            data2 = send_cmd(ser, cmd4)
            data3 = send_cmd(ser, cmd5)
            data4 = send_cmd(ser, cmd6)
            data5 = send_cmd(ser, cmd7)
            data6 = send_cmd(ser, cmd8)
            print('1区1块学号：', data1)
            print('1区2块学号：', data2)
            entry1.delete(0, 100)  # deletes the current value
            entry1.insert(0, data1)  # inserts new value assigned by 2nd parameter
            entry2.delete(0, 100)  # deletes the current value
            entry2.insert(0, data2)  # inserts new value assigned by 2nd parameter
            entry3.delete(0, 100)  # deletes the current value
            entry3.insert(0, data3)  # inserts new value assigned by 2nd parameter
            entry4.delete(0, 100)  # deletes the current value
            entry4.insert(0, data4)  # inserts new value assigned by 2nd parameter
            entry5.delete(0, 100)  # deletes the current value
            entry5.insert(0, data5)  # inserts new value assigned by 2nd parameter
            entry6.delete(0, 100)  # deletes the current value
            entry6.insert(0, data6)  # inserts new value assigned by 2nd parameter

    def helloCallBack4(top):
        print("Hello World4!")


    # 发送指令的完整流程
    def send_cmd(ser, cmd):
        ser.write(cmd)
        response = ser.readline()
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


    top = tk.Tk()
    top.title("lkh的串口调试助手")
    top.minsize(540, 600)
    #  标签
    label1 = ttk.Label(top, text="0001:", width=10)
    label1.place(x=10, y=50)
    label2 = ttk.Label(top, text="0002:", width=10)
    label2.place(x=10, y=80)
    label3 = ttk.Label(top, text="0区0块:", width=10)
    label3.place(x=10, y=110)
    label4 = ttk.Label(top, text="0区1块:", width=10)
    label4.place(x=10, y=140)
    label5 = ttk.Label(top, text="2区0块:", width=10)
    label5.place(x=10, y=170)
    label6 = ttk.Label(top, text="2区1块:", width=10)
    label6.place(x=10, y=200)
    label7 = ttk.Label(top, text="2区2块:", width=10)
    label7.place(x=10, y=230)
    label8 = ttk.Label(top, text="得分:", width=10)
    label8.place(x=300, y=50)
    label9 = ttk.Label(top, text="签名:", width=10)
    label9.place(x=300, y=150)

    #  文本框
    entry1 = ttk.Entry(top)
    entry1.place(x=60, y=50)
    entry2 = ttk.Entry(top)
    entry2.place(x=60, y=80)
    entry3 = ttk.Entry(top)
    entry3.place(x=60, y=110)
    entry4 = ttk.Entry(top)
    entry4.place(x=60, y=140)
    entry5 = ttk.Entry(top)
    entry5.place(x=60, y=170)
    entry6 = ttk.Entry(top)
    entry6.place(x=60, y=200)
    entry7 = ttk.Entry(top)
    entry7.place(x=60, y=230)
    entry8 = ttk.Entry(top)
    entry8.place(x=350, y=50)
    entry9 = ttk.Entry(top)
    entry9.place(x=350, y=150)

    #  按钮
    button1 = ttk.Button(top, text="连接", command=lambda: Connect(ser), width=10)
    button1.place(x=10, y=10)
    button2 = ttk.Button(top, text="读数据", command=lambda: Readdata(ser), width=10)
    button2.place(x=230, y=10)
    button3 = ttk.Button(top, text="评分", command=lambda: Judgescore(top), width=10)
    button3.place(x=330, y=10)
    button4 = ttk.Button(top, text="保存", command=lambda: helloCallBack4(top), width=10)
    button4.place(x=430, y=10)
    button5 = ttk.Button(top, text="签名", command=lambda: Sign(top), width=10)
    button5.place(x=415, y=200)

    number=tk.StringVar()
    comboxlist=ttk.Combobox(top,values=('com1','com2','com3','com4','com5','com6'),state='readonly',width=10,textvariable=number)
    comboxlist.current(3)
    comboxlist.place(x=100,y=12)

    # 进入消息循环
    top.mainloop()
