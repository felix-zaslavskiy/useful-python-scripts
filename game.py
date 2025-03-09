import tkinter as tk
from tkinter import ttk
import random
import math

class ACGame:
    def __init__(self, root):
        self.root = root
        self.root.title("AC Management Game")

        # Game variables
        self.num_houses = 3
        self.thermostats = [77] * self.num_houses
        self.comfort_levels = [65] * self.num_houses
        self.energy_use = 0
        self.max_energy = 100
        self.game_over = False
        self.game_started = False
        self.selected_house = 0
        self.fan_angles = [0] * self.num_houses

        # GUI Setup
        self.house_controls = []
        self.create_widgets()

        # Bind arrow keys and shortcuts
        self.root.bind('<Left>', self.select_previous_house)
        self.root.bind('<Right>', self.select_next_house)
        self.root.bind('<Up>', self.increase_temp)
        self.root.bind('<Down>', self.decrease_temp)
        self.root.bind('s', self.start_game)
        self.root.bind('r', self.reset_game)

    def create_widgets(self):
        # Energy meter
        self.energy_frame = ttk.LabelFrame(self.root, text="Energy Meter")
        self.energy_frame.pack(padx=10, pady=5)
        self.energy_canvas = tk.Canvas(self.energy_frame, width=202, height=20,
                                       bg='white', highlightthickness=1,
                                       highlightbackground='black')
        self.energy_canvas.pack()
        self.energy_bar = self.energy_canvas.create_rectangle(1, 1, 1, 19, fill='green')
        self.energy_label = ttk.Label(self.energy_frame, text="Energy: 0/100")
        self.energy_label.pack()

        # Overall comfort
        self.overall_comfort_frame = ttk.LabelFrame(self.root, text="Overall Comfort")
        self.overall_comfort_frame.pack(padx=10, pady=5)
        self.comfort_canvas = tk.Canvas(self.overall_comfort_frame, width=202, height=20,
                                        bg='white', highlightthickness=1,
                                        highlightbackground='black')
        self.comfort_canvas.pack()
        self.comfort_bar = self.comfort_canvas.create_rectangle(1, 1, 130, 19, fill='yellow')
        self.comfort_percent_label = ttk.Label(self.overall_comfort_frame, text="65%/100%")
        self.comfort_percent_label.pack()

        # House controls
        self.houses_frame = ttk.Frame(self.root)
        self.houses_frame.pack(padx=10, pady=10)

        names = ["Zach", "Dad", "Mom"]
        for i in range(self.num_houses):
            frame = ttk.LabelFrame(self.houses_frame, text=f"House {names[i]}")
            frame.pack(side=tk.LEFT, padx=5)

            comfort_canvas = tk.Canvas(frame, width=102, height=20,
                                       bg='white', highlightthickness=1,
                                       highlightbackground='black')
            comfort_canvas.pack(pady=2)
            comfort_bar = comfort_canvas.create_rectangle(1, 1, 66, 19, fill='yellow')

            temp_canvas = tk.Canvas(frame, width=102, height=20,
                                    bg='white', highlightthickness=1,
                                    highlightbackground='black')
            temp_canvas.pack(pady=2)
            temp_bar = temp_canvas.create_rectangle(1, 1, 101, 19, fill='#FFA500')

            fan_canvas = tk.Canvas(frame, width=50, height=50, bg='white')
            fan_canvas.pack(pady=2)
            center_x, center_y = 25, 25
            fan_canvas.create_oval(center_x-20, center_y-20, center_x+20, center_y+20, outline='gray')
            blades = [
                fan_canvas.create_line(center_x, center_y, center_x+15, center_y, width=2),
                fan_canvas.create_line(center_x, center_y, center_x, center_y+15, width=2),
                fan_canvas.create_line(center_x, center_y, center_x-15, center_y, width=2),
                fan_canvas.create_line(center_x, center_y, center_x, center_y-15, width=2)
            ]

            temp_label = ttk.Label(frame, text="Temp: 77°F")
            comfort_label = ttk.Label(frame, text="Comfort: 65%")
            temp_label.pack(pady=2)
            comfort_label.pack(pady=2)

            sel_canvas = tk.Canvas(frame, width=100, height=20, bg='white', highlightthickness=0)
            sel_canvas.pack(pady=2)
            rect = sel_canvas.create_rectangle(2, 2, 98, 18, outline='blue', width=2) if i == 0 else None

            self.house_controls.append({
                'frame': frame,
                'comfort_canvas': comfort_canvas,
                'comfort_bar': comfort_bar,
                'temp_canvas': temp_canvas,
                'temp_bar': temp_bar,
                'fan_canvas': fan_canvas,
                'fan_blades': blades,
                'temp_label': temp_label,
                'comfort_label': comfort_label,
                'sel_canvas': sel_canvas,
                'rect': rect
            })

        self.update_house_selection()

        ttk.Button(self.root, text="Start Game (S)", command=self.start_game).pack(pady=5)
        ttk.Button(self.root, text="Reset (R)", command=self.reset_game).pack(pady=5)

    def start_game(self, event=None):
        if not self.game_started:
            self.game_started = True
            self.update_game()
            self.animate_fans()

    def select_previous_house(self, event):
        if not self.game_over:
            self.selected_house = (self.selected_house - 1) % self.num_houses
            self.update_house_selection()

    def select_next_house(self, event):
        if not self.game_over:
            self.selected_house = (self.selected_house + 1) % self.num_houses
            self.update_house_selection()

    def increase_temp(self, event):
        if not self.game_over and self.game_started:
            temp = self.thermostats[self.selected_house]
            if temp < 82:
                self.thermostats[self.selected_house] = min(82, temp + 1)
                self.update_game()

    def decrease_temp(self, event):
        if not self.game_over and self.game_started:
            temp = self.thermostats[self.selected_house]
            if temp > 61:
                self.thermostats[self.selected_house] = max(61, temp - 1)
                self.update_game()

    def update_house_selection(self):
        for i, house in enumerate(self.house_controls):
            if i == self.selected_house:
                if house['rect'] is None:
                    house['rect'] = house['sel_canvas'].create_rectangle(2, 2, 98, 18,
                                                                         outline='blue', width=2)
            else:
                if house['rect'] is not None:
                    house['sel_canvas'].delete(house['rect'])
                    house['rect'] = None

    def get_temp_color(self, temp):
        min_temp, max_temp = 61, 82
        ratio = (temp - min_temp) / (max_temp - min_temp)
        ratio = max(0, min(1, ratio))

        colors = [
            (0, 0, 255),    # Blue at 61°F
            (255, 255, 0),  # Yellow at ~68°F
            (255, 165, 0),  # Orange at ~75°F
            (255, 0, 0)     # Red at 82°F
        ]

        if ratio <= 0.33:
            r = int(colors[0][0] + (colors[1][0] - colors[0][0]) * (ratio / 0.33))
            g = int(colors[0][1] + (colors[1][1] - colors[0][1]) * (ratio / 0.33))
            b = int(colors[0][2] + (colors[1][2] - colors[0][2]) * (ratio / 0.33))
        elif ratio <= 0.66:
            r = int(colors[1][0] + (colors[2][0] - colors[1][0]) * ((ratio - 0.33) / 0.33))
            g = int(colors[1][1] + (colors[2][1] - colors[1][1]) * ((ratio - 0.33) / 0.33))
            b = int(colors[1][2] + (colors[2][2] - colors[1][2]) * ((ratio - 0.33) / 0.33))
        else:
            r = int(colors[2][0] + (colors[3][0] - colors[2][0]) * ((ratio - 0.66) / 0.34))
            g = int(colors[2][1] + (colors[3][1] - colors[2][1]) * ((ratio - 0.66) / 0.34))
            b = int(colors[2][2] + (colors[3][2] - colors[2][2]) * ((ratio - 0.66) / 0.34))

        return f'#{r:02x}{g:02x}{b:02x}'

    def animate_fans(self):
        if not self.game_started or self.game_over:
            return
        for i, house in enumerate(self.house_controls):
            temp = self.thermostats[i]
            speed = int(30 - (temp - 61) * (25 / 21))
            self.fan_angles[i] = (self.fan_angles[i] + speed) % 360
            center_x, center_y = 25, 25
            for j, blade in enumerate(house['fan_blades']):
                angle = math.radians(self.fan_angles[i] + j * 90)
                x = center_x + 15 * math.cos(angle)
                y = center_y + 15 * math.sin(angle)
                house['fan_canvas'].coords(blade, center_x, center_y, x, y)
        self.root.after(50, self.animate_fans)

    def update_game(self):
        if not self.game_started or self.game_over:
            return

        total_comfort = 0
        for i in range(self.num_houses):
            temp = self.thermostats[i]
            comfort = max(0, 100 - abs(temp - 72) * 5)
            self.comfort_levels[i] = comfort
            total_comfort += comfort

            comfort_width = (comfort / 100) * 100
            comfort_color = 'red' if comfort < 50 else 'yellow' if comfort < 80 else 'green'
            self.house_controls[i]['comfort_canvas'].coords(
                self.house_controls[i]['comfort_bar'], 1, 1, comfort_width, 19)
            self.house_controls[i]['comfort_canvas'].itemconfig(
                self.house_controls[i]['comfort_bar'], fill=comfort_color)

            temp_color = self.get_temp_color(temp)
            self.house_controls[i]['temp_canvas'].coords(
                self.house_controls[i]['temp_bar'], 1, 1, 101, 19)
            self.house_controls[i]['temp_canvas'].itemconfig(
                self.house_controls[i]['temp_bar'], fill=temp_color)

            self.house_controls[i]['comfort_label'].config(
                text=f"Comfort: {comfort:.0f}%")
            self.house_controls[i]['temp_label'].config(
                text=f"Temp: {temp:.0f}°F")

        avg_comfort = total_comfort / self.num_houses

        self.energy_use = sum(max(0, 79 - temp) * 2.5 for temp in self.thermostats)
        energy_width = (self.energy_use / self.max_energy) * 200
        if energy_width > 200:
            energy_width = 200
        energy_color = 'green' if self.energy_use <= 50 else 'yellow' if self.energy_use <= 80 else 'red'
        self.energy_canvas.coords(self.energy_bar, 1, 1, energy_width, 19)
        self.energy_canvas.itemconfig(self.energy_bar, fill=energy_color)
        self.energy_label.config(text=f"Energy: {self.energy_use:.1f}/{self.max_energy}")

        comfort_width = (avg_comfort / 100) * 200
        comfort_color = 'red' if avg_comfort < 50 else 'yellow' if avg_comfort < 80 else 'green'
        self.comfort_canvas.coords(self.comfort_bar, 1, 1, comfort_width, 19)
        self.comfort_canvas.itemconfig(self.comfort_bar, fill=comfort_color)
        self.comfort_percent_label.config(text=f"{avg_comfort:.0f}%/100%")

        if self.energy_use > self.max_energy:
            self.show_message("Game Over", "Energy usage exceeded maximum!")
            self.game_over = True
        else:
            self.root.after(1000, self.update_game)

    def show_message(self, title, message):
        popup = tk.Toplevel()
        popup.title(title)
        ttk.Label(popup, text=message).pack(padx=20, pady=20)
        ttk.Button(popup, text="OK", command=lambda: [popup.destroy()]).pack(pady=10)

    def reset_game(self, event=None):
        self.game_over = False
        self.game_started = False
        self.selected_house = 0
        self.fan_angles = [0] * self.num_houses
        for i in range(self.num_houses):
            self.thermostats[i] = 77
            self.comfort_levels[i] = 65
            self.house_controls[i]['comfort_canvas'].coords(
                self.house_controls[i]['comfort_bar'], 1, 1, 66, 19)
            self.house_controls[i]['comfort_canvas'].itemconfig(
                self.house_controls[i]['comfort_bar'], fill='yellow')
            self.house_controls[i]['temp_canvas'].coords(
                self.house_controls[i]['temp_bar'], 1, 1, 101, 19)
            self.house_controls[i]['temp_canvas'].itemconfig(
                self.house_controls[i]['temp_bar'], fill='#FFA500')
            self.house_controls[i]['comfort_label'].config(text="Comfort: 65%")
            self.house_controls[i]['temp_label'].config(text="Temp: 77°F")
            center_x, center_y = 25, 25
            for j, blade in enumerate(self.house_controls[i]['fan_blades']):
                angle = math.radians(j * 90)
                x = center_x + 15 * math.cos(angle)
                y = center_y + 15 * math.sin(angle)
                self.house_controls[i]['fan_canvas'].coords(blade, center_x, center_y, x, y)
        self.energy_canvas.coords(self.energy_bar, 1, 1, 1, 19)
        self.energy_canvas.itemconfig(self.energy_bar, fill='green')
        self.energy_label.config(text="Energy: 0/100")
        self.comfort_canvas.coords(self.comfort_bar, 1, 1, 130, 19)
        self.comfort_canvas.itemconfig(self.comfort_bar, fill='yellow')
        self.comfort_percent_label.config(text="65%/100%")
        self.update_house_selection()

def main():
    root = tk.Tk()
    app = ACGame(root)
    root.mainloop()

if __name__ == "__main__":
    main()