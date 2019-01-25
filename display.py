##############################################################################
# Matrix Display Daemon
#
# Author: Kuroki Almajiro
# Date:   2018/10/12
##############################################################################

from rgbmatrix import graphics, RGBMatrix, RGBMatrixOptions
from datetime import datetime
import time
import redis
import os
import glob

##############################################################################
# Parameters
##############################################################################
default_font_path = "./fonts/default.bdf"
light_font_path = "./fonts/light.bdf"

led_rows = 32
led_cols = 64
led_chain = 2
led_parallel = 1
led_pwm_bits = 11
led_brightness = 100
led_hardware_mapping = 'adafruit-hat'

max_row = 2
margin_top = 14
margin_top_single = 24

mode = 0
mode_row = 1

scrolling = {0: 1, 1: 1}
direction = {0: 1, 1: 0}

messages = {}
colors = {}
scroll_speeds = {}
rainbows = {}

detect = True
before_checked = datetime.now()

version = "2.3.8"

##############################################################################
# Initialize Display
##############################################################################
def initialize():
    global options, matrix, canvas, store
    global default_font, light_font

    options = RGBMatrixOptions()
    options.rows = led_rows
    options.cols = led_cols
    options.chain_length = led_chain
    options.parallel = led_parallel
    options.brightness = led_brightness
    options.hardware_mapping = led_hardware_mapping
    options.disable_hardware_pulsing = True
    options.pwm_lsb_nanoseconds = 130

    # if you're not using raspberry pi 3 comment line below
    options.gpio_slowdown = 2

    matrix = RGBMatrix(options=options)
    canvas = matrix.CreateFrameCanvas()

    default_font = graphics.Font()
    default_font.LoadFont(default_font_path)

    light_font = graphics.Font()
    light_font.LoadFont(light_font_path)

    store = redis.StrictRedis(host='localhost', port=6379, db=0)

##############################################################################
# Message setter/getter
##############################################################################
def get_message(row=1):
    return store.get('message'+str(row)).decode('utf-8')

def get_messages():
    for i in range(max_row):
        messages[i] = get_message(i+1)

def set_message(row=1, message=''):
    store.set('message'+str(row), message)

##############################################################################
# Color setter/getter
##############################################################################
def get_color(row=1):
    red = int(store.zscore('message'+str(row)+'_color', 'red'))
    green = int(store.zscore('message'+str(row)+'_color', 'green'))
    blue = int(store.zscore('message'+str(row)+'_color', 'blue'))

    return {'red': red, 'green': green, 'blue': blue}

def get_colors():
    for i in range(max_row):
        _color = get_color(i+1)
        colors[i] = graphics.Color(_color['red'], _color['green'], _color['blue'])

def set_color(row=1, value=0, color='red'):
    store.zadd('message'+str(row)+'_color', int(value), color)

def get_rainbow(row=1):
    return int(store.get('message'+str(row)+'_rainbow'))

def get_rainbows():
    for i in range(max_row):
        rainbows[i] = get_rainbow(i+1)

def set_rainbow(row=1, status=0):
    store.set('message'+str(row)+'_rainbow', status)

##############################################################################
# Scroll Speed setter/getter
##############################################################################
def get_scroll_speed(row=1):
    return int(store.get('message'+str(row)+'_scroll_speed').decode('utf-8'))

def get_scroll_speeds():
    for i in range(max_row):
        scroll_speeds[i] = get_scroll_speed(i+1)

def set_scroll_speed(row=1, speed=4):
    store.set('message'+str(row)+'_scroll_speed', speed)



##############################################################################
# Common Functions
##############################################################################
def set_standby():
    set_message(1, 'Initialized.')
    set_message(2, 'Initialized.')
    #for i in range(2, max_row+1):
    #    set_message(i, '')

    for i in range(1, max_row+1):
        set_scroll_speed(i, 4)
        set_color(i, 255, 'red')
        set_color(i, 0, 'green')
        set_color(i, 0, 'blue')
        set_rainbow(i, 1)

    store.set('changed', 0)
    store.set('type', 0)
    store.set('mode', mode)
    store.set('row', mode_row)

def get_display_parameters():
    global mode, mode_row

    for i in range(max_row):
        get_colors()
        get_scroll_speeds()
        get_rainbows()

    mode = int(store.get('mode'))
    mode_row = int(store.get('row'))

def detect_usb():
    global detect, before_checked
    diff = datetime.now() - before_checked

    if diff.seconds >= 2:
        if glob.glob('/dev/sd*1'):
            if detect != True:
                detect = True
                print("USB Connected !!!!!!")
                check_usb()
                store.set('type', 1)
                store.set('changed', 1)
        else:
            if detect == True:
                detect = False
                print("USB not Disconnected !!!")

        before_checked = datetime.now()

def check():
    status = int(store.get('changed'))

    if status == True:
        store.set('changed', 0)
        return True

    return False

def check_type():
    get_type = int(store.get('type'))
    return get_type

def rainbow(color):
    if color[0] == 255 and color[2] == 0:
        color[1] += 1

    if color[1] == 255 and color[2] == 0:
        color[0] -= 1

    if color[1] == 255 and color[0] == 0:
        color[2] += 1

    if color[2] == 255 and color[0] == 0:
        color[1] -= 1

    if color[2] == 255 and color[1] == 0:
        color[0] += 1

    if color[0] == 255 and color[1] == 0:
        color[2] -= 1

    return color

def usleep(value):
    time.sleep(value / 1000000.0)

def animate():
    global canvas, matrix

    for times in range(3):
        for color_code in range(256):
            if times == 0:
                color = graphics.Color(color_code, 0, 0)
            if times == 1:
                color = graphics.Color(0, color_code, 0)
            if times == 2:
                color = graphics.Color(0, 0, color_code)

            for i in range(led_rows):
                graphics.DrawLine(canvas, 0, i, led_cols*led_chain, i, color)

            time.sleep(0.001)
            canvas = matrix.SwapOnVSync(canvas)

        for color_code in range(255, -1, -1):
            if times == 0:
                color = graphics.Color(color_code, 0, 0)
            if times == 1:
                color = graphics.Color(0, color_code, 0)
            if times == 2:
                color = graphics.Color(0, 0, color_code)

            for i in range(led_rows):
                graphics.DrawLine(canvas, 0, i, led_cols*led_chain, i, color)

            time.sleep(0.001)
            canvas = matrix.SwapOnVSync(canvas)

def check_usb():
    files = glob.glob('/dev/sd*1')

    if files:
        print('USB Drive detected')
        print('Mounting device')
        os.system('sudo mount ' + files[0] + ' /home/mnt')
        print('Device successfully mounted!')

        if os.path.exists('/home/mnt/message.txt'):
            print('Set Messages from USB')
            f = open('/home/mnt/message.txt', 'r')
            for i in range(max_row):
                set_message(i+1, f.readline().strip())
            f.close()

        if os.path.exists('/home/mnt/speed.txt'):
            print('Set Speeds from USB')
            f = open('/home/mnt/speed.txt')
            __speeds = f.read().replace('\r', '').split('\n')
            f.close()

            for i in range(len(__speeds)):
                set_scroll_speed(i+1, __speeds[i])

        if os.path.exists('/home/mnt/color.txt'):
            print('Set Colors from USB')
            f = open('/home/mnt/color.txt')
            __colors = f.read().replace('\r', '').split('\n')
            f.close()

            for i in range(len(__colors)):
                if __colors[i] != '':
                    set_rainbow(i+1, 0)
                    __colors_separated = __colors[i].split(',');
                    set_color(i+1, __colors_separated[0], 'red')
                    set_color(i+1, __colors_separated[1], 'green')
                    set_color(i+1, __colors_separated[2], 'blue')

                    if __colors_separated[0] + __colors_separated[1] +  __colors_separated[2] == '000':
                        set_rainbow(i+1, 1)

        if os.path.exists('/home/mnt/big.txt'):
            global mode, mode_row

            print ('Set Big Font')
            f = open('/home/mnt/big.txt')
            store.set('mode', 1)
            store.set('row', int(f.readline()))
            f.close()
        else:
            store.set('mode', 0)

        if os.path.exists('/home/mnt/direction.txt'):
            print('Set Direction')

            f = open('/home/mnt/direction.txt')
            for i in range(max_row):
                direction[i] = int(f.readline().strip())
            f.close()

        if os.path.exists('/home/mnt/scrollable.txt'):
            print('Set Scrollable')

            f = open('/home/mnt/scrollable.txt')
            for i in range(max_row):
                scrolling[i] = int(f.readline().strip())
            f.close()

        print("Unmounting device")
        os.system('sudo umount /home/mnt')

        before_checked = datetime.now()

    return

##############################################################################
# Main
##############################################################################
if __name__ == '__main__':
    print('Matrix Display Daemon')
    print('Version: '+version)
    print('-------------------------')

    print('Initializing....')
    initialize()
    #animate()
    set_standby()
    check_usb()

    print('Display initialized.')

    try:
        print('<Ctrl+C> to Exit')
        while True:
            get_messages()
            get_display_parameters()

            if mode == 0:
                lengths = {}
                positions ={}
                counters = {}

                rainbow_colors = {}
                rainbow_counters = {}

                for i in range(max_row):
                    if not direction[i]:
                        positions[i] = canvas.width
                    else:
                        messages[i] = messages[i][::-1]
                        positions[i] = -len(messages[i])
                    counters[i] = 0
                    rainbow_counters[i] = 0
                    rainbow_colors[i] = [255, 0, 0]

                strip_color = [255, 0, 0]

                while True:
                    if check():
                        if check_type():
                            break
                        else:
                            get_display_parameters()

                    canvas.Clear()
                    detect_usb()

                    strip_color = rainbow(strip_color)

                    for i in range(led_cols * led_chain):
                        canvas.SetPixel(i, margin_top + 2, strip_color[0], strip_color[1], strip_color[2])

                    for i in range(max_row):
                        if not scrolling[i]:
                            positions[i] = 0

                        if rainbows[i] == 1:
                            rainbow_counters[i] += 1

                            if rainbow_counters[i] == 1:
                                rainbow_colors[i] = rainbow(rainbow_colors[i])
                                rainbow_counters[i] = 0

                            color = graphics.Color(rainbow_colors[i][0], rainbow_colors[i][2], rainbow_colors[i][1])
                        else:
                            color = colors[i]

                        lengths[i] = graphics.DrawText(canvas, default_font, positions[i], margin_top * (i+1), color, messages[i])

                        if (scroll_speeds[i] < counters[i]) and scrolling[i]:
                            if direction[i]:
                                positions[i] += 1
                            else:
                                positions[i] -= 1

                            counters[i] = 0

                        if (positions[i] + lengths[i] < 0) and not direction[i]:
                            positions[i] = canvas.width

                        if direction[i] and (positions[i] + lengths[i] > canvas.width + lengths[i]):
                            positions[i] = -lengths[i]

                        counters[i] += 1

                    usleep(0.001)
                    canvas = matrix.SwapOnVSync(canvas)
            else:
                if not scrolling[mode_row-1]:
                    position = 0
                else:
                    position = canvas.width

                if direction[mode_row-1]:
                    messages[mode_row-1] = messages[mode_row-1][::-1]

                counter = 0
                rainbow_color = [255, 0 ,0]
                rainbow_counter = 0

                while True:
                    if check():
                        if check_type():
                            break
                        else:
                            get_display_parameters()

                    canvas.Clear()
                    detect_usb()

                    if rainbows[mode_row-1] == 1:
                        rainbow_counter += 1

                        if rainbow_counter == 1:
                            rainbow_color = rainbow(rainbow_color)
                            rainbow_counter = 0

                        color = graphics.Color(rainbow_color[0], rainbow_color[2], rainbow_color[1])
                    else:
                        color = colors[mode_row-1]

                    length = graphics.DrawText(canvas, light_font, position, margin_top_single, color, messages[mode_row-1])
                    if (scroll_speeds[mode_row-1] < counter) and scrolling[mode_row-1]:
                        if direction[mode_row-1]:
                            position += 1
                        else:
                            position -= 1

                    if (position + length < 0) and not direction[mode_row-1]:
                        position = canvas.width

                    if direction[mode_row-1] and (position + length > canvas.width + length):
                        position = -length


                    counter += 1
                    time.sleep(0.001)
                    canvas = matrix.SwapOnVSync(canvas)

    except KeyboardInterrupt:
        matrix.Clear()
        print('See you next time!')
