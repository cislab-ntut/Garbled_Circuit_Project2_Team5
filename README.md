# Project5-2_Garbled_circuit
# g^x mod p


|核心概念 | 優點 | 缺點 |
| -------- | -------- | -------- |
| 連加&連減     | 實作簡單     | 速度慢     |
## 流程
先將所有的電路產生出來，並依層數另存為json檔以避免記憶體爆炸
總共會做(x-1) * (g-1)次g^i + g^i，i=1....x-1
將g^x算出來後會進行連減，每次會判斷當前的值是否 >= p
如果True，則output -= p
## 功能實作
### 加法
利用全加器的概念，每次做1-bit
ex:
10 + 10
第一個bit: 0 + 0 = 0, 0(進位)
第二個bit: 1 + 1 = 0, 1(進位)
此時因為最高位有進位的關係，將此進位值加到output最高位
output = 100

### 減法
利用全減器的概念，每次做1-bit
與加法相同，差別在於做減法前會事先確認a > b
### 小於
從最高位開始比較
* if a[i] < b[i] 
return true
* elif a[i] > b[i] 
return false
* if all equal 
return true

## 實例
2^4 mod 5
總共會做(2-1)^(4-1) = 3次加法 
initial: output = 10, g = 10, p = 101

#addition
iteration = 1:
output = output + g = 100

g = output
iteration = 2:
output = output + g = 1000

g = output
iteration = 3:
output = output + g = 10000
output > p ==> output = output - p = 1

#subtraction
iteration = 1
output(10000) >= p(101)
output = output - p = 1011

iteration = 2
output(1011) >= p(101)
output = output - p = 110

iteration = 3
output(110) >= p(101)
output = output - p = 1
![](https://i.imgur.com/ugSrYDd.png)


# Garbled circuit實作
## input -> 電路
假設input為( A and B )，我們使用()來代表一個gate，並用" "來區分每個input(input value 與 所使用的gate)，運用stack的概念來產生電路圖。
## 加密部分
先將每個gate的input與output亂數生成兩個0~25的數字當作其label_0與label_1，之後我們使用enigma來進行加密，將gate的兩個input當作enigma的key，然後對output加密，再使用兩個input與加密前的output產生一個hash number用於之後的驗證
## 解密部分
給定input後，server會使用這兩個input來解密4個output值，並藉由hash number來比對哪一個才是client想要的，最後將結果回傳給client。


## 參考資料
curve 25519 維基
https://zh.wikipedia.org/wiki/Curve25519#%E6%95%B8%E5%AD%B8%E5%B1%AC%E6%80%A7
各個介紹curve 25519 的網站
https://www.johndcook.com/blog/2019/03/09/curve25519/
https://is.gd/HqAlIG
https://is.gd/InUkJN
https://is.gd/xVxNBp
https://is.gd/znG6Eb
https://is.gd/LXz6Ug
https://is.gd/5gKaVG
https://is.gd/a1Tw4z
公開密鑰系統介紹
https://pse.is/M5TZ5
SHA-256
https://is.gd/Tdltlr
https://kknews.cc/zh-tw/tech/zbzjzkl.html
https://blog.csdn.net/lwanttowin/article/details/53726450

SHA-256範例
https://samkuo.me/post/2015/09/python-aes-256-and-sha-256-examples/
