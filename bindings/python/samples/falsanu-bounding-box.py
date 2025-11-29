#!/usr/bin/env python
from samplebase import SampleBase
from datetime import datetime
from rgbmatrix import graphics
import time
import random
import math

class CollisionBox:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y  # Oberkante der CollisionBox
        self.width = width
        self.height = height

    def collides_with(self, pixel_x, pixel_y, pixel_size=1):
        pixel_right = pixel_x + pixel_size
        pixel_bottom = pixel_y + pixel_size
        return (
            pixel_x < self.x + self.width and
            pixel_right > self.x and
            pixel_y < self.y + self.height and
            pixel_bottom > self.y
        )

class SimpleSquare(SampleBase):
    def __init__(self, *args, **kwargs):
        super(SimpleSquare, self).__init__(*args, **kwargs)
        self.brightness = 0.4

    def set_brightness(self, brightness):
        self.brightness = max(0.0, min(1.0, brightness))

    def run(self):
        falling_pixels = []
        stacked_pixels = {}  # Dictionary: {x: [(y, color, max_brightness, start_time, duration)]}
        num_pixels = 1000
        offset_canvas = self.matrix.CreateFrameCanvas()
        width = offset_canvas.width
        height = offset_canvas.height

        # Schriftart laden
        font = graphics.Font()
        font.LoadFont("../../../fonts/9x18B.bdf")
        r, g, b = 220, 150, 0
        text_color = graphics.Color(r, g, b)

        # Uhr-Position und CollisionBox
        font_width = 8 * 9
        font_height = 18
        pos_x = offset_canvas.width // 2 - (font_width // 2)
        pos_y = offset_canvas.height - offset_canvas.height // 2
        
        # CollisionBox direkt über der Schrift (Oberkante der Schrift)
        box_x = offset_canvas.width // 2 - (font_width // 2)
        box_y = pos_y - font_height/2+2  # Oberkante der Schrift
        box_width = font_width
        box_height = 1  # Nur eine Pixelreihe als CollisionBox

        clock_box = CollisionBox(box_x, box_y, box_width, box_height)

        while True:
            offset_canvas.Clear()
            current_time = time.time()

            # Entferne abgelaufene fallende Pixel
            falling_pixels = [
                (x, start_y, color, start_time, duration, max_brightness, fall_speed)
                for (x, start_y, color, start_time, duration, max_brightness, fall_speed) in falling_pixels
                if current_time - start_time < duration
            ]

            # Füge neue fallende Pixel hinzu
            while len(falling_pixels) < num_pixels:
                x = random.randint(0, width - 1)
                start_y = random.randint(0, height // 3)

                r = random.randint(220, 255)
                g = random.randint(100, 180)
                b = random.randint(0, 50)
                r = int(r * self.brightness)
                g = int(g * self.brightness)
                b = int(b * self.brightness)
                color = graphics.Color(r, g, b)

                duration = random.uniform(1.0, 5.0)
                max_brightness = random.uniform(0.7, 1.0)
                fall_speed = random.uniform(10.5, 20.5)
                falling_pixels.append((x, start_y, color, current_time, duration, max_brightness, fall_speed))

            new_falling_pixels = []
            for (x, start_y, color, start_time, duration, max_brightness, fall_speed) in falling_pixels:
                elapsed = current_time - start_time
                y = start_y + (elapsed * fall_speed)

                if clock_box.collides_with(x, y, 1):
                    # Füge das Pixel zum Stapel hinzu (oberhalb der CollisionBox)
                    if x not in stacked_pixels:
                        stacked_pixels[x] = []
                    # Staple Pixel nach oben (Y-Position wird kleiner)
                    stacked_y = clock_box.y - len(stacked_pixels[x]) - 1
                    stacked_pixels[x].append((stacked_y, color, max_brightness, start_time, duration))
                else:
                    progress = (current_time - start_time) / duration
                    if progress < 0.5:
                        brightness = math.sin(progress * math.pi) * max_brightness
                    else:
                        brightness = math.sin((1.0 - progress) * math.pi) * max_brightness

                    r = int(color.red * brightness)
                    g = int(color.green * brightness)
                    b = int(color.blue * brightness)
                    offset_canvas.SetPixel(int(x), int(y), r, g, b)
                    new_falling_pixels.append((x, start_y, color, start_time, duration, max_brightness, fall_speed))

            falling_pixels = new_falling_pixels

            # Zeichne gestapelte Pixel (nach oben stapeln) und entferne abgelaufene
            for x in list(stacked_pixels.keys()):
                stacked_pixels[x] = [
                    (y, color, max_brightness, start_time, duration)
                    for (y, color, max_brightness, start_time, duration) in stacked_pixels[x]
                    if current_time - start_time < duration
                ]

                for y, color, max_brightness, start_time, duration in stacked_pixels[x]:
                    progress = (current_time - start_time) / duration
                    if progress < 0.5:
                        brightness = math.sin(progress * math.pi) * max_brightness
                    else:
                        brightness = math.sin((1.0 - progress) * math.pi) * max_brightness

                    r = int(color.red * brightness)
                    g = int(color.green * brightness)
                    b = int(color.blue * brightness)
                    offset_canvas.SetPixel(int(x), int(y), r, g, b)

                if not stacked_pixels[x]:
                    del stacked_pixels[x]

            # Zeichne die Uhr
            graphics.DrawText(
                offset_canvas,
                font,
                pos_x,
                pos_y,
                text_color,
                datetime.now().strftime("%H:%M:%S")
            )

            time.sleep(0.03)
            offset_canvas = self.matrix.SwapOnVSync(offset_canvas)

if __name__ == "__main__":
    simple_square = SimpleSquare()
    if not simple_square.process():
        simple_square.print_help()

