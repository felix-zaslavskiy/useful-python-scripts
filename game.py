import tkinter as tk
from tkinter import ttk
import random

class ACGame:
    def __init__(self, root):
        self.root = root
        self.root.title("AC Management Game")

        # Game variables
        self.num_houses = 3
        self.thermostats = [25] * self.num_houses
        self.comfort_levels = [50] * self.num_houses
        self.energy_use = 0
        self.max_energy = 100
        self.game_over = False
        self.game_started = False

        # GUI Setup
        self.house_controls = []
        self.create_widgets()

    def create_widgets(self):
        # Style configuration
        self.style = ttk.Style()
        self.style.configure("green.Horizontal.TProgressbar", background='green')
        self.style.configure("yellow.Horizontal.TProgressbar", background='yellow')
        self.style.configure("red.Horizontal.TProgressbar", background='red')

        # Overall meters
        self.energy_frame = ttk.LabelFrame(self.root, text="Energy Meter")
        self.energy_frame.pack(padx=10, pady=5)
        self.energy_meter = ttk.Progressbar(self.energy_frame, length=200,
                                            maximum=self.max_energy,
                                            style="green.Horizontal.TProgressbar")
        self.energy_meter.pack()
        self.energy_label = ttk.Label(self.energy_frame, text="Energy: 0/100")
        self.energy_label.pack()

        self.overall_comfort_frame = ttk.LabelFrame(self.root, text="Overall Comfort")
        self.overall_comfort_frame.pack(padx=10, pady=5)
        self.overall_comfort = ttk.Progressbar(self.overall_comfort_frame,
                                               length=200, maximum=100)
        self.overall_comfort.pack()

        # House controls
        self.houses_frame = ttk.Frame(self.root)
        self.houses_frame.pack(padx=10, pady=10)

        for i in range(self.num_houses):
            frame = ttk.LabelFrame(self.houses_frame, text=f"House {i+1}")
            frame.pack(side=tk.LEFT, padx=5)

            comfort = ttk.Progressbar(frame, length=100, maximum=100)
            comfort.pack()

            temp = ttk.Scale(frame, from_=16, to=28, orient=tk.HORIZONTAL)
            temp.set(25)
            temp.config(command=lambda x, idx=i: self.update_thermostat(idx, float(x)))
            temp.pack()

            temp_label = ttk.Label(frame, text="Temp: 25°C")
            comfort_label = ttk.Label(frame, text="Comfort: 50%")
            temp_label.pack()
            comfort_label.pack()

            self.house_controls.append({
                'comfort': comfort,
                'temp': temp,
                'temp_label': temp_label,
                'comfort_label': comfort_label
            })

        ttk.Button(self.root, text="Start Game", command=self.start_game).pack(pady=5)
        ttk.Button(self.root, text="Reset", command=self.reset_game).pack(pady=5)

    def start_game(self):
        if not self.game_started:
            self.game_started = True
            self.update_game()

    def update_thermostat(self, house_idx, temp):
        if house_idx < len(self.thermostats):
            self.thermostats[house_idx] = temp
            self.house_controls[house_idx]['temp_label'].config(
                text=f"Temp: {temp:.1f}°C")
            if self.game_started:
                self.update_game()

    def update_game(self):
        if not self.game_started or self.game_over:
            return

        total_comfort = 0
        for i in range(self.num_houses):
            temp = self.thermostats[i]
            comfort = max(0, 100 - abs(temp - 20) * 10)
            self.comfort_levels[i] = comfort
            total_comfort += comfort

            self.house_controls[i]['comfort'].config(value=comfort)
            self.house_controls[i]['comfort_label'].config(
                text=f"Comfort: {comfort:.0f}%")

        avg_comfort = total_comfort / self.num_houses
        self.overall_comfort.config(value=avg_comfort)

        self.energy_use = sum(max(0, 26 - temp) * 5 for temp in self.thermostats)
        self.energy_meter.config(value=self.energy_use)
        self.energy_label.config(text=f"Energy: {self.energy_use:.1f}/{self.max_energy}")

        # Update energy meter color
        print(f"Energy use: {self.energy_use}")  # Debug print
        if self.energy_use > 80:
            self.energy_meter.configure(style="red.Horizontal.TProgressbar")
            print("Should be red")
        elif self.energy_use > 50:
            self.energy_meter.configure(style="yellow.Horizontal.TProgressbar")
            print("Should be yellow")
        else:
            self.energy_meter.configure(style="green.Horizontal.TProgressbar")
            print("Should be green")

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
        for i in range(self.num_houses):
            self.thermostats[i] = 25
            self.house_controls[i]['temp'].set(25)
            self.house_controls[i]['comfort'].config(value=50)
            self.house_controls[i]['comfort_label'].config(text="Comfort: 50%")
        self.energy_meter.config(value=0, style="green.Horizontal.TProgressbar")
        self.energy_label.config(text="Energy: 0/100")
        self.overall_comfort.config(value=50)

def main():
    root = tk.Tk()
    app = ACGame(root)
    root.mainloop()

if __name__ == "__main__":
    main()