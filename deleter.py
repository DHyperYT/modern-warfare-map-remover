import os
import tkinter as tk
from tkinter import messagebox, filedialog, Frame

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(__file__)
    return os.path.join(base_path, relative_path)

class MapDeleterApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Modern Warfare Map Remover")
        self.geometry("800x400")
        self.config(bg="#000")
        self.resizable(False, False)
        
        icon_path = resource_path('icon.ico')
        self.iconbitmap(icon_path)

# Map names and corresponding IDS
        self.maps = {
            "Core": {
                "Al-Raab Airbase": "mp_herat", "Aniyah Incursion": "mp_aniyah_tac", "Arklov Peak": "mp_deadzone",
                "Atlas Superstore": "mp_emporium", "Azhir Cave (Day & Night)": "mp_cave",
                "Broadcast": "mp_broadcast2", "Cheshire Park": "mp_garden", "Crash": "mp_crash",
                "Euphrates Bridge": "mp_euphrates", "Grazna Raid": "mp_raid",
                "Gun Runner (Day & Night)": "mp_runner", "Hackney Yard (Day & Night)": "mp_hackney", "Hardhat": "mp_hardhat", "Hovec Sawmill": "mp_village2",
                "Khandor Hideout": "mp_hideout", "Killhouse": "mp_killhouse",
                "Mialstor Tank Factory": "mp_malyshev", "Petrov Oil Rig": "mp_oilrig", "Piccadilly": "mp_piccadilly",
                "Rammaza (Day & Night)": "mp_spear", "Rust": "mp_rust",
                "Scrapyard": "mp_scrapyard", "Shipment": "mp_shipment", "St. Petrograd": "mp_petrograd",
                "Suldal Harbor": "mp_harbor", "Talsik Backlot": "mp_backlot2",
                "Vacant": "mp_vacant"
            },
            "Ground War": {
                "Aniyah Palace (& Aniyah Incursion)": "mp_aniyah",
                "Barakett Promenade": "mp_promenade_gw",
                "Karst River Quarry": "mp_quarry2",
                "Krovnik Farmland": "mp_farms2",
                "Port of Verdansk": "mp_port2_gw",
                "Tavorsk District": "mp_downtown_gw",
                "Verdansk International Airport": "mp_layover_gw",
                "Verdansk Riverside": "mp_riverside_gw",
                "Zhokov Boneyard": "mp_boneyard_gw"
            },
            "Gunfight": {
                "Aisle 9": "mp_m_walco2", "Atrium": "mp_m_cage", "Bazaar": "mp_m_fork",
                "Cargo": "mp_m_cargo", "Docks": "mp_m_overunder", "Drainage": "mp_m_drainage",
                "Gulag Showers": "mp_m_showers", "Hill": "mp_m_hill", "King": "mp_m_king",
                "Livestock": "mp_m_cornfield", "Pine": "mp_m_pine", "Shoot House (& Speedball)": "mp_m_speed", "Speedball": "mp_m_speedball", "Stack": "mp_m_stack", "Station": "mp_m_train", "Trench": "mp_m_trench",
                "Verdansk Stadium": "mp_m_stadium", "Winter Docks": "mp_m_overwinter"
            },
            "Training": {
                "Gun Course": "mp_t_gun_course",
                "Marksman Range": "mp_t_sn_reflex",
                "Training Range": "mp_t_reflex"
            },
            "Warzone": {
                "CALDERA": "mp_wz_island",
                "Verdansk '84": "don4",
                "Verdansk": "donetsk",
                "Caldera Archipelago Airbase": "mp_br_tut2",
                "Rebirth Island": "escape4",
                "Fortune's Keep": "mp_sm_island_1"
            }
        }

        self.map_directory = ""
        self.visible_maps_count = 1  # Number of visible map buttons

        self.main_frame = Frame(self, bg="#000")
        self.main_frame.pack(fill="both", expand=True)

        self.create_directory_selection()

    def create_directory_selection(self):
        self.label = tk.Label(self.main_frame, text="Select the directory containing your Steam installation of Modern Warfare:", bg="black", fg="white", font=("Helvetica", 14))
        self.label.pack(pady=20)

        self.dir_button = tk.Button(self.main_frame, text="Browse", command=self.browse_directory, font=("Helvetica", 16))
        self.dir_button.pack(pady=10)

        self.start_button = tk.Button(self.main_frame, text="Start", command=self.start_app, font=("Helvetica", 16))
        self.start_button.pack(pady=10)
        self.start_button.config(state=tk.DISABLED) 

    def browse_directory(self):
        self.map_directory = filedialog.askdirectory()
        if self.map_directory:
            self.label.config(text=f"Selected directory: {self.map_directory}")
            self.start_button.config(state=tk.NORMAL)

    def start_app(self):
        self.clear_main_frame() 
        self.open_category_selection()

    def open_category_selection(self):
        tk.Label(self.main_frame, text="Select a map category:", bg="black", fg="white", font=("Helvetica", 14)).pack(pady=20)

        for category in self.maps.keys():
            btn = tk.Button(self.main_frame, text=category, command=lambda cat=category: self.select_category(cat), font=("Helvetica", 12))
            btn.pack(pady=5)

        back_button = tk.Button(self.main_frame, text="Back", command=self.reset_app, font=("Helvetica", 12))
        back_button.pack(pady=20)

    def select_category(self, category):
        self.open_map_selection_window(category)

    def open_map_selection_window(self, category):
        map_window = tk.Toplevel(self)
        map_window.title(f"{category}")
        map_window.geometry("800x200")
        map_window.config(bg="black")

        tk.Label(map_window, text=f"Select a {category} map to delete using the arrows and click it:", bg="black", fg="white", font=("Helvetica", 14)).pack(pady=10)

        frame = Frame(map_window)
        frame.pack(pady=20)

        left_arrow = tk.Button(frame, text="<", command=lambda: self.scroll_maps(-1, category, map_window), font=("Helvetica", 16), width=5)
        left_arrow.pack(side="left", padx=10)

        # Create a frame for the map buttons
        self.map_frame = Frame(map_window)
        self.map_frame.pack(pady=20)

        self.current_index = 0
        self.display_map_buttons(category)

        right_arrow = tk.Button(frame, text=">", command=lambda: self.scroll_maps(1, category, map_window), font=("Helvetica", 16), width=5)
        right_arrow.pack(side="right", padx=10)

    def display_map_buttons(self, category):
        for widget in self.map_frame.winfo_children():
            widget.destroy()

        map_names = list(self.maps[category].keys())
        num_maps = len(map_names)

        start_index = self.current_index
        end_index = min(start_index + self.visible_maps_count, num_maps)

        # Create buttons for the visible maps
        for i in range(start_index, end_index):
            map_name = map_names[i]
            button = tk.Button(self.map_frame, text=map_name, command=lambda map_name=map_name: self.delete_map(map_name, category),
            font=("Helvetica", 14), width=20, height=3)
            button.pack(side="left", padx=10)

            if i == self.current_index:
                button.config(bg="white")
            elif i == (self.current_index - 1) % num_maps or i == (self.current_index + 1) % num_maps:
                button.config(bg="lightgray")  # Light gray for adjacent buttons (useless for now)
            else:
                button.config(bg="darkgray")  # Dark gray for non-centered buttons (useless for now)

    def scroll_maps(self, direction, category, map_window):
        self.current_index = (self.current_index + direction) % len(self.maps[category])
        self.display_map_buttons(category)

    def delete_map(self, map_name, category):
        map_id = self.maps[category][map_name]
        result = messagebox.askyesno("Delete Map", f"Do you really want to delete all files containing '{map_id}' for {map_name}?")
        if result:
            # Delete all files that contain the map_id in their file name, ignoring techsets_ files
            deleted_files = 0
            for root, dirs, files in os.walk(self.map_directory):
                for file in files:
                    if map_id in file and not file.startswith("techsets_"):  # Ignore techsets_ files
                        try:
                            os.remove(os.path.join(root, file))
                            deleted_files += 1
                        except Exception as e:
                            messagebox.showerror("Error", f"Error deleting {file}: {str(e)}")
            if deleted_files > 0:
                messagebox.showinfo("Success", f"Deleted {deleted_files} files for {map_name}.")
            else:
                messagebox.showinfo("No Files Found", f"No files found for {map_name} with ID '{map_id}'.")

    def clear_main_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def reset_app(self):
        self.clear_main_frame()
        self.create_directory_selection()

if __name__ == "__main__":
    app = MapDeleterApp()
    app.mainloop()
