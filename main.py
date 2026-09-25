from datetime import datetime
import tkinter as tk
import math
from tkinter import Button


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
        self.after_id = None

    def new_number(self, i, rotation):
        new_x = self.center[0] + (self.radius - 10) * math.cos(rotation - math.pi / 2)
        new_y = self.center[1] + (self.radius - 10) * math.sin(rotation - math.pi / 2)

        return Number(new_x, new_y, (i - 1) % 12 + 1)

    def rotate_hand(self, hand, rotation):
        hand.rotation = (hand.rotation + rotation) % (2 * math.pi)
        hand.update_end()

    def time_to_clock(self):
        now = datetime.now()

        hours = int(now.hour)
        minutes = int(now.minute)
        seconds = int(now.second)

        second_degrees = seconds * 6
        minutes_degrees = minutes * 6 + 0.1 * seconds
        hour_degrees = hours * 30 + 1 / 3 * minutes + 1 / 180 * seconds

        self.second_hand.rotation = math.radians(second_degrees)
        self.minute_hand.rotation = math.radians(minutes_degrees)
        self.hour_hand.rotation = math.radians(hour_degrees)

        self.second_hand.update_end()
        self.minute_hand.update_end()
        self.hour_hand.update_end()

        self.update_time()
        self.draw_clock()

    def update_time(self):
        hour_degrees = round(math.degrees(self.hour_hand.rotation), 1)
        minutes_degrees = round(math.degrees(self.minute_hand.rotation), 1)
        second_degrees = round(math.degrees(self.second_hand.rotation), 1)

        hours = int(hour_degrees / 30) % 12
        minutes = int(minutes_degrees / 6) % 60
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


def move_clock(clock, seconds, schedule=True):
    clock.rotate_hand(clock.hour_hand, seconds * math.pi / 21600)
    clock.rotate_hand(clock.minute_hand, seconds * math.pi / 1800)
    clock.rotate_hand(clock.second_hand, seconds * math.pi / 30)

    clock.canvas.delete("all")
    clock.draw_clock()
    clock.update_time()

    if schedule and clock.loop:
        clock.after_id = clock.canvas.after(
            1000,
            lambda: move_clock(clock, seconds)
        )


def switch_loop(clock):
    if clock.loop:
        clock.loop = False
        clock.canvas.after_cancel(clock.after_id)
        clock.after_id = None
    else:
        clock.loop = True
        move_clock(clock, 1)


def set_loop(clock, state):
    if clock.loop:
        clock.loop = state
        clock.canvas.after_cancel(clock.after_id)
        clock.after_id = None
    else:
        clock.loop = state
        move_clock(clock, 1)


def main():
    window_width = 600
    window_height = 600

    canvas_height = window_height * 2 / 3
    controls_frame_height = window_height / 3

    root = tk.Tk()
    root.geometry(f"{window_width}x{window_height}")

    canvas = tk.Canvas(
        root,
        bd=0,
        highlightthickness=0,
        width=window_width,
        height=canvas_height,
    )
    canvas.pack()

    digital_clock = tk.Label(
        canvas,
        text="00:00:00",
        font=("Arial", 24)
    )

    root.update_idletasks()

    clock = Clock(canvas, digital_clock)

    clock.time_to_clock()
    switch_loop(clock)

    # ----------
    # Controls
    # ----------

    controls_frame = tk.Frame(root, width=window_width, height=controls_frame_height, )
    controls_frame.pack_propagate(False)
    controls_frame.pack()

    time_controls = tk.Frame(controls_frame)
    time_controls.pack()

    tk.Button(
        time_controls,
        text="- Hour",
        command=lambda: move_clock(clock, -3600, False)
    ).grid(row=0, column=0)

    tk.Button(
        time_controls,
        text="+ Hour",
        command=lambda: move_clock(clock, 3600, False)
    ).grid(row=0, column=1)

    tk.Button(
        time_controls,
        text="- Minute",
        command=lambda: move_clock(clock, -60, False)
    ).grid(row=1, column=0)

    tk.Button(
        time_controls,
        text="+ Minute",
        command=lambda: move_clock(clock, 3600, False)
    ).grid(row=1, column=1)

    tk.Button(
        time_controls,
        text="- Second",
        command=lambda: move_clock(clock, -1, False)
    ).grid(row=2, column=0)

    tk.Button(
        time_controls,
        text="+ Second",
        command=lambda: move_clock(clock, 1, False)
    ).grid(row=2, column=1)

    mode_controls = tk.Frame(controls_frame)
    mode_controls.pack(pady=10)

    (tk.Button(
        mode_controls,
        text="Start",
        command=lambda: set_loop(clock, True))
     .grid(row=0, column=0))

    (tk.Button(
        mode_controls,
        text="Pause",
        command=lambda: set_loop(clock, False))
     .grid(row=0, column=1))

    (tk.Button(
        mode_controls,
        text="Sync",
        command=clock.time_to_clock)
     .grid(row=0, column=2))

    digital_clock.place(x=window_width / 2 - digital_clock.winfo_reqwidth() / 2,
                        y=clock.radius / 2 - digital_clock.winfo_reqheight())

    # back_btn = tk.Button(root, text="←", command=lambda: move_clock(clock, -1, False))
    # back_btn.place(x=0, y=0)
    # forward_btn = tk.Button(root, text="→", command=lambda: move_clock(clock, 1, False))
    # forward_btn.place(x=50, y=0)

    # btn.pack()

    root.bind("<Left>", lambda event: move_clock(clock, -1, False))
    root.bind("<Right>", lambda event: move_clock(clock, 1, False))
    root.bind("<BackSpace>", lambda event: switch_loop(clock))
    root.bind("<Control_L>", lambda event: clock.time_to_clock())

    root.mainloop()


if __name__ == "__main__":
    main()
