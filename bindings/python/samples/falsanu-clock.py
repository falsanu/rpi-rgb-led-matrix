#!/usr/bin/env python
from samplebase import SampleBase
from datetime import datetime
from rgbmatrix import graphics
import time
import random
import math

# Current date time in local system
print(datetime.now())


class SimpleSquare(SampleBase):
    def __init__(self, *args, **kwargs):
        super(SimpleSquare, self).__init__(*args, **kwargs)
        self.brightness = 0.2

    def set_brightness(self, brightness):
        """Setzt die Helligkeit der Pixel (0.0–1.0)."""
        self.brightness = max(0.0, min(1.0, brightness))


    def run(self):

         # Liste für die aktuellen Pixel
        pixels = []
        density = 1
        num_pixels = 1500
        pixel_duration_seconds = 1.0  # in Sekunden
        
        offset_canvas = self.matrix.CreateFrameCanvas()
        
        
        width = offset_canvas.width
        height = offset_canvas.height
        font = graphics.Font()
        font.LoadFont("../../../fonts/9x18B.bdf")
        r = int(220)
        g = int(150)
        b = int(0)
        textColor = graphics.Color(r, g, b)
        posX = offset_canvas.width / 2 - (8*9/2)
        posY = offset_canvas.height - offset_canvas.height//4 
        while True:
            offset_canvas.Clear()


            # Entferne Pixel, deren Anzeigedauer abgelaufen ist
            current_time = time.time()
            pixels = [(x, y,start_y, color, start_time, duration, _,_) for (x, y,start_y, color, start_time, duration,_,_) in pixels
                  if current_time - start_time < duration]

            
            # Füge neue Pixel hinzu, falls weniger als num_pixels aktiv sind
            while len(pixels) < num_pixels:
                x = random.randint(0, width - 1)
#                y = random.randint(0, height - 1)
                # Zufällige Farbnuancen im warmen Orange-Bereich
                # R: 220–255, G: 100–180, B: 0–50
#                r = random.randint(220, 255)
#                g = random.randint(100, 180)
#                b = random.randint(0, 50)
                
                if random.choice([True, False]):
                    r = random.randint(230,255)
                    g = random.randint(230,255)
                    b = random.randint(230,255)       
                else:
                    r = random.randint(163,190)
                    g = random.randint(35,65)
                    b = random.randint(10,30)
                
                max_brightness = random.uniform(0.7, 1.0)

                r = int(r * self.brightness)
                g = int(g * self.brightness)
                b = int(b * self.brightness)

                color = graphics.Color(r, g, b)
                
                duration = random.uniform(1, 5.0)

                start_y = random.randint(0, offset_canvas.height )
                fall_speed = random.uniform(1.5, 2.5)

                
                pixels.append((x, start_y,start_y, color, current_time, duration, max_brightness, fall_speed))


            for (x, y, start_y, color, start_time, duration, max_brightness, fall_speed) in pixels:
                
                elapsed = current_time - start_time

                y = start_y + (elapsed * fall_speed)
                progress = (current_time - start_time) / duration

                # Fading-Kurve: Aufleuchten (0.0–0.5), Ausblenden (0.5–1.0)
                if progress < 0.5:
                    # Aufleuchten (sinusförmig für sanften Übergang)
                    brightness = math.sin(progress * math.pi) * max_brightness
                else:
                    # Ausblenden (sinusförmig für sanften Übergang)
                    brightness = math.sin((1.0 - progress) * math.pi) * max_brightness


                # Basis-Orange-Farbe (hell und warm)
                r = int(color.red * brightness)
                g = int(color.green * brightness)
                b = int(color.blue  * brightness)

                offset_canvas.SetPixel(int(x), int(y), r, g, b)
            
            graphics.DrawText(offset_canvas, font, posX, posY, textColor, datetime.now().strftime("%H:%M:%S"))

            time.sleep(0)

            offset_canvas = self.matrix.SwapOnVSync(offset_canvas)


# Main function
if __name__ == "__main__":
    simple_square = SimpleSquare()
    if (not simple_square.process()):
        simple_square.print_help()
