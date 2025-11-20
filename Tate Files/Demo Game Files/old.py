



#Create sniffer frame on button press
def sniffer_pane(container, btn, model_container, net_size, right_pane):
    # Sniffer frame
    btn.config(state="disabled")
    sniffer_frame = tk.Frame(container)
    sniffer_frame.pack(side="top", fill="both", expand=True, padx=5, pady=5)
    sniffer_label = tk.Label(sniffer_frame, text="Sniffer Sniffing Data:")
    sniffer_label.pack(side="top", pady=7, padx=10)
    sniffer_data = scrolledtext.ScrolledText(sniffer_frame)
    sniffer_data.pack(side="top", padx=10)
    sniffer_data.config(state="disabled")
    decipher_frame = tk.Frame(sniffer_frame)
    decipher_frame.pack(side="top", padx=10, expand=True)
    decipher_button = tk.Button(decipher_frame, text="Decipher Packets", command=lambda:hacker_pane(right_pane, decipher_button))
    decipher_button.pack(side="right")

    # Sniffer data stream
    global boat
    boat = network.Boat()
    boat.start()
    boat_history = []
    # Listering loop
    def intercept_data():
        try:
            data = boat.send_queue.get_nowait()
            # data = []
            # for d in boat_data:
            #     data.append(float(d))
            # Add to sniffer
            sniffer_data.config(state="normal")
            boat_history.append(copy.deepcopy(data))
            if simplify_data == True:
                        # 0x 1y 2dir 3speed 4rudder

                entry = f"X: {math.floor(data[0]):05d}\n"\
                        f"Y: {math.floor(data[1]):05d}\n"\
                        f"θ: {math.floor(data[2]*180/2*math.pi):.2f}\n"\
                        f"Propellor: {math.floor(data[3]):03d}\n"\
                        f"Rudder: {math.floor(data[4]*180/math.pi):.2f}\n"
                sniffer_data.insert(tk.END, entry + "\n")

            else:
                sniffer_data.insert(tk.END, str(data) + "\n")
                
            sniffer_data.see(tk.END)
            sniffer_data.config(state="disabled")
            # Draw new position
            redraw_boat_canvas(boat_history)
            redraw_network_canvas()
            container.after(50, intercept_data)
        except:
            container.after(50, intercept_data)
    intercept_data()

    def redraw_network_canvas():
        network_canvas.delete("all")
        width = float(network_canvas.winfo_width())
        height = float(network_canvas.winfo_height())
        rectwidth = 100
        margin = 10
        wiredist = height/5
        model_color = "dark gray"
        roll = random.randint(1,4)
        wire_color = model_color
        if roll > 1:
            wire_color = "yellow"
        
        network_canvas.create_rectangle(0, 0, width, height, fill="#6F8695")
        network_canvas.create_rectangle(margin, margin, rectwidth+margin, height-margin, fill=model_color, outline="black")
        network_canvas.create_rectangle(width-margin-rectwidth, margin, width-margin, height-margin, fill=model_color, outline="black")
        network_canvas.create_line(margin+rectwidth, margin+wiredist, width-margin-rectwidth, margin+wiredist, fill=wire_color, width=3)
        network_canvas.create_line(margin+rectwidth, height-margin-wiredist, width-margin-rectwidth, height-margin-wiredist, fill=wire_color, width=3)
        network_canvas.create_text(margin+rectwidth/2, margin*2, anchor="n", text="Controller")
        network_canvas.create_text(width-margin-rectwidth/2, margin*2, anchor="n", text="Device")

    # Redraw boat canvas
    def redraw_boat_canvas(boat_history):
        map_history = []
        boat_canvas.delete("all")
        height = float(boat_canvas.winfo_height() - net_size)
        width = float(boat_canvas.winfo_width())
        
        # Get current boat position and create canvas offset
        x = boat_history[len(boat_history)-1][0] + width/2
        y = height/2 - boat_history[len(boat_history)-1][1]
        x_margin = width/2
        y_margin = height/2
        y_offset = 0
        x_offset = 0
        if x > width - x_margin:
            x_offset = width - x_margin - x
        elif x < 0 + x_margin:
            x_offset = 0 + x_margin - x
        if y > height - y_margin:
            y_offset = height - y_margin - y
        elif y < 0 + y_margin:
            y_offset = 0 + y_margin - y
        for point in boat_history:
            x = point[0] + width/2 + x_offset
            y = height/2 - point[1] + y_offset
            map_history.append(float(x))
            map_history.append(float(y))
        # length = math.sqrt((x1-x0)^2 + (y1-y0)^2)
        boat_canvas.create_rectangle(0, 0, boat_canvas.winfo_width(), boat_canvas.winfo_height(), fill="#003459")
        if len(map_history) >= 4:
            boat_canvas.create_line(map_history, fill="white", width=4)
            boat_vertices = [
                            [-2, 1],
                            [-2, -1],
                            [1, -1],
                            [3, 0],
                            [1, 1]
                            ]
            
            last = len(map_history) - 1
            new_vertices = []
            scale = 7
            angle = math.atan2((map_history[last] - map_history[last-2]),(map_history[last-1] - map_history[last-3]))
            for vertice in boat_vertices:
                x = vertice[0]*scale
                y = vertice[1]*scale
                vertice[0] = x*math.cos(angle) - y*math.sin(angle)
                vertice[1] = x*math.sin(angle) + y*math.cos(angle)
                vertice[0] = vertice[0] + map_history[last-1]
                vertice[1] = vertice[1] + map_history[last]
                new_vertices.append(float(vertice[0]))
                new_vertices.append(float(vertice[1]))
            boat_canvas.create_polygon(new_vertices, fill="dark gray", outline="black")
        # canvas.create_line(float(x0), float(y0), float(x1), float(y1), fill="red",capstyle="round", width="2")

    # Model canvases
    network_canvas = tk.Canvas(model_container)
    boat_canvas = tk.Canvas(model_container)
    def resize_model(event):
        boat_canvas.place(anchor="n", width=event.width-10, height=event.height-net_size-7, x=event.width/2, y=7)
        network_canvas.place(anchor="s", width=event.width-10, height=net_size-10, x=event.width/2, y=event.height-5)
    # Bind resize event to the container
    model_container.bind("<Configure>", resize_model)

    def hacker_pane(right_pane, decipher_button):
        decipher_button.config(state="disabled")
        global simplify_data
        simplify_data = True

        instructions = tk.Label(
        right_pane,
        text="You can now inject packets into the device!\n"
            "Command its propellor speed and rudder angle below\n"
            "Leave an input blank to leave it unchanged\n"
            "The submarine will follow your command until\n"
            "a new one arrives from the controller.",
        wraplength=right_pane.winfo_width()-20,
        justify="left"
        )
        instructions.pack(padx=5, pady=7, anchor="n", fill="x")

        # Panel for label/input pairs
        panel = tk.Frame(right_pane)
        panel.pack(padx=5, pady=7, fill="x")

        # First label/input
        tk.Label(panel, text="Speed").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        speed_input = tk.Entry(panel)
        speed_input.grid(row=0, column=1, sticky="ew", padx=5, pady=5)

        # Second label/input
        tk.Label(panel, text="Rudder").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        rudder_input = tk.Entry(panel)
        rudder_input.grid(row=1, column=1, sticky="ew", padx=5, pady=5)

        # Make the second column expand to fill panel width
        panel.columnconfigure(1, weight=1)

        # Status label
        hack_status = tk.Label(panel)
        hack_status.grid(row=2, column=0, sticky="w", padx=5, pady=5)
        hack_status.config(text="Injection Status: Idle")
        # Send button
        send_button = tk.Button(panel, text="Send", command=lambda: inject_button(speed_input, rudder_input, hack_status, panel, False, auto_button, send_button))
        auto_button = tk.Button(panel, text="Auto-send (DDoS)", command=lambda:inject_button(speed_input, rudder_input, hack_status, panel, True, auto_button, send_button))
        send_button.grid(row=2, column=1, sticky="e", padx=5, pady=5)
        global hack_count
        hack_count = 0

    def inject_button(speed, rudder, status, panel, replay, auto_button, send_button):
        global hack_count
        if replay == True:
            auto_button.config(state="disabled")
            send_button.config(state="disabled")
            auto_button.after(500, lambda:inject_button(speed, rudder, status, panel, True, auto_button, send_button))
            
        valid_speed = 0
        valid_rudder = 0
        send = False
        global boat
        try:
            valid_speed = float(speed.get())
            valid_rudder = float(rudder.get())*math.pi/180
            send = True
        except:
            status.config(text="Failed: Please input numbers.")
            return
        if send == True:
            status.config(text="Success!")
            boat.receive_queue.put_nowait([valid_speed, valid_rudder])
            hack_count += 1
            if hack_count == 10:
                auto_button.grid(row=3, column=1, sticky="e", padx=5, pady=5)
                control_frame = tk.Frame(panel)
                control_frame.grid(row=4, column=0, columnspan=2, sticky="ew", padx=5, pady=5)
                faster = tk.Button(control_frame, text="Faster", command=lambda: edit_value(speed, 10))
                slower = tk.Button(control_frame, text="slower", command=lambda: edit_value(speed, -10))
                lefter = tk.Button(control_frame, text="lefter", command=lambda: edit_value(rudder, 5))
                righter = tk.Button(control_frame, text="righter", command=lambda: edit_value(rudder, -5))

                faster.grid(row=0, column=0, sticky="w", padx=2, pady=5)
                slower.grid(row=0, column=1, sticky="w", padx=2, pady=5)
                lefter.grid(row=0, column=2, sticky="w", padx=2, pady=5)
                righter.grid(row=0, column=3, sticky="w", padx=2, pady=5)

        def edit_value(box, change):
            og = float(box.get())
            box.delete(0, tk.END)
            box.insert(0, str(og + change))