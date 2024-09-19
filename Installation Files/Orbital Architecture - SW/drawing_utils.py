#drawing_utils.py

import pyglet
from pyglet.gl import *
import datetime

(line_thickness_square, line_thickness_rectangle, square_line_thickness,
 rectangle_highlight_line_thickness, rectangle_highlight_offset, intro_font_size,
 instructions_font_size, start_font_size, assessment_end_font_size,
 complete_end_font_size, sl_slider_height, sl_total_width, sl_line_width,
 sl_knob_radius, sl_whisker_length, sl_increment_length, sl_label_font_size,
 sl_prompt_font_size, sl_min_max_label_font_size, sl_mid_line_width,
 sl_label_offset_x, sl_label_offset_y, sl_prompt_offset_x, sl_prompt_offset_y,
 sl_min_label_offset_x, sl_min_label_offset_y, sl_max_label_offset_x,
 sl_max_label_offset_y, sl_promt_width, sl_line_height, sl_offset_x) = [None] * 31


stimuli_to_grid = {
    1: (0, 2),  # Top left
    2: (1, 2),  # Top center
    3: (2, 2),  # Top right
    4: (0, 1),  # Middle left
    5: (2, 1),  # Middle right
    6: (0, 0),  # Bottom left
    7: (1, 0),  # Bottom center
    8: (2, 0)   # Bottom right
}

# Functions for Printing to Console
def debug_print(message):
    print(f"\033[91m[DEBUG]\033[0m\033[94m[{datetime.datetime.now()}]: \033[0m[{message}]")

def feedback_print(message):
    print(f"\033[95m[FEEDB]\033[0m\033[94m[{datetime.datetime.now()}]: \033[0m[{message}]")

# Drawing Functions

def draw_rectangle(x, y, width, height, line_thickness, offset, color):
    x = int(x - (line_thickness / 2) - offset)
    y = int(y - (line_thickness / 2) - offset)
    width = int(width + line_thickness + (offset*2))
    height = int(height + line_thickness + (offset*2))

    pyglet.gl.glColor4f(*color)
    pyglet.gl.glLineWidth(line_thickness)
    pyglet.graphics.draw(4, pyglet.gl.GL_LINE_LOOP, ('v2i', [
        x, y,
        x + width, y,
        x + width, y + height,
        x, y + height
    ]))
    pyglet.gl.glColor4f(1., 1., 1., 1.) # Reset color to white

def create_grid(height, width, grid_ratio):

    square_size = (height * grid_ratio) / 3
    total_grid_size = square_size * 3

    grid_start_x = (width - total_grid_size) / 2
    grid_start_y = (height - total_grid_size) / 2

    squares = [[(grid_start_x + x * square_size,
                 grid_start_y + y * square_size,
                 square_size, square_size)
                for x in range(3)] for y in range(3)]

    return squares

def draw_square(x, y, width, height):
    pyglet.graphics.draw(4, pyglet.gl.GL_LINE_LOOP, ('v2i', [
        int(x), int(y),
        int(x + width), int(y),
        int(x + width), int(y + height),
        int(x), int(y + height)
    ]))

def draw_grid(squares):
    for row in squares:
        for square in row:
            draw_square(*square)

def draw_filled_square(position,squares, color, ratio):
    # Calculate square size and offset to center the filled square within the grid cell
    square_size = squares[0][0][2] * ratio
    offset = (squares[0][0][2] - square_size) / 2

    # Get grid cell index from our mapping
    grid_x, grid_y = stimuli_to_grid[position]

    # Calculate filled square position
    square_x = squares[grid_y][grid_x][0] + offset
    square_y = squares[grid_y][grid_x][1] + offset

    # Create and draw the filled square
    filled_square = pyglet.shapes.Rectangle(square_x, square_y, square_size, square_size, color=color)
    filled_square.draw()

def draw_visual(av_stimuli, squares, width, height, ratio, color):
    square_size = squares[0][0][2] * ratio
    font_size = int(square_size)
    stimuli_label = pyglet.text.Label('',
                                      font_size=font_size,
                                      bold=True,
                                      x=width // 2,
                                      y=(height // 2) + 2,
                                      anchor_x='center',
                                      anchor_y='center',
                                      color=color)

    stimuli_label.text = str(av_stimuli)
    stimuli_label.draw()

def play_sound(stimuli, files):
    sound = pyglet.media.load(files[stimuli], streaming=False)
    sound.play()

def draw_cross(width, height, length_ratio, width_ratio, color):
    # Calculate the center of the window
    center_x = width // 2
    center_y = height // 2

    # Calculate the length of the cross arms
    arm_length = height * length_ratio
    line_width = height * width_ratio

    # Set the line color to cross_color
    pyglet.gl.glColor3f(*color)
    pyglet.gl.glLineWidth(line_width)

    pyglet.gl.glBegin(pyglet.gl.GL_LINES)
    # Draw horizontal arm
    pyglet.gl.glVertex2f(center_x - arm_length, center_y)
    pyglet.gl.glVertex2f(center_x + arm_length, center_y)

    # Draw vertical arm
    pyglet.gl.glVertex2f(center_x, center_y - arm_length)
    pyglet.gl.glVertex2f(center_x, center_y + arm_length)
    pyglet.gl.glEnd()

def draw_dot(width, height, dot, ratio, color):
    if dot is None:
        radius = height * ratio
        dot = pyglet.shapes.Circle(width // 2, height // 2, radius, color=color)
    dot.draw()

def draw_rt_feedback(elapsed_time, toggle, label):
    if toggle:
        label.text = f"{elapsed_time} ms"
        label.draw()
        feedback_print(f"Response provided {elapsed_time} ms after stimuli")

def draw_nb_instruction(label, debug):
    label.text = "[Indicate if there is a match using the buttons]"
    label.draw()


def draw_nback_sq_feedback(correct, label, feedback):
    if correct:
        label.text = "[CORRECT]"
        label.color = (0, 255, 0, 255)  # Green
    else:
        label.text = "[INCORRECT]"
        label.color = (255, 0, 0, 255)  # Red
    if feedback:
        label.draw()


def draw_nback_av_feedback(correct, label,  feedback):
    if correct:
        label.text = "[CORRECT]"
        label.color = (0, 255, 0, 255)  # Green
    else:
        label.text = "[INCORRECT]"
        label.color = (255, 0, 0, 255)  # Red
    if feedback:
        label.draw()


def draw_early_flag(label, feedback, debug):
    label.text = '[Too Early. Please wait for Stimuli.]'
    if feedback:
        label.draw()
    if debug:
        feedback_print('Too Early. Subject provided feedback before stimuli.')