import cv2
import json
from web3 import Web3
from pyzbar.pyzbar import decode
import pyqrcode
import tkinter as tk
from time import sleep

from datetime import datetime
import numpy as np
import random
ganach_url = "http://127.0.0.1:7545"
web3 = Web3(Web3.HTTPProvider(ganach_url))
web3.eth.defaultAccount = web3.eth.accounts[1]


abi = json.loads('[{"inputs":[],"name":"GET_CURRNT_TEMP","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"string","name":"CID","type":"string"},{"internalType":"string","name":"TID","type":"string"}],"name":"addCar_TransactionID","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"string","name":"_sa","type":"string"},{"internalType":"string","name":"_nS","type":"string"},{"internalType":"string","name":"tx","type":"string"}],"name":"addSupplier","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"string","name":"TID","type":"string"},{"internalType":"string","name":"Sdate","type":"string"}],"name":"add_End_time_ToTransction","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"string","name":"TID","type":"string"},{"internalType":"string","name":"Sdate","type":"string"}],"name":"add_Start_time_ToTransction","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"string","name":"TID","type":"string"},{"internalType":"string","name":"UID","type":"string"}],"name":"add_Uints_ToTransction","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"string","name":"TID","type":"string"},{"internalType":"string","name":"temp","type":"string"}],"name":"add_temp","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"cdate","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"string","name":"_sa","type":"string"},{"internalType":"string","name":"_da","type":"string"}],"name":"dateSupplier","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"end","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"string","name":"z","type":"string"}],"name":"erase","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"string","name":"_name","type":"string"},{"internalType":"string","name":"_code","type":"string"},{"internalType":"string","name":"_sup","type":"string"},{"internalType":"string","name":"_date","type":"string"},{"internalType":"string","name":"_am","type":"string"},{"internalType":"string","name":"_typ","type":"string"},{"internalType":"string","name":"tx","type":"string"}],"name":"factory","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"string","name":"z","type":"string"}],"name":"getindex","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"show","outputs":[{"internalType":"string","name":"","type":"string"},{"internalType":"string","name":"","type":"string"},{"internalType":"string","name":"","type":"string"},{"internalType":"string","name":"","type":"string"},{"internalType":"string","name":"","type":"string"},{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"show_Track","outputs":[{"internalType":"string","name":"","type":"string"},{"internalType":"string","name":"","type":"string"},{"internalType":"string","name":"","type":"string"},{"internalType":"string","name":"","type":"string"},{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"string","name":"TID","type":"string"}],"name":"start_trac","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"suplly1","outputs":[],"stateMutability":"nonpayable","type":"function"}]')
address = web3.toChecksumAddress("0x6Bfd0eB49c83A6367bDD09C519Cfb59E259551c3")
contract = web3.eth.contract(address=address , abi= abi)

def scaner1():
    cn = 0

    cap = cv2.VideoCapture(0)
    cap.set(3, 640)
    cap.set(4, 480)
    f = True
    nstr = 0
    while f and cn < 100:
        sleep(0.1)
        cn += 1
        success, img = cap.read()
        for barcode in decode(img):
            myData = barcode.data.decode('utf-8')
            print(myData)
            if len(myData) > 3:
                f = False
                nstr = 1

            pts = np.array([barcode.polygon], np.int32)
            pts = pts.reshape((-1, 1, 2))
            cv2.polylines(img, [pts], True, (255, 0, 255), 5)
            pts2 = barcode.rect
            cv2.putText(img, myData, (pts2[0], pts2[1]), cv2.FONT_HERSHEY_SIMPLEX,
                        0.9, (255, 0, 255), 2)

        cv2.imshow('QRCODE', img)
        cv2.waitKey(1)
    cap.release()  #################
    cv2.destroyAllWindows()
    if nstr == 0:
        return 'no'
    else:
        return myData

choices = list(range(52, 80))
random.shuffle(choices)
def getQR():
    x = choices.pop()
    y = choices.pop()
    code = x * y
    qr = pyqrcode.create(str(code))
    print(qr)
    qr.png(str(code) + '.png', scale=8)
    return str(code)
def ui():

    def factoryx():
        Mname = entery11.get()
        amunt = entery12.get()
        Type = entery13.get()
        Fro = entery14.get()
        To = entery15.get()
        con=Fro+"-"+To+"-"
        trx1=enteryx15.get()
        trx1 = trx1 + "-"
        now = datetime.today().strftime('%Y-%m-%d')
        dat = now + "/"
        tx_hash = contract.functions.factory(Mname, getQR(),con, dat,amunt,Type,trx1).transact()
        print(dat)

    def shoow():
        qr = scaner1()
        print(qr)
        if qr != 'no':
            tx_hash = contract.functions.getindex(qr).transact()
            z = contract.functions.show().call()
            lbl16.config(text="{}  ".format(z),
                         bg='#67a5b9')
            lbl16.place(x=20,y=230,width=520,height=25)
            # lbl16.grid(row=6, column=3)
    def erres():
        qr = scaner1()
        print(qr)
        if qr != 'no':
            tx_hash = contract.functions.erase(qr).transact()
            z = contract.functions.show().call()
            print(z)




    root = tk.Tk()
    root.title("Factory")
    root.geometry("630x340")
    root['bg'] = '#76b7cc'

    lbl11 = tk.Label()
    lbl11.config(text=' medicine name  ',bg='#67a5b9')
    lbl11.grid(row=0, column=0)

    lbl12 = tk.Label()
    lbl12.config(text='  amount ',bg='#67a5b9')
    lbl12.grid(row=0 , column=1)

    lbl13 = tk.Label()
    lbl13.config(text='   type  ',bg='#67a5b9')
    lbl13.grid(row=0, column=2)

    entery11 = tk.Entry(width=11)
    entery11.grid(row=1, column=0)

    entery12 = tk.Entry(width=6)
    entery12.grid(row=1, column=1)

    entery13 = tk.Entry(width=4)
    entery13.grid(row=1, column=2)

    supl = tk.Label()
    supl.config(text='   supplier   ',bg='#67a5b9')
    supl.grid(row=2, column=0)

    lbl14 = tk.Label()
    lbl14.config(text='from : ',bg='#67a5b9')
    lbl14.grid(row=3, column=0)
    entery14 = tk.Entry(width=9)
    entery14.grid(row=3, column=1)
    lbl15 = tk.Label()
    lbl15.config(text=' to :   ',bg='#67a5b9')
    lbl15.grid(row=4, column=0)
    entery15 = tk.Entry(width=9)
    entery15.grid(row=4, column=1)
    lblx15 = tk.Label()
    lblx15.config(text=' Trans. ID :   ',bg='#67a5b9')
    lblx15.grid(row=5, column=0)
    enteryx15 = tk.Entry(width=9)
    enteryx15.grid(row=5, column=1)

    btn1 = tk.Button(text="add",bg='#8ea6af', fg='black', command=factoryx)
    btn1.grid(row=6, column=1)
    btn2 = tk.Button(text="show",bg='#8ea6af', fg='black', command=shoow)
    btn2.grid(row=7, column=0)
    btn3 = tk.Button(text="Delete",bg='#8ea6af', fg='black', command=erres)
    btn3.grid(row=8, column=1)

    lbl16 = tk.Label()




    root.mainloop()

ui()
