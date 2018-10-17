#!/usr/bin/python
from rgbmatrix import graphics, RGBMatrix, RGBMatrixOptions
from PIL import Image
from pprint import pprint
import mpd
import time
import datetime
import feedparser
import random
import json
import requests

def showDateTime(canvas):

    datenow = datetime.datetime.now()

    message = str(datenow.hour).zfill(2) + ":" + str(datenow.minute).zfill(2) + ":" + str(datenow.second).zfill(2)

    canvas.Clear()

    len = graphics.DrawText(canvas, font, 0, 13, textColor, message)

    for x in range(0, canvas.width):
        canvas.SetPixel(x, 0, 128, 128, 64)
        canvas.SetPixel(x, 1, 128, 128, 64)

        canvas.SetPixel(x, ledRows - 2, 64, 128, 128);
        canvas.SetPixel(x, ledRows - 1, 64, 128, 128);

    canvas = matrix.SwapOnVSync(canvas)
    
def showRss(canvas):
    pos = canvas.width
    pos2 = canvas.width
    rss = feedparser.parse(rssLinks[random.randrange(5)])

    message = ""

    for entry in rss.entries:
        message += entry.title + "         "

    textColor = graphics.Color(64, 128, 34)

    color1 = 255
    color2 = 0
    color3 = 0
    rgb = 1

    scanner = 0
    scannerMode = 0

    prayerApi = "http://api.aladhan.com/v1/timingsByAddress?address=Kazo,%20Saitama,%20Japan"
    r = requests.get(prayerApi)
    json_object = r.text

    data = json.loads(json_object)

    pprint(data)

    prayerMsg = ""

    displayMode = 1

    for timings in data["data"]["timings"]:
        prayerMsg += timings + ": " + data["data"]["timings"][timings] + " "

    displayStart = time.time()

    while True:
        canvas.Clear()

        datenow = datetime.datetime.now()
                                                                                                                      
        message2 = str(datenow.hour).zfill(2) + ":" + str(datenow.minute).zfill(2) + ":" + str(datenow.second).zfill(2)

        today = datetime.date.today()

        message3 = str(today.month).zfill(2) + "/" + str(today.day).zfill(2)

        len = graphics.DrawText(canvas, font, pos, 14, textColor, message)

        if time.time() - displayStart > 20:
            displayMode = not displayMode
            displayStart = time.time()

        if displayMode == 0:
            graphics.DrawText(canvas, font, 4, 28, textColor, message2)
            graphics.DrawText(canvas, font, 42, 28, textColor, message3)
        else:
            len2 = graphics.DrawText(canvas, font, pos2, 28, textColor, prayerMsg)

        if rgb == 1:
            color1 -= 1
            color2 += 1
            color3 += 1

            if color1 == 0:
                color1 = 0
                color2 = 255
                color3 = 255
                rgb = 2

        if rgb == 2:
            color1 += 1
            color3 -= 1

            if color3 == 0:
                color1 = 255
                color2 = 255
                color3 = 0
                rgb = 3

        if rgb == 3:
            color2 -= 1

            if color2 == 0:
                color1 = 255
                color2 = 0
                color3 = 0
                rgb = 1

        for x in range(0, canvas.width):
            canvas.SetPixel(x, 0, color1, color2, color3)
            canvas.SetPixel(x, 1, color1, color2, color3)
            canvas.SetPixel(x, 2, color2, color1, color2)

            canvas.SetPixel(x, canvas.height - 3, color2, color1, color2)
            canvas.SetPixel(x, canvas.height - 2, color1, color2, color3)
            canvas.SetPixel(x, canvas.height - 1, color1, color2, color3)

            canvas.SetPixel(x, canvas.height / 2 - 1, 0, 0, 0)

        if scannerMode == 0:
            for x in range(0, scanner):
                canvas.SetPixel(x, canvas.height / 2 , color2, color1, color2)
            scanner += 1

            if scanner == canvas.width:
                scanner = 0
                scannerMode = 1

        if scannerMode == 1:
            for x in range(scanner, canvas.width):
                canvas.SetPixel(x, canvas.height / 2, color2, color1, color2)

            scanner += 1

            if scanner == canvas.width:
                scanner = 0
                scannerMode = 0

        if scannerMode == 3:
            for x in range(0, scanner):
                canvas.SetPixel(x, canvas.height / 2 - 1, color2, color1, color2)
            scanner -= 1

            if scanner == 0:
                scanner = 0
                scannerMode = 0

        pos -= 1
        pos2 -= 1

        if (pos + len < 0):
            break

        if (pos2 + len2 < 0):
            pos2 = canvas.width

        time.sleep(0.04)
        canvas = matrix.SwapOnVSync(canvas)

def showTime(canvas, client):

    if client.status()["state"] == "play":
        songTime = client.status()["time"]
        currentTime = int(songTime.split(":")[0])

        minutes = 0
        seconds = 0

        while currentTime >= 60:
            minutes += 1
            currentTime -= 60

        seconds = currentTime

        message = str(minutes).zfill(2) + ":" + str(seconds).zfill(2)

        canvas.Clear()

        len = graphics.DrawText(canvas, font, 7, 13, textColor, message)

        for x in range(0, canvas.width):
            canvas.SetPixel(x, 0, 128, 128, 0)
            canvas.SetPixel(x, 1, 128, 128, 0)

            canvas.SetPixel(x, ledRows - 2, 128, 128, 0);
            canvas.SetPixel(x, ledRows - 1, 128, 128, 0);

        canvas = matrix.SwapOnVSync(canvas)

def showStatus(canvas, client):
    pos = canvas.width

    if client.status()["state"] == "play":
        audio = client.status()["audio"]
        bitrate = client.status()["bitrate"]
        volume = client.status()["volume"]

        message = audio + " / Bitrate: " + bitrate + " / Volume: " + volume

        while True:
            canvas.Clear()

            len = graphics.DrawText(canvas, font, pos, 13, textColor, message)

            for x in range(0, canvas.width):
                canvas.SetPixel(x, 0, 128, 0, 0)
                canvas.SetPixel(x, 1, 128, 0, 0)

                canvas.SetPixel(x, ledRows - 2, 128, 0, 0);
                canvas.SetPixel(x, ledRows - 1, 128, 0, 0);

            pos -= 1

            if (pos + len < 0):
                break

            time.sleep(0.04)
            canvas = matrix.SwapOnVSync(canvas)

def showAlbum(canvas, clinet):
    pos = canvas.width

    if client.status()["state"] == "play":
        currentAlbum = client.currentsong()["album"]
        album = client.currentsong()["album"]

        try:
            date = client.currentsong()["date"]
        except KeyError:
            date = ""

        try:
            genre = client.currentsong()["genre"]
        except KeyError:
            genre = ""

        message = album

        if date != "":
            message += " (" + date + ")"

        if genre != "":
            message += " / " + genre

        while True:
            if currentAlbum != album:
                break

            canvas.Clear()

            len = graphics.DrawText(canvas, font, pos, 13, textColor, message)

            for x in range(0, canvas.width):
                canvas.SetPixel(x, 0, 0, 0, 128)
                canvas.SetPixel(x, 1, 0, 0, 128)

                canvas.SetPixel(x, ledRows - 2, 0, 0, 128);
                canvas.SetPixel(x, ledRows - 1, 0, 0, 128);

            pos -= 1

            if (pos + len < 0):
                break

            time.sleep(0.04)
            canvas = matrix.SwapOnVSync(canvas)

def showTitle(canvas, client):
    pos = canvas.width

    if client.status()["state"] == "play":
        currentTitle = client.currentsong()["title"]
        title = client.currentsong()["title"]
        artist = client.currentsong()["artist"]

        message = artist + " - " + title

        while True:
            if currentTitle != title:
                break

            songTime = client.status()["time"]
            currentTime = int(songTime.split(":")[0])

            minutes = 0
            seconds = 0

            while currentTime >= 60:
                minutes += 1
                currentTime -= 60

            seconds = currentTime

            message2 = str(minutes).zfill(2) + ":" + str(seconds).zfill(2)
            print(message2)
            canvas.Clear()

            len = graphics.DrawText(canvas, font, pos, 13, textColor, message)
            graphics.DrawText(canvas, font, 80, 44, textColor, message2)
            
            for x in range(0, 10):
                for y in range(0, 15):
                    canvas.SetPixel(x, y, 0, 0, 0)

            canvas.SetImage(playbutton, 65, 22)

            for x in range(0, canvas.width):
                canvas.SetPixel(x, 0, 0, 128, 0)
                canvas.SetPixel(x, 1, 0, 128, 0)

                canvas.SetPixel(x, ledRows - 2, 0, 128, 0);
                canvas.SetPixel(x, ledRows - 1, 0, 128, 0);

            pos -= 1

            if (pos + len < 0):
                break

            time.sleep(0.04)
            canvas = matrix.SwapOnVSync(canvas)

def animate():
    global animationCurrentCol
    global animationCurrentRow
    global animationStatus
    global ledRows
    global ledCols
    global canvas

    if animationStatus == 0:
        for x in range(0, animationCurrentRow):
            canvas.SetPixel(animationCurrentCol, x, 0, 128, 0)
        animationCurrentRow += 1
    elif animationStatus == 1:
        for x in range(0, animationCurrentCol):
            canvas.SetPixel(x, animationCurrentRow, 0, 128, 0)
        animationCurrentCol += 1
    elif animationStatus == 2:
        for x in range(animationCurrentRow, 0, -1):
            canvas.SetPixel(animationCurrentCol, x, 0, 128, 0)
        animationCurrentRow -= 1
    elif animationStatus == 3:
        for x in range(animationCurrentCol, 0, -1):
            canvas.SetPixel(x, animationCurrentRow, 0, 128, 0)
        animationCurrentCol -= 1

    canvas = matrix.SwapOnVSync(canvas)

    if animationCurrentRow == ledRows - 1 and animationStatus == 0:
        animationStatus = 1
    elif animationCurrentCol == ledCols - 1 and animationCurrentRow == ledRows - 1:
        animationStatus = 2
    elif animationCurrentCol == ledCols - 1 and animationCurrentRow == 0:
        animationStatus = 3
    elif animationCurrentRow == 0 and animationCurrentCol == 0:
        animationStatus = 0
    

if __name__ == "__main__":
    currentTime = 0
    slideTime = 15
    mode = 5 

    animationState = 0
    animationCurrentRow = 0
    animationCurrentCol = 0
    animationStatus = 0

    ledFont = "./fonts/k8x12.bdf"

    ledRows = 32
    ledCols = 32
    ledChain = 2
    ledParallel = 1
    ledPwmBits = 11
    ledBrightness = 100

    options = RGBMatrixOptions()
    options.rows = ledRows
    options.cols = ledCols
    options.chain_length = ledChain
    options.parallel = ledParallel
    options.brightness = ledBrightness
    options.hardware_mapping = 'adafruit-hat'
    options.disable_hardware_pulsing = False
    
    matrix = RGBMatrix(options = options)

    canvas = matrix.CreateFrameCanvas()
    font = graphics.Font()
    font.LoadFont(ledFont)
    textColor = graphics.Color(255, 0, 0)

    playbutton = Image.open("./playbutton.png").convert('RGB')

    currentTime = time.time()

    rssLinks = [
        "http://rss.asahi.com/rss/asahi/newsheadlines.rdf",
        "https://www.oreilly.co.jp/catalog/soon.xml",
        "https://news.mynavi.jp/rss/index.xml",
        "http://rss.asahi.com/rss/asahi/politics.rdf",
        "http://rss.asahi.com/rss/asahi/national.rdf"
    ]

    while True:
        try:
            client = mpd.MPDClient(use_unicode=True)
            client.timeout = 2
            client.idletimeout = None
            client.connect("192.168.255.99", 6600)

            if time.time() - currentTime > slideTime:
                currentTime = time.time()
                #mode += 1
            
                if mode == 7:
                    mode = 1

            if mode == 1:
                showTitle(canvas, client)
        
            if mode == 2:
                showAlbum(canvas, client)
        
            if mode == 3:
                showStatus(canvas, client)

            if mode == 4:
                showTime(canvas, client)

            if mode == 5:
                showRss(canvas)

            if mode == 6:
                showDateTime(canvas)

            time.sleep(0.025)

        except:
            showRss(canvas)

    client.close()
    client.disconnect()
