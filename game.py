import tkinter as tk
from tkinter import ttk
import math
import pygame  # Import pygame for sound

class ACGame:
    def __init__(self, root):
        self.root = root
        self.root.title("AC Management Game")

        # Initialize pygame mixer for sound
        pygame.mixer.init()


        # Game variables
        self.num_houses = 3
        self.thermostats = [77] * self.num_houses
        self.comfort_levels = [65] * self.num_houses
        self.ac_on = [True] * self.num_houses
        self.energy_use = 0
        self.max_energy = 100
        self.game_over = False
        self.game_started = False
        self.selected_house = 0
        self.fan_angles = [0] * self.num_houses

        # Load sound file (ensure 'fan_hum.wav' is in the same directory)
        self.fan_sound = pygame.mixer.Sound("fan_hum.mp3")
        self.fan_sound.set_volume(0.5)  # Default volume (0.0 to 1.0)
        self.channels = [pygame.mixer.Channel(i) for i in range(self.num_houses)]  # One channel per house

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
        # [Existing create_widgets code remains unchanged]
        self.energy_frame = ttk.LabelFrame(self.root, text="Energy Meter")
        self.energy_frame.pack(padx=10, pady=5)
        self.energy_canvas = tk.Canvas(self.energy_frame, width=202, height=20,
                                       bg='white', highlightthickness=1,
                                       highlightbackground='black')
        self.energy_canvas.pack()
        self.energy_bar = self.energy_canvas.create_rectangle(1, 1, 1, 19, fill='green')
        self.energy_label = ttk.Label(self.energy_frame, text="Energy: 0/100")
        self.energy_label.pack()

        self.overall_comfort_frame = ttk.LabelFrame(self.root, text="Overall Comfort")
        self.overall_comfort_frame.pack(padx=10, pady=5)
        self.comfort_canvas = tk.Canvas(self.overall_comfort_frame, width=202, height=20,
                                        bg='white', highlightthickness=1,
                                        highlightbackground='black')
        self.comfort_canvas.pack()
        self.comfort_bar = self.comfort_canvas.create_rectangle(1, 1, 130, 19, fill='yellow')
        self.comfort_percent_label = ttk.Label(self.overall_comfort_frame, text="65/100%")
        self.comfort_percent_label.pack()

        self.houses_frame = ttk.Frame(self.root)
        self.houses_frame.pack(padx=10, pady=10)

        names = ["Zach", "Dad", "Mom"]
        for i in range(self.num_houses):
            frame = ttk.Frame(self.houses_frame)
            frame.pack(side=tk.LEFT, padx=5)
            name_label = ttk.Label(frame, text=names[i], font=("Arial", 14), anchor="center")
            name_label.pack(fill="x")
            if i == 0:
                name_label.config(font=("Arial", 14, "bold"))

            comfort_canvas = tk.Canvas(frame, width=102, height=20,
                                       bg='white', highlightthickness=1,
                                       highlightbackground='black')
            comfort_canvas.pack(pady=2)
            comfort_bar = comfort_canvas.create_rectangle(1, 1, 66, 19, fill='yellow')

            comfort_label = ttk.Label(frame, text="Comfort: 65%")
            comfort_label.pack(pady=2)

            ssd_canvas = tk.Canvas(frame, width=60, height=35, bg='black')
            ssd_canvas.pack(pady=2)
            ssd_segments = self.create_ssd(ssd_canvas, 77)

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

            energy_frame = ttk.Frame(frame)
            energy_frame.pack(pady=2)
            bolt_canvas = tk.Canvas(energy_frame, width=30, height=30, bg='white', highlightthickness=0)
            bolt_canvas.pack(side=tk.LEFT)
            bolt_points = [15, 0, 7, 12, 13, 15, 5, 30, 20, 14, 10, 12]
            bolt_canvas.create_polygon(bolt_points, fill='yellow', outline='black')

            house_energy_canvas = tk.Canvas(energy_frame, width=82, height=20,
                                            bg='white', highlightthickness=1,
                                            highlightbackground='black')
            house_energy_canvas.pack(side=tk.LEFT)
            house_energy_bar = house_energy_canvas.create_rectangle(1, 1, 1, 19, fill='green')

            self.house_controls.append({
                'frame': frame,
                'name_label': name_label,
                'comfort_canvas': comfort_canvas,
                'comfort_bar': comfort_bar,
                'temp_canvas': temp_canvas,
                'temp_bar': temp_bar,
                'fan_canvas': fan_canvas,
                'fan_blades': blades,
                'ssd_canvas': ssd_canvas,
                'ssd_segments': ssd_segments,
                'comfort_label': comfort_label,
                'house_energy_canvas': house_energy_canvas,
                'house_energy_bar': house_energy_bar
            })

        self.update_house_selection()

        ttk.Button(self.root, text="Start Game (S)", command=self.start_game).pack(pady=5)
        ttk.Button(self.root, text="Reset (R)", command=self.reset_game).pack(pady=5)

    def create_ssd(self, canvas, temp):
        # [Unchanged]
        segments = [
            [1, 1, 1, 0, 1, 1, 1],  # 0
            [0, 0, 1, 0, 0, 1, 0],  # 1
            [1, 0, 1, 1, 1, 0, 1],  # 2
            [1, 0, 1, 1, 0, 1, 1],  # 3
            [0, 1, 1, 1, 0, 1, 0],  # 4
            [1, 1, 0, 1, 0, 1, 1],  # 5
            [1, 1, 0, 1, 1, 1, 1],  # 6
            [1, 0, 1, 0, 0, 1, 0],  # 7
            [1, 1, 1, 1, 1, 1, 1],  # 8
            [1, 1, 1, 1, 0, 1, 1]   # 9
        ]

        tens = temp // 10
        ones = temp % 10
        segment_list = []

        x_offset = 5
        segment_list.extend(self.draw_digit(canvas, segments[tens], x_offset))

        x_offset = 30
        segment_list.extend(self.draw_digit(canvas, segments[ones], x_offset))

        return segment_list

    def draw_digit(self, canvas, pattern, x_offset):
        # [Unchanged]
        segment_coords = [
            (x_offset + 5, 7, x_offset + 15, 7),    # Top
            (x_offset + 5, 9, x_offset + 5, 19),   # Top-left
            (x_offset + 15, 9, x_offset + 15, 19), # Top-right
            (x_offset + 5, 20, x_offset + 15, 20), # Middle
            (x_offset + 5, 21, x_offset + 5, 31),  # Bottom-left
            (x_offset + 15, 21, x_offset + 15, 31),# Bottom-right
            (x_offset + 5, 32, x_offset + 15, 32)  # Bottom
        ]

        segments = []
        for i, on in enumerate(pattern):
            if on:
                segments.append(canvas.create_line(
                    segment_coords[i][0], segment_coords[i][1],
                    segment_coords[i][2], segment_coords[i][3],
                    fill='red', width=2
                ))
            else:
                segments.append(None)
        return segments

    def update_ssd(self, canvas, segments, temp):
        # [Unchanged]
        for seg in segments:
            if seg:
                canvas.delete(seg)
        return self.create_ssd(canvas, temp)

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
                self.ac_on[self.selected_house] = self.thermostats[self.selected_house] < 79
                self.update_game()

    def decrease_temp(self, event):
        if not self.game_over and self.game_started:
            temp = self.thermostats[self.selected_house]
            if temp > 61:
                self.thermostats[self.selected_house] = max(61, temp - 1)
                self.ac_on[self.selected_house] = self.thermostats[self.selected_house] < 79
                self.update_game()

    def update_house_selection(self):
        for i, house in enumerate(self.house_controls):
            if i == self.selected_house:
                house['name_label'].config(font=("Arial", 14, "bold"))
                # Sound will be handled by animate_fans; no need to start it here
            else:
                house['name_label'].config(font=("Arial", 14))
                self.channels[i].stop()  # Stop sound for non-selected houses

    def get_temp_color(self, temp):
        # [Unchanged]
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
            if self.ac_on[i]:
                temp = self.thermostats[i]
                speed = int(30 - (temp - 61) * (25 / 21))
                self.fan_angles[i] = (self.fan_angles[i] + speed) % 360
                center_x, center_y = 25, 25
                for j, blade in enumerate(house['fan_blades']):
                    angle = math.radians(self.fan_angles[i] + j * 90)
                    x = center_x + 15 * math.cos(angle)
                    y = center_y + 15 * math.sin(angle)
                    house['fan_canvas'].coords(blade, center_x, center_y, x, y)

                # Adjust sound volume based on fan speed
                if i == self.selected_house:
                    volume = max(0.1, 1.0 - (temp - 61) / 17)
                    self.channels[i].set_volume(volume)
                    if not self.channels[i].get_busy():
                        self.channels[i].play(self.fan_sound, loops=-1)
                else:
                    self.channels[i].stop()
            else:
                # Reset fan blades and stop sound for non-selected or AC-off houses
                center_x, center_y = 25, 25
                for j, blade in enumerate(house['fan_blades']):
                    angle = math.radians(j * 90)
                    x = center_x + 15 * math.cos(angle)
                    y = center_y + 15 * math.sin(angle)
                    house['fan_canvas'].coords(blade, center_x, center_y, x, y)
                self.channels[i].stop()


        self.root.after(50, self.animate_fans)

    def update_game(self):
        if not self.game_started or self.game_over:
            return

        total_comfort = 0
        house_energy_values = []
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

            self.house_controls[i]['ssd_segments'] = self.update_ssd(
                self.house_controls[i]['ssd_canvas'],
                self.house_controls[i]['ssd_segments'],
                temp
            )

            self.house_controls[i]['comfort_label'].config(
                text=f"Comfort: {comfort:.0f}%")

            house_energy = (max(0, 79 - temp) * 2.5) if self.ac_on[i] else 0
            house_energy_values.append(house_energy)
            house_energy_width = (house_energy / 45) * 80
            if house_energy_width > 80:
                house_energy_width = 80
            house_energy_color = 'green' if house_energy_width <= 25 else 'yellow' if house_energy_width <= 50 else 'red'
            self.house_controls[i]['house_energy_canvas'].coords(
                self.house_controls[i]['house_energy_bar'], 1, 1, house_energy_width, 19)
            self.house_controls[i]['house_energy_canvas'].itemconfig(
                self.house_controls[i]['house_energy_bar'], fill=house_energy_color)

        avg_comfort = total_comfort / self.num_houses

        self.energy_use = sum(house_energy_values)
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
        self.comfort_percent_label.config(text=f"{avg_comfort:.0f}/100%")

        if self.energy_use > self.max_energy:
            self.show_message("Game Over", "Energy usage exceeded maximum!")
            self.game_over = True
        else:
            self.root.after(1000, self.update_game)

    def show_message(self, title, message):
        # [Unchanged]
        popup = tk.Toplevel()
        popup.title(title)
        ttk.Label(popup, text=message).pack(padx=20, pady=20)
        ttk.Button(popup, text="OK", command=lambda: [popup.destroy()]).pack(pady=10)

    def reset_game(self, event=None):
        self.game_over = False
        self.game_started = False
        self.selected_house = 0
        self.fan_angles = [0] * self.num_houses
        self.ac_on = [True] * self.num_houses
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
            self.house_controls[i]['ssd_segments'] = self.update_ssd(
                self.house_controls[i]['ssd_canvas'],
                self.house_controls[i]['ssd_segments'],
                77
            )
            self.house_controls[i]['comfort_label'].config(text="Comfort: 65%")
            self.house_controls[i]['house_energy_canvas'].coords(
                self.house_controls[i]['house_energy_bar'], 1, 1, 1, 19)
            self.house_controls[i]['house_energy_canvas'].itemconfig(
                self.house_controls[i]['house_energy_bar'], fill='green')
            center_x, center_y = 25, 25
            for j, blade in enumerate(self.house_controls[i]['fan_blades']):
                angle = math.radians(j * 90)
                x = center_x + 15 * math.cos(angle)
                y = center_y + 15 * math.sin(angle)
                self.house_controls[i]['fan_canvas'].coords(blade, center_x, center_y, x, y)
            self.channels[i].stop()  # Stop sound on reset
        self.energy_canvas.coords(self.energy_bar, 1, 1, 1, 19)
        self.energy_canvas.itemconfig(self.energy_bar, fill='green')
        self.energy_label.config(text="Energy: 0/100")
        self.comfort_canvas.coords(self.comfort_bar, 1, 1, 130, 19)
        self.comfort_canvas.itemconfig(self.comfort_bar, fill='yellow')
        self.comfort_percent_label.config(text="65/100%")
        self.update_house_selection()

def main():
    root = tk.Tk()
    app = ACGame(root)
    root.mainloop()

if __name__ == "__main__":
    main()