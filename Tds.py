import requests
import os,sys,json

tokentds = input("Nhập token TDS:")
checktt=requests.get("http://traodoisub.com/api/?fields=profile&access_token=" +tokentds).json()
tokenfb = input("Nhập token Facebook :")
checkttfb = requests.get("https://graph.facebook.com/me/?access_token=" +tokenfb).json()
try :
  idfb = checkttfb["id"]
  tenfb = checkttfb["name"]
except :
  print("nhập sai token Facebook !")
  quit()

if "success" in checktt : 
  tentk = checktt["data"]["user"]
  xu = checktt["data"]["xu"]
  xudie = checktt["data"]["xudie"]
  
  print("Tài Khoản TDS là "+tentk)
  print("xu hiện có là " +xu)
  print("số xu die là " +xudie)
else:
   print("ẩu rồi ba")
   quit()
print("id của FaceBook vừa nhập là " +idfb)
print("Tên Facebook vừa nhập là " +tenfb)
cauhinh=requests.get("https://traodoisub.com/api/?fields=run&id="+idfb+"&access_token="+tokentds).json()
if "success" in cauhinh :
#if 1 == 1:
  idcauhinh = cauhinh["data"]["id"]
  #print("id "+idcauhinh+" đã được cấu hình thành công")
  trangthaicauhinh = cauhinh["data"]["msg"]
  print(trangthaicauhinh+" cho id " + idcauhinh)
else :
  print("id chưa được cấu hình")
  quit()
print("1.like")
print("2.share")
#print("3.cmt")
print("4.follow")
nhiemvu = input("nhập số chọn nhiệm vụ:"  )
if nhiemvu == str(1):
  nhiemvulam = "like"
  while True :
    get_like = requests.get("https://traodoisub.com/api/?fields=like&access_token=" + tokentds).json()
    for get in get_like:
      idnv = get['id']
    lamnv = requests.post("https://graph.facebook.com/" +str(idnv) +"/likes?access_token="+ tokenfb)
    done = requests.get("https://traodoisub.com/api/coin/?type=like&id=" +str(idnv)+ "&access_token="+ tokentds)
elif nhiemvu == str(2) :
  nhiemvulam = "share"
while True :
  get_share = requests.get("https://traodoisub.com/api/?fields=comment&access_token=" + tokentds).json()
  for get in get_share :
    idshare = get["id"]
    lamnvshare = requests.get("https://graph.facebook.com/" + idshare +"/share?access_token=" + tokenfb)
    print(lamvnshare)
    done = requests.get("https://traodoisub.com/api/coin/?type=share&id="+ idshare + "&access_token=" + tokentds)
    print(done.text)
    #time.sleep(5)
    continue 
#elif nhiemvu == str(3) :
  #nhiemvulam = "comments"
#elif nhiemvu == str(4) :
  #nhiemvulam = "subscribers"
#else :
  #print("chọn con cặc gì vậy")
  quit()
#print(nhiemvulam)

