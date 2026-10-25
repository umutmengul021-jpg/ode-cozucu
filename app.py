import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from numpy import sin, cos, tan, exp, log, sqrt, pi   # kullanıcı sin(x), exp(x) yazabilsin diye

tablo={"euler":{"c":[0],
                "a":[[0]],
                "b":[1]},
       "rk4":{"c":[0,1/2,1/2,1],
              "a":[[0,  0,  0,0],
                   [1/2,0,  0,0],
                   [0,  1/2,0,0],
                   [0,  0,  1,0]],
              "b":[1/6,2/6,2/6,1/6]}}

def çözücü_çekirdek(x0,y0,f,xson,adım_sayısı,tablo):
    h=(xson-x0)/(adım_sayısı)
    y=np.zeros(adım_sayısı+1)
    x=np.zeros(adım_sayısı+1)
    y[0]=y0
    x[0]=x0
    c=np.array(tablo["c"])
    b=np.array(tablo["b"])
    a=np.array(tablo["a"])
    for i in range(adım_sayısı):
        k=np.zeros(len(b))
        for j in range(len(c)):
            yy=y[i]+h*np.sum(a[j]*k)
            k[j]=f(x[i]+c[j]*h,yy)
        y[i+1]=y[i]+h*np.sum(k*b)
        x[i+1]=x[i]+h
    return x,y

# ---------------- sayfa ----------------
st.title("Diferansiyel Denklem Çözücü")
st.write("y' = f(x, y) biçimindeki denklemi Python yazımıyla girin (örnek: x + y, -2*x*y, cos(x))")

denklem=st.text_input("y' =","x + y")
analitik_yazı=st.text_input("Analitik çözüm (bilmiyorsanız boş bırakın)","2*exp(x) - x - 1")
x0=st.number_input("x0",value=0.0)
y0=st.number_input("y0",value=1.0)
xson=st.number_input("x son",value=2.0)
adım_sayısı=st.number_input("adım sayısı",value=10,step=1)
yöntemler=st.multiselect("yöntem",list(tablo.keys()),default=["euler","rk4"])

if st.button("Çöz"):
    try:
        f=lambda x,y: eval(denklem)
        fig,ax=plt.subplots()
        if analitik_yazı!="":
            x=np.linspace(x0,xson,200)
            ax.plot(x,eval(analitik_yazı),"k-",label="analitik")
        for yöntem in yöntemler:
            x_s,y_s=çözücü_çekirdek(x0,y0,f,xson,int(adım_sayısı),tablo[yöntem])
            ax.plot(x_s,y_s,"o--",label=yöntem)
            st.write(yöntem,": x =",x_s[-1],"için y =",y_s[-1])
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.grid(True)
        ax.legend()
        st.pyplot(fig)
    except Exception as hata:
        st.error(hata)
