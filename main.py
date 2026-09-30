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
            self.start[1] + self.length * math.sin(self.rotation - math.pi / 2),
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

        self.top_left = (self.center[0] - self.radius, self.center[1] - self.radius)
        self.bottom_right = (self.center[0] + self.radius, self.center[1] + self.radius)

        self.center_dot = Dot(self.center, 2)

        self.numbers = []

        self.digital_clock = digital_clock

        rotation = 0
        for i in range(12):
            self.numbers.append(self.new_number(i, rotation))
            rotation += math.pi / 6

        self.hour_hand = Hand(start=self.center_dot.center, length=self.radius * 0.65)
        self.minute_hand = Hand(start=self.center_dot.center, length=self.radius * 0.85)
        self.second_hand = Hand(
            start=self.center_dot.center, length=self.radius * 0.95, fill="red"
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
        self.render()

    def print_hand_degrees(self):
        hour_degrees = round(math.degrees(self.hour_hand.rotation), 1)
        minutes_degrees = round(math.degrees(self.minute_hand.rotation), 1)
        second_degrees = round(math.degrees(self.second_hand.rotation), 1)
        print(
            f"Hour: {hour_degrees}° Minute: {minutes_degrees}° Second:{second_degrees}°"
        )

    def update_time(self):
        hour_degrees = round(math.degrees(self.hour_hand.rotation), 1)
        minutes_degrees = round(math.degrees(self.minute_hand.rotation), 1)
        second_degrees = round(math.degrees(self.second_hand.rotation), 1)

        hours = int(hour_degrees / 30) % 12
        minutes = int(minutes_degrees / 6) % 60
        seconds = int(second_degrees / 6) % 60

        time = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        self.digital_clock.config(text=time)

    def render(self):
        # Face
        self.canvas.create_oval(
            self.top_left, self.bottom_right, fill="white", outline="black"
        )

        # Center
        self.canvas.create_oval(
            self.center_dot.top_left,
            self.center_dot.bottom_right,
            fill=self.center_dot.color,
        )

        # Numbers
        for number in self.numbers:
            self.canvas.create_text(
                number.top_left, number.bottom_right, text=number.value
            )

        # Hour hand
        self.hour_hand_id = self.canvas.create_line(
            self.hour_hand.start, self.hour_hand.end, width=4, tags="hand"
        )

        # Minute hand
        self.minute_hand_id = self.canvas.create_line(
            self.minute_hand.start, self.minute_hand.end, width=3, tags="hand"
        )

        # Second hand
        self.second_hand_id = self.canvas.create_line(
            self.second_hand.start,
            self.second_hand.end,
            fill=self.second_hand.fill,
            width=2,
            tags="hand",
        )


    def move(self, seconds, schedule=True):
        self.rotate_hand(self.hour_hand, seconds * math.pi / 21600)
        self.rotate_hand(self.minute_hand, seconds * math.pi / 1800)
        self.rotate_hand(self.second_hand, seconds * math.pi / 30)

        self.canvas.delete("all")
        self.render()
        self.update_time()

        if schedule and self.loop:
            self.after_id = self.canvas.after(1000, lambda: self.move(seconds))


    def switch_loop(self):
        if self.loop:
            self.loop = False
            self.canvas.after_cancel(self.after_id)
            self.after_id = None
        else:
            self.loop = True
            self.move(1)


    def set_loop(self, state):
        if self.loop:
            self.loop = state
            self.canvas.after_cancel(self.after_id)
            self.after_id = None
        else:
            self.loop = state
            self.move(self, 1)


def main():
    window_width = 960
    window_height = 1080

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

    digital_clock = tk.Label(canvas, text="00:00:00", font=("Arial", 24))

    root.update_idletasks()

    clock = Clock(canvas, digital_clock)

    clock.time_to_clock()
    clock.switch_loop()

    # ----------
    # Controls
    # ----------

    controls_frame = tk.Frame(
        root,
        width=window_width,
        height=controls_frame_height,
    )
    controls_frame.pack_propagate(False)
    controls_frame.pack()

    time_controls = tk.Frame(controls_frame)
    time_controls.pack()

    tk.Button(
        time_controls, text="- Hour", command=lambda: clock.move(-3600, False)
    ).grid(row=0, column=0)

    tk.Button(
        time_controls, text="+ Hour", command=lambda: clock.move(seconds=3600, schedule=False)
    ).grid(row=0, column=1)

    tk.Button(
        time_controls, text="- Minute", command=lambda: clock.move(seconds=-60, schedule=False)
    ).grid(row=1, column=0)

    tk.Button(
        time_controls, text="+ Minute", command=lambda: clock.move(seconds=60, schedule=False)
    ).grid(row=1, column=1)

    tk.Button(
        time_controls, text="- Second", command=lambda: clock.move(seconds=-1, schedule=False)
    ).grid(row=2, column=0)

    tk.Button(
        time_controls, text="+ Second", command=lambda: clock.move(seconds=1, schedule=False)
    ).grid(row=2, column=1)

    mode_controls = tk.Frame(controls_frame)
    mode_controls.pack(pady=10)

    (
        tk.Button(
            mode_controls, text="Start", command=lambda: clock.set_loop(True)
        ).grid(row=0, column=0)
    )

    (
        tk.Button(
            mode_controls, text="Pause", command=lambda: clock.set_loop(False)
        ).grid(row=0, column=1)
    )

    (
        tk.Button(mode_controls, text="Sync", command=clock.time_to_clock).grid(
            row=0, column=2
        )
    )

    digital_clock.place(
        x=window_width / 2 - digital_clock.winfo_reqwidth() / 2,
        y=clock.radius / 2 - digital_clock.winfo_reqheight(),
    )

    def select_hand(event):
        canvas.itemconfig("current", fill="blue")

    def deselect_hand(event):
        canvas.itemconfig("current", fill="black")

    mouse_held = False    

    def pressed(event):
        global mouse_held
        mouse_held = True
        # canvas.itemconfig("current", fill="blue")

    def released(event):
        global mouse_held
        mouse_held = False
        # canvas.itemconfig("current", fill="black")

    def moved(event):
        # print("pong")
        global mouse_held
        if mouse_held:
            print("Dragging at", event.x, event.y)
            dx = event.x - clock.center[0]
            dy = event.y - clock.center[1]

            angle = math.atan2(dy, dx) + math.pi / 2
        
            clock.minute_hand.rotation = angle
            clock.minute_hand.update_end()
            clock.render()


    root.bind("<Return>", lambda event: clock.move(3500, False))  

    canvas.tag_bind("hand","<Button-1>", pressed)
    canvas.tag_bind("hand","<ButtonRelease-1>", released)
    canvas.bind("<Motion>", moved)
    
    canvas.tag_bind("hand", "<Enter>", select_hand)
    canvas.tag_bind("hand", "<Leave>", deselect_hand)

    root.mainloop()


if __name__ == "__main__":
    main()
