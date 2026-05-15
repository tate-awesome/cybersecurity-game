import serial
import re
import pygame
import sys
import math

# --- Configuration ---
SERIAL_PORT = 'COM5'
BAUD_RATE = 115200
GRID_SIZE = 200      
GRAPH_SIZE = 800     # The square area for the grid
LOG_WIDTH = 400      # The sidebar for text
MARGIN = 40
BOTTOM_LABEL_SPACE = 60
WINDOW_WIDTH = GRAPH_SIZE + LOG_WIDTH + (MARGIN * 2)+100
WINDOW_HEIGHT = GRAPH_SIZE + MARGIN + BOTTOM_LABEL_SPACE
SCALE = GRAPH_SIZE / GRID_SIZE

# --- Initialize Pygame ---
pygame.init()
# screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.RESIZABLE | pygame.SCALED)
pygame.display.set_caption("Cyber-ICS Real-Time Monitor")
clock = pygame.time.Clock()
font = pygame.font.SysFont('Consolas', 14)

# --- Serial Setup ---
try:
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=0.1)
except Exception as e:
    print(f"Error opening {SERIAL_PORT}: {e}")
    sys.exit()

# Regex for position
#pos_regex = re.compile(r"x=([\d\.-]+).*?y=([\d\.-]+).*?theta=([\d\.-]+)")
pos_regex = re.compile(r"x=([\d\.-]+)\s+m\s+y=([\d\.-]+)\s+m\s+theta=([\d\.-]+)")

# Global State
pos_history = []
current_pos = (0, 0)
current_theta = 0.0
real_x, real_y = 0.0, 0.0
running = True
serial_log = [] # Stores lines to display in the sidebar

def draw_vessel(surface, pos, angle_rad):
    size = 12
    pts = [(size * 1.5, 0), (-size, -size), (-size, size)]
    rotated_pts = []
    for px, py in pts:
        rx = px * math.cos(-angle_rad) - py * math.sin(-angle_rad)
        ry = px * math.sin(-angle_rad) + py * math.cos(-angle_rad)
        rotated_pts.append((pos[0] + rx, pos[1] + ry))
    pygame.draw.polygon(surface, (255, 50, 50), rotated_pts)
    pygame.draw.polygon(surface, (255, 255, 255), rotated_pts, 2)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: running = False

    # 1. Read Serial Data
    if ser.in_waiting > 0:
        line = ser.readline().decode('utf-8', errors='ignore').strip()
        if line:
            # Add to side log (keep last 40 lines)
            serial_log.append(line)
            if len(serial_log) > 45:
                serial_log.pop(0)

            # Parse for coordinates
            match = pos_regex.search(line)
            if match:
                real_x = float(match.group(1))
                real_y = float(match.group(2))
                current_theta = float(match.group(3))
                
                screen_x = int(real_x * SCALE)
                screen_y = int((real_y * SCALE)) 
                current_pos = (screen_x, screen_y)
                pos_history.append(current_pos)
                if len(pos_history) > 300: pos_history.pop(0)

    # --- Drawing ---
    screen.fill((15, 15, 20)) # Background
    
    # A. Draw Grid Area
    # for i in range(0, 201, 10):  # 0, 10, 20... 200
    #     # Calculate pixel position for the grid lines
    #     pos = int(i * SCALE) + MARGIN
        
    #     # Draw Vertical Lines (X-axis markers)
    #     pygame.draw.line(screen, (35, 35, 45), (pos, MARGIN), (pos, GRAPH_SIZE + MARGIN))
    #     # Draw Horizontal Lines (Y-axis markers)
    #     pygame.draw.line(screen, (35, 35, 45), (MARGIN, pos), (GRAPH_SIZE + MARGIN, pos))
        
    #     # Create Label Text
    #     label = font.render(str(i), True, (100, 100, 120))
        
    #     # X-axis labels (bottom)
    #     screen.blit(label, (pos - 10, GRAPH_SIZE + MARGIN + 5))
    #     # Y-axis labels (left) - Remember to flip Y: 0 is at the bottom (GRAPH_SIZE)
    #     y_label_pos = (GRAPH_SIZE + MARGIN) - pos + (MARGIN - 10)
    #     screen.blit(label, (5, y_label_pos))

    for i in range(0, 201, 10):
        val = int(i * SCALE)
        
        # Vertical Lines
        pygame.draw.line(screen, (35, 35, 45), (val + MARGIN, MARGIN), (val + MARGIN, GRAPH_SIZE + MARGIN))
        # Horizontal Lines
        pygame.draw.line(screen, (35, 35, 45), (MARGIN, val + MARGIN), (GRAPH_SIZE + MARGIN, val + MARGIN))
        
        # Labels
        label = font.render(str(i), True, (100, 100, 120))
        
        # X-axis labels: Positioned in that extra BOTTOM_LABEL_SPACE we created
        screen.blit(label, (val + MARGIN - 10, GRAPH_SIZE + MARGIN + 10))
        
        # Y-axis labels: Flipped so 0 is at the bottom
        y_pos = (GRAPH_SIZE + MARGIN) - val
        screen.blit(label, (5, y_pos - 7))

    # 2. DRAW PATH (Adjusted for Margin)
    if len(pos_history) > 1:
        # We adjust every point in history by the Margin offset
        offset_history = [(p[0] + MARGIN, (GRAPH_SIZE - p[1]) + MARGIN) for p in pos_history]
        pygame.draw.lines(screen, (0, 150, 255), False, offset_history, 2)

    # Apply the MARGIN shift to the vessel position so it stays on the blue line
    vessel_draw_pos = (current_pos[0] + MARGIN, (GRAPH_SIZE - current_pos[1]) + MARGIN)
    draw_vessel(screen, vessel_draw_pos, current_theta)

    # B. Draw Sidebar Separator
    sidebar_x_start = GRAPH_SIZE + (MARGIN * 2)
    pygame.draw.rect(screen, (30, 30, 40), (sidebar_x_start, 0, LOG_WIDTH, WINDOW_HEIGHT))
    pygame.draw.line(screen, (100, 100, 100), (sidebar_x_start, 0), (sidebar_x_start, WINDOW_HEIGHT), 2)

    # C. Render Serial Log to Sidebar
    for idx, log_line in enumerate(serial_log):
        # Determine color based on content (Optional flavor)
        color = (200, 200, 200) # Default Gray
        if "[MASTER]" in log_line: color = (100, 255, 100) # Green for Master
        if "Speed" in log_line: color = (255, 200, 100)    # Orange for Speed lines
        
        text_surf = font.render(log_line, True, color)
        screen.blit(text_surf, (sidebar_x_start + 10, 10 + (idx * 17)))

    # D. Top Overlay
    info_text = font.render(f"LIVE POS: X={real_x:.2f} Y={real_y:.2f} THETA={current_theta:.2f}", True, (255, 255, 255))
    pygame.draw.rect(screen, (0,0,0), (5, 5, 400, 25))
    screen.blit(info_text, (10, 10))

    pygame.display.flip()
    clock.tick(60)

ser.close()
pygame.quit()