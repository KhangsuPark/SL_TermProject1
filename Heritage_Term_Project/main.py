from tkinter import *
import sys
from PIL import ImageTk, Image
import random
import requests
import xml.etree.ElementTree as ET
import telepot
import traceback


class MainGUI:

    def __init__(self):
        #데이터 추출
        url = 'http://www.cha.go.kr/cha/SearchKindOpenapiList.do'
        param = {'ccbaCtcd' : '11'}
        response = requests.get(url, params=param)
        self.root = ET.fromstring(response.text)
        self.apiKey = 'AIzaSyBB47PEev4ghi50AZ3j3Xf-VcMGxgX67fc'
        params1 = [21,22,23,24,25,26,45,31,32,33,34,35,36,37,38,50,'ZZ']

        for i in params1:
            params = {'ccbaCtcd' : i}
            response = requests.get(url, params=params)

            self.root.append(ET.fromstring(response.text))

        self.barChartData = [['11', '국보', 0],
                             ['12', '보물', 0],
                             ['13', '사적', 0],
                             ['16', '천연기념물', 0],
                             ['18', '국가민속문화재', 0],
                             ['21', '시도유형문화재', 0]]

        self.window = Tk()
        self.window.title("한국 문화유산 정보")
        self.window.geometry("650x610")


        #검색
        self.entry = Entry(self.window,font=("Helvetica",10),width = 40)
        self.entry.place(x=1,y=1)

        #검색결과리스트
        self.frame = Frame(self.window,bg = 'azure4')
        self.frame.place(x = 1,y = 31,width = 280,height = 250)

        self.scrollbar = Scrollbar(self.frame)
        self.scrollbar.pack(side='right', fill='y')

        self.list = Listbox(self.frame,yscrollcommand=self.scrollbar.set)
        self.list.pack(side='left', fill='both', expand=True)

        self.scrollbar.config(command=self.list.yview)

        self.info_canvas = Canvas(self.window, bg='azure3', width=340, height=100)
        self.info_canvas.place(x=300, y=350)
        self.text_object =[]
        for i in range(4):
            temp = self.info_canvas.create_text(170, 20 * (i + 1), text='')
            self.text_object.append(temp)

        #리스트에 아이템 추가
        self.data = []

        for item in self.root.iter("item"):
            ccbaMnm1 = item.findtext("ccbaMnm1")
            ccbaKdcd = item.findtext("ccbaKdcd")
            ccsiName = item.findtext("ccsiName")
            ccbaCtcdNm = item.findtext("ccbaCtcdNm")
            ccbaAdmin = item.findtext("ccbaAdmin")
            longitude = item.findtext("longitude")
            latitude = item.findtext("latitude")
            ccmaName = item.findtext("ccmaName")

            self.data.append([ccbaMnm1, ccbaKdcd,ccbaCtcdNm,ccsiName,ccbaAdmin,longitude, latitude,ccmaName])

            for index in self.barChartData:
                if index[0] == ccbaKdcd:
                    index[2] += 1

        #검색 결과
        self.update(self.data)
        self.list.bind("<<ListboxSelect>>",self.fill_out)
        self.entry.bind("<KeyRelease>",self.check)

        #파이차트 만들기
        self.create_pi_chart()

        #봇 생성
        TOKEN = '6062580679:AAH9aWOA0h6cEIOIBjP0j7ZAxq5-EUZleRA'
        self.bot = telepot.Bot(TOKEN)
        self.bot.message_loop(self.handle)

        #이미지 파일
        self.image_path = 'heritage.png'
        self.image = Image.open(self.image_path)
        self.heritage_image = ImageTk.PhotoImage(self.image)
        self.image_label = Label(self.window, image=self.heritage_image)
        self.image_label.place(x=0,y=450)

        self.window.mainloop()
    def sendMessage(self, user, msg):
        try:
            self.bot.sendMessage(user, msg)
        except:
            traceback.print_exc(file=sys.stdout)

    def handle(self, msg):
        content_type, chat_type, chat_id = telepot.glance(msg)
        if content_type != 'text':
            self.sendMessage(chat_id, '난 텍스트 이외의 메시지는 처리하지 못해요.')
            return

        text = msg['text']
        args = text.split(' ')

        if text.startswith('정보') and len(args) > 1:
            print('try to 정보', args[1])
            existFlag = False
            for item in self.data:
                if args[1] in item[0]:
                    existFlag = True
                    msg = '<' + args[1] + '정보>\n'
                    ccsi = item[2]
                    ccba = item[3]
                    admin = item[4]
                    msg += '문화재 종목 : ' + item[7] + '\n'
                    msg += '시도명 : ' + item[2] + '\n'
                    msg += '시군구명 : ' + item[3] + '\n'
                    msg += '관리자 : ' + item[4] + '\n'
                    break

            if existFlag == True:
                self.sendMessage(chat_id, msg)
            else:
                self.sendMessage(chat_id, '정보가 없습니다')
        elif text.startswith('거리') and len(args) > 1:
            pass

        elif text.startswith('분포'):
            print('try to 분포')
            msg = '<문화재 분포도>\n'

            for i in range(6):
                msg += str(self.barChartData[i][1])+' : '+ str(self.barChartData[i][2]) + '\n'
            self.sendMessage(chat_id, msg)
        else:
            self.sendMessage(chat_id, '모르는 명령어입니다.')
    def update(self, data):
        self.list.delete(0,END)
        for item in data:
            self.list.insert(END, item[0])

    def fill_out(self,e):
        lon = 0
        lat = 0
        ccsi = ''
        ccba = ''
        admin = ''
        ccma = ''
        for i in self.data:
            if i[0] == self.list.get(self.list.curselection()):
                ccsi = i[2]
                ccba = i[3]
                admin = i[4]
                lon = i[5]
                lat = i[6]
                ccma = i[7]
                break
        self.info_canvas.itemconfig(self.text_object[0], text='문화재종목 : ' + ccma)
        self.info_canvas.itemconfig(self.text_object[1], text='시도명 : ' + ccsi)
        self.info_canvas.itemconfig(self.text_object[2], text='시군구명 : ' + ccba)
        self.info_canvas.itemconfig(self.text_object[3], text='관리자 : ' + admin)

        if lon == 0 or lat == 0:
            print(lon, lat)
        else:
            marker_color = 'red'
            url = f"https://maps.googleapis.com/maps/api/staticmap?center={lat},{lon}&zoom=13&size=600x400&key={self.apiKey}"
            marker_params = f"color:{marker_color}|label:X|{lat},{lon}"
            url += f"&markers={marker_params}"
            response = requests.get(url)
            image_data = response.content
            image = PhotoImage(data=image_data)

            map_label = Label(self.window, image=image,width=330,height=330)
            map_label.image = image
            map_label.place(x=300, y=10)


    def check(self, e):
        typed = self.entry.get()
        if typed == '':
            data = self.data
        else:
            data = []
            for item in self.data:
                if typed in item[0]:
                    data.append(item)

        self.update(data)

    def create_pi_chart(self):
        c2 = Canvas(self.window,width=280, height=160, bg='azure3')
        c2.place(x = 1,y=290)

        start = 0
        s = 0
        for i in self.barChartData:
            s += i[2]

        for i in range(6):
            extent = self.barChartData[i][2] / s * 360
            color = self.random_color()
            c2.create_arc((10, 10, 160, 160), fill=color, outline='white', start=start, extent=extent)
            start = start + extent
            c2.create_rectangle(160, 20 + 20 * i, 260, 20 + 20 * (i + 1), fill=color)
            c2.create_text(210, 10 + 20 * (i + 1), text=str(self.barChartData[i][1]))
        c2.create_text(75, 10, text='문화재 종류')

    def random_color(self):
        color = '#'
        colors = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F']
        for i in range(6):
            color += colors[random.randint(0, 15)]
        return color



MainGUI()