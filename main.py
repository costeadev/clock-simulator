import numbers
import tkinter as tk
import math

class Hand:
    def __init__(self, start, end):
        self.start = start
        self.end = end

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
    def __init__(self, canvas):
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

        rotation = 0
        for i in range(12):
            self.numbers.append(self.new_number(i, rotation))
            rotation += math.pi / 6

        self.long_hand = Hand(start=self.center_dot.center, end=(self.center[0], self.center[1] - self.radius))
        self.short_hand = Hand(start=self.center_dot.center, end=(self.center[0], self.center[1] + self.radius / 2))


    def new_number(self, i, rotation):
        new_x = self.center[0] + (self.radius - 10) * math.cos(rotation - math.pi / 2)
        new_y = self.center[1] + (self.radius - 10) * math.sin(rotation - math.pi / 2)

        return Number(new_x, new_y, (i - 1) % 12 + 1)


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

        # Short hand
        self.canvas.create_line(self.short_hand.start, self.short_hand.end)
        
        # Long hand
        self.canvas.create_line(self.long_hand.start, self.long_hand.end)

def main():
    window_width = 600
    window_height = 600

    root = tk.Tk()
    root.geometry(f"{window_width}x{window_height}")

    canvas = tk.Canvas(root, bd=0, highlightthickness=0, width=window_width, height=window_height)
    canvas.pack()

    root.update_idletasks()

    clock = Clock(canvas)
    root.after(50, clock.draw_clock)

    root.mainloop()

if __name__ == "__main__":
    main()