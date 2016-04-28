# import time
import sys
sys.path.append('lib')

if sys.platform == 'linux':
    # Packages used only on linux platform (named pipes, ...)
    sys.path.append('lib_linux')

import utime
import math
import gc

# import transport_pipe as pipe

# from trezor import msg
from trezor import loop
from trezor.utils import unimport_gen, unimport_func
from trezor import layout
from trezor import ui

if __debug__:
    import logging
    logging.basicConfig(level=logging.INFO)

def perf_info():
    mem_alloc = gc.mem_alloc()
    gc.collect()
    print("mem_alloc: %s/%s, last_sleep: %d" % \
          (mem_alloc, gc.mem_alloc(), loop.last_sleep))
    loop.call_later(1000000, perf_info)

'''
def animate():
    col = 0
    # hawcons gesture
    f = open('playground/tap_64.toig', 'r')

    while True:
        col %= 0xff
        col += 0x0f

        ui.display.icon(190, 170, f.read(), ui.rgbcolor(col, 0, 0), 0xffff)
        f.seek(0)

        yield loop.Sleep(int(0.5 * 1000000))

sec = 0
event = None
def sekunda(x):
    global sec
    print('Sekunda %d' % sec)
    

    if sec == 0:
        # if loop.button_cb:
        #    loop.call_soon(loop.button_cb, 'levy')
        #    loop.button_cb = None
        return

    sec += 1
    loop.call_later(1, sekunda, x)

def wait_for():
    print("Jsem tady")

    ktery = yield loop.IOButton()
    print(ktery)
    
    print("Po cekani na event")
'''

def tap_to_confirm(address, amount, currency):

    loop.call_later(5 * 1000000, layout.change(homescreen()))

    ui.display.bar(0, 0, 240, 40, ui.GREEN)
    ui.display.bar(0, 40, 240, 200, ui.WHITE)

    ui.display.text(10, 28, 'Sending', ui.BOLD, ui.WHITE, ui.GREEN)
    ui.display.text(10, 80, '%f %s' % (amount, currency), ui.BOLD, ui.BLACK, ui.WHITE)
    ui.display.text(10, 110, 'to this address:', ui.NORMAL, ui.BLACK, ui.WHITE)
    ui.display.text(10, 140, address[:18], ui.MONO, ui.BLACK, ui.WHITE)
    ui.display.text(10, 160, address[18:], ui.MONO, ui.BLACK, ui.WHITE)

    f = open('playground/tap_64.toig', 'r')
    _background = ui.rgbcolor(255, 255, 255)

    def func(foreground):
        ui.display.text(68, 212, 'TAP TO CONFIRM', 2, foreground, _background)

        f.seek(0)
        ui.display.icon(3, 170, f.read(), _background, foreground)

    yield from ui.animate_pulse(func, ui.BLACK, ui.GREY)  # , delay=10000)

'''
def on_read():
    print("READY TO READ")
    print(msg.read())
'''

@unimport_func
def zprava():
    from _io import BytesIO

    from trezor.messages.GetAddress import GetAddress

    m = GetAddress()
    m.address_n = [1, 2, 3]
    m.show_display = True

    print(m.__dict__)
    f = BytesIO()
    m.dump(f)
    data = f.getvalue()
    f.close()
    print(data)
    # m2 = GetAddress.load(BytesIO(data))
    # print(m2.__dict__)

def homescreen():
    print("Homescreen layout!")

    loop.call_later(5 * 1000000, layout.change(tap_to_confirm('1BitkeyP2nDd5oa64x7AjvBbbwST54W5Zmx2', 110.126967, 'BTC')))

    ui.display.bar(0, 0, 240, 240, ui.WHITE)

    f = open('playground/trezor.toig', 'r')

    def func(foreground):
        f.seek(0)
        ui.display.icon(0, 0, f.read(), foreground, ui.BLACK)
    yield from ui.animate_pulse(func, ui.WHITE, ui.GREY, speed=400000)

def run():
    ui.touch.start(lambda x, y: print('touch start %d %d\n' % (x, y)))
    ui.touch.move(lambda x, y: print('touch move %d %d\n' % (x, y)))
    ui.touch.end(lambda x, y: print('touch end %d %d\n' % (x, y)))

    # pipe.init('../pipe', on_read)
    # msg.set_notify(on_read)

    zprava()
    
    loop.call_soon(perf_info)
    loop.call_soon(layout.set_main(homescreen()))

    # loop.call_later(10 * 1000000, layout.change(tap_to_confirm('1BitkeyP2nDd5oa64x7AjvBbbwST54W5Zmx2', 110.126967, 'BTC')))
    # loop.call_soon(animate())

    loop.run_forever()
    loop.close()