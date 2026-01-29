

# def clear(parent):
#     while len(parent.winfo_children()) > 0:
#         parent.winfo_children()[0].destroy()

# def clear_window(root):
#     clear(root)



# def draw_map(parent, buffer):
#     canvas.delete("all")
#     draw.ocean(canvas, "#003459")
#     if len(net.fake_pos_history) < 5 or len(net.real_pos_history) < 5:
#         print(net.real_pos_history)
#         return
#     draw.line(canvas, net.fake_pos_history, "pink")
#     x = net.fake_pos_history[-2]
#     y = net.fake_pos_history[-1]
#     dir = net.current_fake_direction
#     draw.boat(canvas, x, y, dir, "pink", "")
#     draw.line(canvas, net.real_pos_history, "white")
#     x = net.real_pos_history[-2]
#     y = net.real_pos_history[-1]
#     dir = net.current_real_direction
#     draw.boat(canvas, x, y, dir, "black", "white")
#     draw.target(canvas, net.target[0], net.target[1], "red")
#     draw.ticks(canvas, [x, y, net.target[0], net.target[1]], 10, 10, "green")
#     draw.ticks(canvas, net.real_pos_history, 10, 10, "black")
#     draw.ticks(canvas, [0, 0, 0, 1000], 100, 20, "white")
#     draw.ticks(canvas, [0, 0, 1000, 0], 100, 20, "white")
#     return