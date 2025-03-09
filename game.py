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
        self.selected_house = 0  # Currently selected house (0-based index)

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
        self.comfort_bar = self.comfort_canvas.create_rectangle(1, 1, 100, 19, fill='yellow')

        # House controls
        self.houses_frame = ttk.Frame(self.root)
        self.houses_frame.pack(padx=10, pady=10)

        for i in range(self.num_houses):
            frame = ttk.LabelFrame(self.houses_frame, text=f"House {i+1}")
            frame.pack(side=tk.LEFT, padx=5)

            comfort = ttk.Progressbar(frame, length=100, maximum=100)
            comfort.pack()

            temp_label = ttk.Label(frame, text="Temp: 25°C")
            comfort_label = ttk.Label(frame, text="Comfort: 50%")
            temp_label.pack()
            comfort_label.pack()

            self.house_controls.append({
                'frame': frame,  # Store frame for border color
                'comfort': comfort,
                'temp_label': temp_label,
                'comfort_label': comfort_label
            })

        # Highlight first house
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
            if temp < 28:
                self.thermostats[self.selected_house] = min(28, temp + 1)
                self.update_game()

    def decrease_temp(self, event):
        if not self.game_over and self.game_started:
            temp = self.thermostats[self.selected_house]
            if temp > 16:
                self.thermostats[self.selected_house] = max(16, temp - 1)
                self.update_game()

    def update_house_selection(self):
        for i, house in enumerate(self.house_controls):
            # Highlight selected house with blue border, others with default
            color = 'blue' if i == self.selected_house else 'black'
            house['frame'].config(style=f"{color}.TLabelframe")

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
            self.house_controls[i]['temp_label'].config(
                text=f"Temp: {temp:.0f}°C")

        avg_comfort = total_comfort / self.num_houses

        # Update Energy meter
        self.energy_use = sum(max(0, 26 - temp) * 5 for temp in self.thermostats)
        energy_width = (self.energy_use / self.max_energy) * 200
        if energy_width > 200:
            energy_width = 200
        energy_color = 'green' if self.energy_use <= 50 else 'yellow' if self.energy_use <= 80 else 'red'
        self.energy_canvas.coords(self.energy_bar, 1, 1, energy_width, 19)
        self.energy_canvas.itemconfig(self.energy_bar, fill=energy_color)
        self.energy_label.config(text=f"Energy: {self.energy_use:.1f}/{self.max_energy}")

        # Update Comfort meter
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
            self.thermostats[i] = 25
            self.house_controls[i]['comfort'].config(value=50)
            self.house_controls[i]['comfort_label'].config(text="Comfort: 50%")
            self.house_controls[i]['temp_label'].config(text="Temp: 25°C")
        self.energy_canvas.coords(self.energy_bar, 1, 1, 1, 19)
        self.energy_canvas.itemconfig(self.energy_bar, fill='green')
        self.energy_label.config(text="Energy: 0/100")
        self.comfort_canvas.coords(self.comfort_bar, 1, 1, 100, 19)
        self.comfort_canvas.itemconfig(self.comfort_bar, fill='yellow')
        self.update_house_selection()

def main():
    root = tk.Tk()

    # Configure styles for house selection
    style = ttk.Style()
    style.configure("blue.TLabelframe", bordercolor="blue")
    style.configure("black.TLabelframe", bordercolor="black")

    app = ACGame(root)
    root.mainloop()

if __name__ == "__main__":
    main()