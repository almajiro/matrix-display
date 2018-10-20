from rgbmatrix import graphics, RGBMatrix, RGBMatrixOptions
import time
import redis

led_font = "./fonts/k8x12.bdf"

led_rows = 32
led_cols = 32
led_chain = 2
led_parallel = 1
led_pwm_bits = 11
led_brightness = 100
led_hardware_mapping = 'adafruit-hat'

message1 = ''
message2 = ''

message1_scroll_speed = 4
message2_scroll_speed = 4

max_text_length = led_cols / 2

def initialize():
    global options, matrix, canvas, font, text_color, store

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

    font = graphics.Font()
    font.LoadFont(led_font)

    text_color = graphics.Color(255, 0, 0)

    store = redis.StrictRedis(host='localhost', port=6379, db=0)

def get_color(row=1):
    red = store.zscore('message'+row+'_color', 'red')
    green = store.zscore('message'+row+'_color', 'green')
    blue = store.zscore('message'+row+'_color', 'blue')

    return {'red': red, 'green': green, 'blue': blue}


def get_colors():
    global message1_color, message2_color

    message1_color_obj = get_color(1)
    message2_color_obj = get_color(2)

    message1_color = graphics.Color(message1_color_obj.red, message1_color_obj.green, message1_color_obj.blue)
    message2_color = graphics.Color(message2_color_obj.red, message2_color_obj.green, message2_color_obj.blue)


def set_message(message1='', message2=''):
    store.set('message1', message1)
    store.set('message2', message2)

def set_standby():
    set_message('Initialized.', 'Waiting for new message')
    store.set('message1_scroll_speed', 4)
    store.set('message2_scroll_speed', 4)

    store.zadd('message1_color', 255, 'red')
    store.zadd('message1_color', 0, 'green')
    store.zadd('message1_color', 0, 'blue')

    store.zadd('message2_color', 255, 'red')
    store.zadd('message2_color', 0, 'green')
    store.zadd('message2_color', 0, 'blue')


def get_message(row=1):
    return store.get('message'+str(row)).decode('utf-8')

def get_new_message():
    global message1, message2

    message1 = get_message(1)
    message2 = get_message(2)

    print('1: '+message1)
    print('2: '+message2)

def get_display_parameters():
    global message1_scroll_speed, message2_scroll_speed

    message1_scroll_speed = store.get('message1_scroll_speed')
    message2_scroll_speed = store.get('message2_scroll_speed')

    get_colors()

def check_new_message():
    global message1, message2

    if (message1 != get_message(1)) or (message2 != get_message(2)):
        return True
    else:
        return False

if __name__ == '__main__':
    initialize()
    set_standby()

    print('Display initialized.')

    while True:
        print('Get new message from redis.')
        get_new_message()

        if len(message1) > max_text_length:
            message1_position = canvas.width
        else:
            message1_position = 0

        if len(message2) > max_text_length:
            message2_position = canvas.width
        else:
            message2_position = 0

        message1_scroll_counter = 0
        message2_scroll_counter = 0

        while True:
            if check_new_message():
                break
            else:
                get_display_parameters()

            canvas.Clear()

            message1_length = graphics.DrawText(canvas, font, message1_position, 14, message1_color, message1)
            message2_length = graphics.DrawText(canvas, font, message2_position, 28, message2_color, message2)

            if (len(message1) > max_text_length) and (int(message1_scroll_speed) < message1_scroll_counter):
                message1_position -= 1
                message1_scroll_counter = 0

            if (len(message2) > max_text_length) and (int(message2_scroll_speed) < message2_scroll_counter):
                message2_position -= 1
                message2_scroll_counter = 0

            if message1_position + message1_length < 0:
                message1_position = canvas.width

            if message2_position + message2_length < 0:
                message2_position = canvas.width

            message1_scroll_counter += 1
            message2_scroll_counter += 1

            time.sleep(0.001)
            canvas = matrix.SwapOnVSync(canvas)
