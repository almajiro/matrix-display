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
mode = False
mode_row = 1

messages = {}
colors = {}
scroll_speeds = {}

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
        print(str(i)+': '+messages[i])

def set_message(row=1, message=''):
    store.set('message'+str(row), message)

##############################################################################
# Color setter/getter
##############################################################################
def get_color(row=1):
    red = store.zscore('message'+str(row)+'_color', 'red')
    green = store.zscore('message'+str(row)+'_color', 'green')
    blue = store.zscore('message'+str(row)+'_color', 'blue')

    return {'red': int(red), 'green': int(green), 'blue': int(blue)}

def get_colors():
    for i in range(max_row):
        color = get_color(i+1)
        colors[i] = graphics.Color(color['red'], color['green'], color['blue'])

def set_color(row=1, value=0, color='red'):
    store.zadd('message'+str(row)+'_color', value, color)

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

    for i in range(1, max_row+1):
        set_scroll_speed(i, 4)
        set_color(i, 255, 'red')
        set_color(i, 0, 'green')
        set_color(i, 0, 'blue')

    store.set('changed', 0)
    store.set('type', 0)
    store.set('mode', mode)
    store.set('row', mode_row)

def get_display_parameters():
    for i in range(max_row):
        get_colors()
        get_scroll_speeds()

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

##############################################################################
# Main
##############################################################################
if __name__ == '__main__':
    initialize()
    set_standby()
    get_display_parameters()

    print('Display initialized.')

    while True:
        print('Get new message from redis.')
        get_messages()

        if mode == False:
            lengths = {}
            positions ={}
            counters = {}

            for i in range(max_row):
                positions[i] = canvas.width
                counters[i] = 0

            while True:
                if check():
                    if check_type():
                        break
                    else:
                        get_display_parameters()

                canvas.Clear()

                for i in range(max_row):
                    lengths[i] = graphics.DrawText(canvas, default_font, positions[i], margin_top * (i+1), colors[i], messages[i])

                    if scroll_speeds[i] < counters[i]:
                        positions[i] -= 1
                        counters[i] = 0
                    
                    if positions[i] + lengths[i] < 0:
                        positions[i] = canvas.width

                    counters[i] += 1

                time.sleep(0.001)
                canvas = matrix.SwapOnVSync(canvas)
        else:
            message = messages[mode_row-1]
            color = colors[mode_row-1]
            scroll_speed = scroll_speeds[mode_row-1]
            position = canvas.width
            counter = 0

            while True:
                if check():
                    if check_type():
                        break
                    else:
                        get_display_parameters()

                canvas.Clear()

                length = graphics.DrawText(canvas, lgiht_font, position, 10, color, message)

                if scroll_speed < counter:
                    positions[i] -= 1
                    counters[i] = 0
                    
                if position + length < 0:
                    position = canvas.width

                counter += 1
                time.sleep(0.001)
                canvas = matrix.SwapOnVSync(canvas)