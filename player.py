import argparse
import time
import sys
import os

sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/..'))
from rgbmatrix import RGBMatrix, RGBMatrixOptions

from rgbmatrix import graphics
import time

class HardwareBase(object):
    def __init__(self, *args, **kwargs):
        self.parser = argparse.ArgumentParser()

        self.parser.add_argument("-r", "--led-rows", action="store", help="Display rows. 16 for 16x32, 32 for 32x32. Default: 32", default=32, type=int)
        self.parser.add_argument("--led-cols", action="store", help="Panel columns. Typically 32 or 64. (Default: 32)", default=64, type=int)
        self.parser.add_argument("-c", "--led-chain", action="store", help="Daisy-chained boards. Default: 1.", default=1, type=int)
        self.parser.add_argument("-P", "--led-parallel", action="store", help="For Plus-models or RPi2: parallel chains. 1..3. Default: 1", default=1, type=int)
        self.parser.add_argument("-p", "--led-pwm-bits", action="store", help="Bits used for PWM. Something between 1..11. Default: 11", default=11, type=int)
        self.parser.add_argument("-b", "--led-brightness", action="store", help="Sets brightness level. Default: 100. Range: 1..100", default=100, type=int)
        self.parser.add_argument("-m", "--led-gpio-mapping", help="Hardware Mapping: regular, adafruit-hat, adafruit-hat-pwm" , choices=['regular', 'adafruit-hat', 'adafruit-hat-pwm'], type=str)
        self.parser.add_argument("--led-scan-mode", action="store", help="Progressive or interlaced scan. 0 Progressive, 1 Interlaced (default)", default=1, choices=range(2), type=int)
        self.parser.add_argument("--led-pwm-lsb-nanoseconds", action="store", help="Base time-unit for the on-time in the lowest significant bit in nanoseconds. Default: 130", default=130, type=int)
        self.parser.add_argument("--led-show-refresh", action="store_true", help="Shows the current refresh rate of the LED panel")
        self.parser.add_argument("--led-slowdown-gpio", action="store", help="Slow down writing to GPIO. Range: 1..100. Default: 1", choices=range(3), type=int)
        self.parser.add_argument("--led-no-hardware-pulse", action="store", help="Don't use hardware pin-pulse generation")
        self.parser.add_argument("--led-rgb-sequence", action="store", help="Switch if your matrix has led colors swapped. Default: RGB", default="RGB", type=str)
        self.parser.add_argument("--led-pixel-mapper", action="store", help="Apply pixel mappers. e.g \"Rotate:90\"", default="", type=str)
        self.parser.add_argument("--led-row-addr-type", action="store", help="0 = default; 1=AB-addressed panels;2=row direct", default=0, type=int, choices=[0,1,2])
        self.parser.add_argument("--led-multiplexing", action="store", help="Multiplexing type: 0=direct; 1=strip; 2=checker; 3=spiral; 4=ZStripe; 5=ZnMirrorZStripe; 6=coreman; 7=Kaler2Scan; 8=ZStripeUneven (Default: 0)", default=0, type=int)

    def usleep(self, value):
        time.sleep(value / 1000000.0)

    def run(self):
        print("Running")

    def process(self):
        
        self.args = self.parser.parse_args()

        options = RGBMatrixOptions()

        if self.args.led_gpio_mapping != None:
            options.hardware_mapping = self.args.led_gpio_mapping
        options.rows = self.args.led_rows
        options.cols = self.args.led_cols
        options.chain_length = self.args.led_chain
        options.parallel = self.args.led_parallel
        options.row_address_type = self.args.led_row_addr_type
        options.multiplexing = self.args.led_multiplexing
        options.pwm_bits = self.args.led_pwm_bits
        options.brightness = self.args.led_brightness
        options.pwm_lsb_nanoseconds = self.args.led_pwm_lsb_nanoseconds
        options.led_rgb_sequence = self.args.led_rgb_sequence
        options.pixel_mapper_config = self.args.led_pixel_mapper
        if self.args.led_show_refresh:
            options.show_refresh_rate = 1

        if self.args.led_slowdown_gpio != None:
            options.gpio_slowdown = self.args.led_slowdown_gpio
        if self.args.led_no_hardware_pulse:
            options.disable_hardware_pulsing = True

        self.matrix = RGBMatrix(options = options)

        try:
            # Start loop
            self.run()
        except KeyboardInterrupt:
            print("Exiting\n")
            sys.exit(0)

        return True

def four_byte_int(data):
    return int.from_bytes(data,byteorder='little')    

class RunPlayer(HardwareBase):
    def __init__(self, *args, **kwargs):
        super(RunPlayer, self).__init__(*args, **kwargs)
        
        """
        self._movies = []
        
        # Load the list of movies        
        with open('a.bin','rb') as mf:
            _ = mf.read(16)
            read = 16
            while True:
                movie_info = mf.read(16)
                read += 16
                if movie_info[0] == 0:
                    break
                start_sector = four_byte_int(movie_info[12:16])
                i = movie_info.index(b'\x00')
                name = movie_info[0:i]
                self._movies.append({'name':name,'start_sector':start_sector})
        
            mf.read(512-read)
        
            mh = mf.read(512)
            print(mh)
            cnt = four_byte_int(mh[0:4])
            delay = four_byte_int(mh[4:8])
        """    
            

    def run(self):
        
        while True:        
            
            with open('a.bin','rb') as mf:
                mf.read(512) # List of movies
                while True:
                    sec = mf.read(512) # Movie info
                    cnt = four_byte_int(sec[0:4])
                    delay = four_byte_int(sec[4:8])
                    if cnt==0:
                        break
                    sec = mf.read(1024) # Colors
                    colors = []
                    for i in range(256):
                        # 00 GG RR BB
                        g = sec[i*4+2]
                        r = sec[i*4+1]
                        b = sec[i*4]                    
                        colors.append([r,g,b])
                        #print([r,g,b])
                    for _ in range(cnt):
                        sec = mf.read(2048)
                        offscreen_canvas = self.matrix.CreateFrameCanvas()
                        for y in range(32):
                            for x in range(64):
                                v = sec[y*64+x]
                                c = colors[v]
                                #if v!=0:
                                #    print(c)                            
                                offscreen_canvas.SetPixel(x,y,c[0],c[1],c[2])
                        self.matrix.SwapOnVSync(offscreen_canvas)
                        time.sleep(delay/1000) 
    
# Main function
if __name__ == "__main__":
    run_text = RunPlayer()
    if (not run_text.process()):
        run_text.print_help()
