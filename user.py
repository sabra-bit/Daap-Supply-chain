import cv2
import json
from web3 import Web3
from pyzbar.pyzbar import decode
import pyqrcode
import tkinter as tk
from time import sleep

from datetime import datetime
import numpy as np

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


def ui():
    def shoow():
        qr = scaner1()
        print(qr)
        if qr != 'no':
            tx_hash = contract.functions.getindex(qr).transact()
            z = contract.functions.show().call()
            lbl12.config(text="{}  ".format(z),
                         bg='#67a5b9')
            lbl12.place(x=10,y=70,width=520,height=25)

    root = tk.Tk()
    root.title("Factory")
    root.geometry("530x140")
    root['bg'] = '#76b7cc'
    lbl11 = tk.Label()
    lbl11.config(text=' check your medicine  ', bg='#67a5b9')
    lbl11.grid(row=0, column=0)



    btn1 = tk.Button(text="scane", bg='#8ea6af', fg='black', command=shoow)
    btn1.grid(row=1, column=0)

    lbl12 = tk.Label()



    root.mainloop()

ui()