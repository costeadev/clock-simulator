import numbers
import tkinter as tk
import math

class Hand:
    def __init__(self, start, length, rotation=0.0, fill="black"):
        self.start = start
        self.rotation = rotation
        self.length = length
        self.fill = fill
        self.update_end()

    def update_end(self):
        self.end = (
            self.start[0] + self.length * math.cos(self.rotation - math.pi / 2),
            self.start[1] + self.length * math.sin(self.rotation - math.pi / 2)
        )

class Number:
    def __init__(self, top_left, bottom_right, value):
        self.top_left = top_left
        self.bottom_right = bottom_right
        self.value = value

class Dot:
    def __init__(self, center, radius, color="black"):
        self.center = center
        self.radius = radius
        self.color = color

        self.top_left = (center[0] - self.radius, center[1] - self.radius)
        self.bottom_right = (center[0] + self.radius, center[1] + self.radius)

class Clock:
    def __init__(self, canvas, digital_clock):
        self.canvas = canvas

        width = canvas.winfo_width()
        height = canvas.winfo_height()

        self.center = (width / 2, height / 2)
        self.radius = min(width, height) / 4

        self.top_left = (
            self.center[0] - self.radius,
            self.center[1] - self.radius
        )
        self.bottom_right = (
            self.center[0] + self.radius,
            self.center[1] + self.radius
        )

        self.center_dot = Dot(self.center, 2)

        self.numbers = []

        self.digital_clock = digital_clock

        rotation = 0
        for i in range(12):
            self.numbers.append(self.new_number(i, rotation))
            rotation += math.pi / 6

        self.hour_hand = Hand(
            start=self.center_dot.center,
            length=self.radius * 0.65
        )
        self.minute_hand = Hand(
            start=self.center_dot.center,
            length=self.radius * 0.85
        )
        self.second_hand = Hand(
            start=self.center_dot.center,
            length=self.radius * 0.95,
            fill="red"
        )

        self.loop = False

    def new_number(self, i, rotation):
        new_x = self.center[0] + (self.radius - 10) * math.cos(rotation - math.pi / 2)
        new_y = self.center[1] + (self.radius - 10) * math.sin(rotation - math.pi / 2)

        return Number(new_x, new_y, (i - 1) % 12 + 1)

    def rotate_hand(self, hand, rotation):
        hand.rotation += rotation
        hand.update_end()

    def update_time(self):

        hour_degrees = round(math.degrees(self.hour_hand.rotation), 1)
        minutes_degrees = round(math.degrees(self.minute_hand.rotation), 1)
        second_degrees = round(math.degrees(self.second_hand.rotation), 1)

        hours = int(hour_degrees / 30) % 12
        minutes = int(minutes_degrees/ 6) % 60
        seconds = int(second_degrees / 6) % 60

        time = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        self.digital_clock.config(text=time)

        print(f"Hour: {hour_degrees}° Minute: {minutes_degrees}° Second:{second_degrees}°")

    def draw_clock(self):
        # Face
        self.canvas.create_oval(
            self.top_left,
            self.bottom_right,
            fill="white",
            outline='black'
        )

        # Center
        self.canvas.create_oval(
            self.center_dot.top_left,
            self.center_dot.bottom_right,
            fill=self.center_dot.color
        )

        # Numbers
        for number in self.numbers:
            self.canvas.create_text(number.top_left, number.bottom_right, text=number.value)

        # Hour hand
        self.canvas.create_line(
            self.hour_hand.start,
            self.hour_hand.end,
            width=4
        )

        # Minute hand
        self.canvas.create_line(
            self.minute_hand.start,
            self.minute_hand.end,
            width=3
        )

        # Second hand
        self.canvas.create_line(
            self.second_hand.start,
            self.second_hand.end,
            fill=self.second_hand.fill,
            width=2
        )

def move_clock(clock, seconds):
    clock.rotate_hand(clock.hour_hand, seconds * math.pi / 21600)
    clock.rotate_hand(clock.minute_hand, seconds * math.pi / 1800)
    clock.rotate_hand(clock.second_hand, seconds * math.pi / 30)

    clock.canvas.delete("all")
    clock.draw_clock()
    clock.update_time()

    if clock.loop:
        clock.after_id = clock.canvas.after(
            1000,
            lambda: move_clock(clock, seconds)
        )

def switch_loop(clock):
    clock.loop = not clock.loop

    if clock.loop:
        move_clock(clock, 1)

def main():
    window_width = 600
    window_height = 600

    root = tk.Tk()
    root.geometry(f"{window_width}x{window_height}")

    canvas = tk.Canvas(root, bd=0, highlightthickness=0, width=window_width, height=window_height)
    canvas.pack()

    digital_clock = tk.Label(
        root,
        text="00:00:00",
        font=("Arial", 24)
    )

    root.update_idletasks()

    clock = Clock(canvas, digital_clock)
    root.after(0, clock.draw_clock)

    digital_clock.place(x=window_width / 2 - digital_clock.winfo_reqwidth() / 2, y=clock.radius / 2 - digital_clock.winfo_reqheight())

    loop = False
    root.bind("<Return>", lambda event: move_clock(clock, 1))
    root.bind("<BackSpace>", lambda event: switch_loop(clock))

    root.mainloop()

if __name__ == "__main__":
    main()