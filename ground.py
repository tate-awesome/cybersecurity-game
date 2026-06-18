import customtkinter as ctk
import math
import time


class ValueGrid(ctk.CTkFrame):
    def __init__(self, parent, title, variables):
        super().__init__(parent)

        self.labels = {}

        title_label = ctk.CTkLabel(
            self,
            text=title,
            font=ctk.CTkFont(size=16, weight="bold")
        )
        title_label.grid(row=0, column=0, columnspan=2, padx=5, pady=5)

        for row, var in enumerate(variables, start=1):
            ctk.CTkLabel(self, text=var).grid(
                row=row,
                column=0,
                sticky="w",
                padx=5,
                pady=2
            )

            value_label = ctk.CTkLabel(self, text="0")
            value_label.grid(
                row=row,
                column=1,
                sticky="e",
                padx=5,
                pady=2
            )

            self.labels[var] = value_label

    def set(self, name, value):
        if name in self.labels:
            if isinstance(value, float):
                self.labels[name].configure(text=f"{value:.2f}")
            else:
                self.labels[name].configure(text=str(value))


class App(ctk.CTk):

    DT_MS = 100
    DT = DT_MS / 1000

    def __init__(self):
        super().__init__()

        self.title("Networked HVAC Control System")
        self.geometry("1400x700")

        self.running = False
        self.mitm_enabled = False

        self.sim_time = 0.0

        # --------------------------------------------------
        # SYSTEM STATE
        # --------------------------------------------------

        self.interior_temp = 72.0
        self.vent_temp = 70.0
        self.exterior_temp = 70.0

        self.hvac_command = 0.0

        # Hidden parameters
        self.k_outside = 0.01
        self.k_vent = 0.08
        self.k_vent_response = 0.05

        self.heat_setpoint = 90.0
        self.cool_setpoint = 50.0

        # --------------------------------------------------
        # CONTROLLER STATE
        # --------------------------------------------------

        self.target_temp = 72.0
        self.reported_temp = 72.0
        self.reported_exterior_temp = 70.0
        self.temp_error = 0.0
        self.controller_output = 0.0

        self.kp = 0.08

        # --------------------------------------------------
        # PACKETS
        # --------------------------------------------------

        self.packet_interior_temp = 72.0
        self.packet_hvac_command = 0.0
        self.packet_exterior_temp = 70.0

        self.build_ui()

    # ======================================================
    # UI
    # ======================================================

    def build_ui(self):

        control_frame = ctk.CTkFrame(self)
        control_frame.pack(fill="x", padx=10, pady=10)

        ctk.CTkButton(
            control_frame,
            text="Start",
            command=self.start_sim
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            control_frame,
            text="Stop",
            command=self.stop_sim
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            control_frame,
            text="Enable MITM",
            command=lambda: self.set_mitm(True)
        ).pack(side="left", padx=20)

        ctk.CTkButton(
            control_frame,
            text="Disable MITM",
            command=lambda: self.set_mitm(False)
        ).pack(side="left")

        self.mitm_status = ctk.CTkLabel(
            control_frame,
            text="MITM: OFF"
        )
        self.mitm_status.pack(side="left", padx=20)

        main = ctk.CTkFrame(self)
        main.pack(fill="both", expand=True, padx=10, pady=10)

        # ==================================================
        # SYSTEM GRID
        # ==================================================

        self.system_grid = ValueGrid(
            main,
            "Physical System",
            [
                "interior_temp",
                "vent_temp",
                "exterior_temp",
                "hvac_command",
                "target_vent_temp"
            ]
        )
        self.system_grid.grid(row=0, column=0, sticky="nsew", padx=10)

        # ==================================================
        # CONTROLLER GRID
        # ==================================================

        self.controller_grid = ValueGrid(
            main,
            "Controller",
            [
                "target_temp",
                "reported_temp",
                "reported_exterior_temp",
                "temp_error",
                "controller_output"
            ]
        )
        self.controller_grid.grid(row=0, column=1, sticky="nsew", padx=10)

        # ==================================================
        # ATTACKER GRID
        # ==================================================

        attacker_frame = ctk.CTkFrame(main)
        attacker_frame.grid(row=0, column=2, sticky="nsew", padx=10)

        ctk.CTkLabel(
            attacker_frame,
            text="MITM Attack",
            font=ctk.CTkFont(size=16, weight="bold")
        ).grid(row=0, column=0, columnspan=3, pady=5)

        row = 1

        self.attack_vars = {}

        variables = [
            "packet_interior_temp",
            "packet_exterior_temp",
            "packet_hvac_command"
        ]

        for var in variables:

            ctk.CTkLabel(
                attacker_frame,
                text=var
            ).grid(row=row, column=0, sticky="w", padx=5)

            mult = ctk.CTkEntry(attacker_frame, width=80)
            mult.insert(0, "1.0")
            mult.grid(row=row, column=1, padx=5)

            offset = ctk.CTkEntry(attacker_frame, width=80)
            offset.insert(0, "0.0")
            offset.grid(row=row, column=2, padx=5)

            self.attack_vars[var] = {
                "mult": mult,
                "offset": offset
            }

            row += 1

        self.attacker_grid = ValueGrid(
            attacker_frame,
            "Observed Packets",
            [
                "packet_interior_temp",
                "packet_exterior_temp",
                "packet_hvac_command"
            ]
        )
        self.attacker_grid.grid(
            row=row,
            column=0,
            columnspan=3,
            pady=10
        )

        main.columnconfigure(0, weight=1)
        main.columnconfigure(1, weight=1)
        main.columnconfigure(2, weight=1)

        self.refresh_ui()

    # ======================================================
    # ATTACKS
    # ======================================================

    def apply_attack(self, variable_name, value):

        if not self.mitm_enabled:
            return value

        try:
            mult = float(
                self.attack_vars[variable_name]["mult"].get()
            )
        except:
            mult = 1.0

        try:
            offset = float(
                self.attack_vars[variable_name]["offset"].get()
            )
        except:
            offset = 0.0

        return value * mult + offset

    # ======================================================
    # CONTROLLER
    # ======================================================

    def update_controller(self):

        self.temp_error = (
            self.target_temp
            - self.reported_temp
        )

        feedforward = (
            self.k_outside *
            (
                self.target_temp
                - self.reported_exterior_temp
            )
        )

        self.controller_output = (
            self.kp * self.temp_error
            +
            4.0 * feedforward
        )

        self.controller_output = max(
            -1.0,
            min(1.0, self.controller_output)
        )

        self.packet_hvac_command = self.controller_output

    # ======================================================
    # SYSTEM
    # ======================================================

    def update_system(self):

        self.exterior_temp = (
            70
            + 15 * math.sin(self.sim_time / 20)
        )

        cmd = self.hvac_command

        target_vent_temp = (
            self.exterior_temp
            + cmd * (
                self.heat_setpoint
                - self.exterior_temp
            )
            if cmd >= 0
            else
            self.exterior_temp
            + abs(cmd)
            * (
                self.cool_setpoint
                - self.exterior_temp
            )
        )

        self.target_vent_temp = target_vent_temp

        self.vent_temp += (
            self.k_vent_response
            * (
                target_vent_temp
                - self.vent_temp
            )
        )

        self.interior_temp += (
            self.k_outside
            * (
                self.exterior_temp
                - self.interior_temp
            )
            +
            self.k_vent
            * (
                self.vent_temp
                - self.interior_temp
            )
        )

    # ======================================================
    # NETWORK
    # ======================================================

    def system_to_controller(self):

        self.packet_interior_temp = self.interior_temp
        self.packet_exterior_temp = self.exterior_temp

        self.reported_temp = self.apply_attack(
            "packet_interior_temp",
            self.packet_interior_temp
        )

        self.reported_exterior_temp = self.apply_attack(
            "packet_exterior_temp",
            self.packet_exterior_temp
        )

    def controller_to_system(self):

        attacked = self.apply_attack(
            "packet_hvac_command",
            self.packet_hvac_command
        )

        self.hvac_command = max(
            -1.0,
            min(1.0, attacked)
        )

    # ======================================================
    # SIMULATION
    # ======================================================

    def step(self):

        if not self.running:
            return

        self.sim_time += self.DT

        self.system_to_controller()

        self.update_controller()

        self.controller_to_system()

        self.update_system()

        self.refresh_ui()

        self.after(
            self.DT_MS,
            self.step
        )

    # ======================================================
    # UI UPDATE
    # ======================================================

    def refresh_ui(self):

        self.system_grid.set(
            "interior_temp",
            self.interior_temp
        )

        self.system_grid.set(
            "vent_temp",
            self.vent_temp
        )

        self.system_grid.set(
            "exterior_temp",
            self.exterior_temp
        )

        self.system_grid.set(
            "hvac_command",
            self.hvac_command
        )

        self.system_grid.set(
            "target_vent_temp",
            getattr(
                self,
                "target_vent_temp",
                self.exterior_temp
            )
        )

        self.controller_grid.set(
            "target_temp",
            self.target_temp
        )

        self.controller_grid.set(
            "reported_temp",
            self.reported_temp
        )

        self.controller_grid.set(
            "reported_exterior_temp",
            self.reported_exterior_temp
        )

        self.controller_grid.set(
            "temp_error",
            self.temp_error
        )

        self.controller_grid.set(
            "controller_output",
            self.controller_output
        )

        self.attacker_grid.set(
            "packet_interior_temp",
            self.packet_interior_temp
        )

        self.attacker_grid.set(
            "packet_exterior_temp",
            self.packet_exterior_temp
        )

        self.attacker_grid.set(
            "packet_hvac_command",
            self.packet_hvac_command
        )

    # ======================================================
    # CONTROL
    # ======================================================

    def start_sim(self):

        if self.running:
            return

        self.running = True
        self.step()

    def stop_sim(self):

        self.running = False

    def set_mitm(self, enabled):

        self.mitm_enabled = enabled

        if enabled:
            self.mitm_status.configure(
                text="MITM: ON"
            )
        else:
            self.mitm_status.configure(
                text="MITM: OFF"
            )


if __name__ == "__main__":

    ctk.set_appearance_mode("dark")

    app = App()
    app.mainloop()