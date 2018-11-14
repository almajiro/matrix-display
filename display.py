##############################################################################
# Matrix Display Daemon 
#
# Author: Kuroki Almajiro
# Date:   2018/10/12
##############################################################################

from rgbmatrix import graphics, RGBMatrix, RGBMatrixOptions
import time
import redis

##############################################################################
# Parameters
##############################################################################
default_font_path = "./fonts/default.bdf"
light_font_path = "./fonts/light.bdf"

led_rows = 32
led_cols = 32
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

messages = {}
colors = {}
scroll_speeds = {}
rainbows = {}

version = "1.0"

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
    options.disable_hardware_pulsing = False

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
        colors[i] = graphics.Color(_color['red'], _color['blue'], _color['green'])

def set_color(row=1, value=0, color='red'):
    store.zadd('message'+str(row)+'_color', value, color)

def get_rainbow(row=1):
    return int(store.get('message'+str(row)+'_rainbow'))

def get_rainbows():
    for i in range(max_row):
        rainbows[i] = get_rainbow(i+1)

def set_rainbow(row=1, status=0):
    store.add('message'+str(row)+'_rainbow', status)

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
    for i in range(2, max_row+1):
        set_message(i, '')

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

##############################################################################
# Main
##############################################################################
if __name__ == '__main__':
    print('Matrix Display Daemon')
    print('Version: '+version)
    print('-------------------------')

    print('Initializing....')
    initialize()
    set_standby()

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

                rainbow_colors = []
                rainbow_counters = {}

                for i in range(max_row):
                    positions[i] = canvas.width
                    counters[i] = 0
                    rainbow_counters[i] = 0
                    rainbow_colors[i] = [255, 0, 0]

                while True:
                    if check():
                        if check_type():
                            break
                        else:
                            get_display_parameters()

                    canvas.Clear()

                    for i in range(max_row):
                        if rainbows[i] == 1:
                            rainbow_counters[i] += 1

                            if rainbow_count = 1:
                                rainbow_colors[i] = rainbow(rainbow_colors[i])
                                rainbow_counters[i] = 0

                            color = graphics.Color(rainbow_colors[i][0], rainbow_colors[i][2], rainbow_colors[i][1])
                        else:
                            color = colors[i]

                        lengths[i] = graphics.DrawText(canvas, default_font, positions[i], margin_top * (i+1), color, messages[i])

                        if scroll_speeds[i] < counters[i]:
                            positions[i] -= 1
                            counters[i] = 0
                        
                        if positions[i] + lengths[i] < 0:
                            positions[i] = canvas.width

                        counters[i] += 1

                    time.sleep(0.001)
                    canvas = matrix.SwapOnVSync(canvas)
            else:
                position = canvas.width
                counter = 0

                while True:
                    if check():
                        if check_type():
                            break
                        else:
                            get_display_parameters()

                    canvas.Clear()

                    length = graphics.DrawText(canvas, light_font, position, margin_top_single, colors[mode_row-1], messages[mode_row-1])

                    if scroll_speeds[mode_row-1] < counter:
                        position -= 1
                        counter = 0
                        
                    if position + length < 0:
                        position = canvas.width

                    counter += 1
                    time.sleep(0.001)
                    canvas = matrix.SwapOnVSync(canvas)

    except KeyboardInterrupt:
        print('See you next time!')