import tkinter as tk
from tkinter import ttk
import random

class ACGame:
    def __init__(self, root):
        self.root = root
        self.root.title("AC Management Game")

        # Game variables
        self.num_houses = 3
        self.thermostats = [77] * self.num_houses  # Starting at 77°F (~25°C)
        self.comfort_levels = [65] * self.num_houses  # Initial comfort at 77°F
        self.energy_use = 0
        self.max_energy = 100
        self.game_over = False
        self.game_started = False
        self.selected_house = 0

        # GUI Setup
        self.house_controls = []
        self.create_widgets()

        # Bind arrow keys
        self.root.bind('<Left>', self.select_previous_house)
        self.root.bind('<Right>', self.select_next_house)
        self.root.bind('<Up>', self.increase_temp)
        self.root.bind('<Down>', self.decrease_temp)

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
        self.comfort_bar = self.comfort_canvas.create_rectangle(1, 1, 130, 19, fill='yellow')  # 65%

        # House controls
        self.houses_frame = ttk.Frame(self.root)
        self.houses_frame.pack(padx=10, pady=10)

        for i in range(self.num_houses):
            frame = ttk.LabelFrame(self.houses_frame, text=f"House {i+1}")
            frame.pack(side=tk.LEFT, padx=5)

            comfort_canvas = tk.Canvas(frame, width=102, height=20,
                                       bg='white', highlightthickness=1,
                                       highlightbackground='black')
            comfort_canvas.pack(pady=2)
            comfort_bar = comfort_canvas.create_rectangle(1, 1, 66, 19, fill='yellow')  # 65%

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
                'temp_label': temp_label,
                'comfort_label': comfort_label,
                'sel_canvas': sel_canvas,
                'rect': rect
            })

        self.update_house_selection()

        ttk.Button(self.root, text="Start Game", command=self.start_game).pack(pady=5)
        ttk.Button(self.root, text="Reset", command=self.reset_game).pack(pady=5)

    def start_game(self):
        if not self.game_started:
            self.game_started = True
            self.update_game()

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
            if temp < 82:  # ~28°C
                self.thermostats[self.selected_house] = min(82, temp + 1)
                self.update_game()

    def decrease_temp(self, event):
        if not self.game_over and self.game_started:
            temp = self.thermostats[self.selected_house]
            if temp > 61:  # ~16°C
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

    def update_game(self):
        if not self.game_started or self.game_over:
            return

        total_comfort = 0
        for i in range(self.num_houses):
            temp = self.thermostats[i]
            # Comfort: 100% at 72°F, -5% per degree deviation
            comfort = max(0, 100 - abs(temp - 72) * 5)
            self.comfort_levels[i] = comfort
            total_comfort += comfort

            # Update individual comfort meter
            comfort_width = (comfort / 100) * 100
            comfort_color = 'red' if comfort < 50 else 'yellow' if comfort < 80 else 'green'
            self.house_controls[i]['comfort_canvas'].coords(
                self.house_controls[i]['comfort_bar'], 1, 1, comfort_width, 19)
            self.house_controls[i]['comfort_canvas'].itemconfig(
                self.house_controls[i]['comfort_bar'], fill=comfort_color)

            self.house_controls[i]['comfort_label'].config(
                text=f"Comfort: {comfort:.0f}%")
            self.house_controls[i]['temp_label'].config(
                text=f"Temp: {temp:.0f}°F")

        avg_comfort = total_comfort / self.num_houses

        # Update Energy meter (adjusted for Fahrenheit)
        self.energy_use = sum(max(0, 79 - temp) * 2.5 for temp in self.thermostats)  # 79°F ~ 26°C
        energy_width = (self.energy_use / self.max_energy) * 200
        if energy_width > 200:
            energy_width = 200
        energy_color = 'green' if self.energy_use <= 50 else 'yellow' if self.energy_use <= 80 else 'red'
        self.energy_canvas.coords(self.energy_bar, 1, 1, energy_width, 19)
        self.energy_canvas.itemconfig(self.energy_bar, fill=energy_color)
        self.energy_label.config(text=f"Energy: {self.energy_use:.1f}/{self.max_energy}")

        # Update Overall Comfort meter
        comfort_width = (avg_comfort / 100) * 200
        comfort_color = 'red' if avg_comfort < 50 else 'yellow' if avg_comfort < 80 else 'green'
        self.comfort_canvas.coords(self.comfort_bar, 1, 1, comfort_width, 19)
        self.comfort_canvas.itemconfig(self.comfort_bar, fill=comfort_color)

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

    def reset_game(self):
        self.game_over = False
        self.game_started = False
        self.selected_house = 0
        for i in range(self.num_houses):
            self.thermostats[i] = 77
            self.comfort_levels[i] = 65
            self.house_controls[i]['comfort_canvas'].coords(
                self.house_controls[i]['comfort_bar'], 1, 1, 66, 19)
            self.house_controls[i]['comfort_canvas'].itemconfig(
                self.house_controls[i]['comfort_bar'], fill='yellow')
            self.house_controls[i]['comfort_label'].config(text="Comfort: 65%")
            self.house_controls[i]['temp_label'].config(text="Temp: 77°F")
        self.energy_canvas.coords(self.energy_bar, 1, 1, 1, 19)
        self.energy_canvas.itemconfig(self.energy_bar, fill='green')
        self.energy_label.config(text="Energy: 0/100")
        self.comfort_canvas.coords(self.comfort_bar, 1, 1, 130, 19)
        self.comfort_canvas.itemconfig(self.comfort_bar, fill='yellow')
        self.update_house_selection()

def main():
    root = tk.Tk()
    app = ACGame(root)
    root.mainloop()

if __name__ == "__main__":
    main()