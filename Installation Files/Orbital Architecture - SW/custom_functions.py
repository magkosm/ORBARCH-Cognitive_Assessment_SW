# custom_functions.py
import configparser
import ast
import math
from drawing_utils import feedback_print, debug_print
from pyglet.gl import *
import pyglet

def set_globals_from_config(config_dict, target_globals):
    for key, value in config_dict.items():
        target_globals[key] = value
        globals()[key] = value

def read_config(file_path):
    config = configparser.ConfigParser()
    config.read(file_path)
    result = {}

    for section in config.sections():
        for key in config[section]:
            value = config[section][key]
            # Parsing the types based on the section
            if "Boolean" in section:
                result[key] = config.getboolean(section, key)
            elif "Integer" in section:
                result[key] = config.getint(section, key)
            elif "Float" in section:
                result[key] = config.getfloat(section, key)
            elif ("RGBA" in section) or ("RGB" in section) or ("3f" in section):
                result[key] = ast.literal_eval(value)  # Parse tuple
            elif "AudioFiles" in section:
                result[key] = ast.literal_eval(value)  # Parse dictionary
            elif "List" in section:
                result[key] = ast.literal_eval(value)  # Parse list
            else:
                result[key] = value  # String as default

    return result

def scale_global_variables(scale_factor):
    print("Running Scaler")
    # Define the list of global variables to scale
    variable_list = ["line_thickness_square", "line_thickness_rectangle",
                     "square_line_thickness", "rectangle_highlight_line_thickness",
                     "rectangle_highlight_offset", "intro_font_size",
                     "instructions_font_size", "start_font_size",
                     "assessment_end_font_size", "complete_end_font_size",
                     "sl_slider_height", "sl_total_width", "sl_line_width",
                     "sl_knob_radius", "sl_whisker_length","sl_increment_length",
                     "sl_label_font_size", "sl_prompt_font_size",
                     "sl_min_max_label_font_size", "sl_mid_line_width",
                     "sl_label_offset_x", "sl_label_offset_y", "sl_prompt_offset_x",
                     "sl_prompt_offset_y", "sl_min_label_offset_x",
                     "sl_min_label_offset_y", "sl_max_label_offset_x",
                     "sl_max_label_offset_y", "sl_promt_width",
                     "sl_line_height", "sl_offset_x"]

    # Scale each global variable by the scale factor
    for var in variable_list:
        if var in globals():
            globals()[var] *= scale_factor


# Questionaire generation
class Slider:
    def __init__(self, x, y, width, min_val=0, max_val=100, increments=21, default_pos=.5, label='Test Label',
                 prompt='Test Prompt', min_label="min", max_label="max"):
        self.x = x
        self.y = y
        self.width = width
        self.min_val = min_val
        self.max_val = max_val
        self.min_label = min_label
        self.max_label = max_label
        # Use global variables for custom attributes
        self.knob_radius = sl_knob_radius

        self.dragging = False
        self.label = label
        self.prompt = prompt
        self.increments = increments

        # Default position of the knob
        if default_pos is None:
            self.knob_pos = self.x
        else:
            self.knob_pos = self.x + default_pos * self.width

    def draw(self):

        # Set line width
        glLineWidth(sl_line_width)
        glColor3f(*[c / 255. for c in sl_line_color])

        # Draw the line representing the track of the slider
        pyglet.graphics.draw(2, GL_LINES, ('v2f', [self.x, self.y, self.x + self.width, self.y]))

        # Reset line width (if needed)
        glLineWidth(1)

        # Draw whiskers at the ends
        glColor3f(*[c / 255. for c in sl_line_color])
        whisker_length = sl_whisker_length
        # Draw whiskers at the ends (adjusting the y-coordinates)
        pyglet.graphics.draw(2, pyglet.gl.GL_LINES, ('v2f', [self.x, self.y, self.x, self.y + whisker_length]))
        pyglet.graphics.draw(2, pyglet.gl.GL_LINES,
                             ('v2f', [self.x + self.width, self.y, self.x + self.width, self.y + whisker_length]))

        # Draw the prominent mid line
        glColor3f(*[c / 255. for c in sl_mid_line_color])
        glLineWidth(sl_mid_line_width)
        mid_x = self.x + self.width / 2
        pyglet.graphics.draw(2, GL_LINES,
                             ('v2f', [mid_x, self.y, mid_x, self.y + sl_whisker_length]))

        glLineWidth(1)
        # Draw increments
        glColor3f(*[c / 255. for c in sl_increment_color])
        increment_distance = self.width / self.increments
        for i in range(self.increments + 1):
            xpos = self.x + i * increment_distance
            pyglet.graphics.draw(2, GL_LINES,
                                 ('v2f', [xpos, self.y, xpos, self.y + sl_increment_length]))

        # Draw the knob as a circle
        glColor3f(*[c / 255. for c in sl_knob_color])
        num_segments = 100
        angle = 2 * 3.1415926 / num_segments
        cosine = math.cos(angle)
        sine = math.sin(angle)
        cx = self.knob_radius
        cy = 0
        vertices = []
        for i in range(num_segments):
            vertices.append(cx + self.knob_pos)
            vertices.append(cy + self.y)
            next_cx = cosine * cx - sine * cy
            cy = sine * cx + cosine * cy
            cx = next_cx
        pyglet.graphics.draw(len(vertices) // 2, pyglet.gl.GL_TRIANGLE_FAN, ('v2f', vertices))

        if provide_feedback:
            # Calculate slider value
            slider_value = self.get_value()

            value_label = pyglet.text.Label(str(round(slider_value, 2)),
                                            font_name='Arial',
                                            font_size=sl_prompt_font_size,
                                            x=self.x + self.width + sl_total_width/4,
                                            # Adjust this to place the label where you want it
                                            y=self.y,
                                            anchor_x='left',
                                            anchor_y='center',
                                            color=sl_prompt_color + (255,))
            value_label.draw()

        # Labels with offsets
        label = pyglet.text.Label(self.label, font_name='Arial', font_size=sl_label_font_size,
                                  x=self.x + sl_label_offset_x, y=self.y + sl_label_offset_y, anchor_x='left',
                                  anchor_y='center', color=sl_label_color + (255,))
        label.draw()

        # Labels with offsets
        prompt = pyglet.text.Label(self.prompt, font_name='Arial',
                                   font_size=sl_prompt_font_size,
                                   width=sl_promt_width, multiline=True,  # use defined constant here
                                   x=self.x + self.width + sl_prompt_offset_x,
                                   y=self.y + sl_prompt_offset_y + sl_line_height * (self.prompt.count('\n') + 1),
                                   anchor_x='right', anchor_y='center',
                                   align='right',
                                   color=sl_prompt_color + (255,))
        prompt.draw()

        min_label = pyglet.text.Label(str(self.min_label), font_name='Arial', font_size=sl_min_max_label_font_size,
                                      x=self.x + sl_min_label_offset_x, y=self.y + sl_min_label_offset_y,
                                      anchor_x='left', anchor_y='center', color=sl_min_max_label_color + (255,))
        min_label.draw()

        max_label = pyglet.text.Label(str(self.max_label), font_name='Arial', font_size=sl_min_max_label_font_size,
                                      x=self.x + self.width + sl_max_label_offset_x, y=self.y + sl_max_label_offset_y,
                                      anchor_x='right', anchor_y='center', color=sl_min_max_label_color + (255,))
        max_label.draw()

        glColor3f(1., 1., 1.)

    def update_knob_pos(self, x):
        # Update knob position according to mouse x position
        self.knob_pos = max(min(x, self.x + self.width), self.x)

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        if self.dragging and self.y - self.knob_radius <= y <= self.y + self.knob_radius:
            self.update_knob_pos(x)

    def on_mouse_press(self, x, y, button, modifiers):
        # Check if the mouse click is within the slider's y range
        if self.y - self.knob_radius -5 <= y <= self.y + self.knob_radius +5:
            self.update_knob_pos(x)
            self.dragging = True  # Keep this line if you still want to drag after clicking.

    def on_mouse_release(self, x, y, button, modifiers):
        # Stop dragging if mouse is released
        self.dragging = False

    def get_value(self):
        # Calculate and return the current value of slider
        return self.min_val + (self.knob_pos - self.x) / self.width * (self.max_val - self.min_val)

def generate_nasa_tlx_sliders(window):
    # Slider descriptions for NASA-TLX
    slider_descriptions = [
        ("Mental Demand", "How mentally demanding were the tasks?", "Very Low", "Very High"),
        ("Physical Demand", "How physically demanding were the tasks?", "Very Low", "Very High"),
        ("Temporal Demand", "How hurried or rushed was the pace of all the tasks?", "Very Low", "Very High"),
        ("Own Performance", "How successful were you in accomplishing all the tasks?", "Perfect", "Failure"),
        ("Effort", "How hard did you have to work to accomplish your level of performance?", "Very Low", "Very High"),
        ("Frustration Level", "How insecure, discouraged, irritated, stressed and annoyed were you?", "Very Low",
         "Very High")
    ]

    num_sliders = len(slider_descriptions)
    total_height = num_sliders * sl_slider_height

    # Calculate starting y-coordinate to center the sliders on the screen
    start_y = (window.height - total_height) / 2 + (num_sliders - 1) * sl_slider_height

    sliders = []

    for i, (label, prompt, min_label, max_label) in enumerate(slider_descriptions):
        slider = Slider(window.width / 2 - (sl_total_width/2), start_y - i * sl_slider_height, sl_total_width, label=label, prompt=prompt,
                        min_label=min_label, max_label=max_label)
        sliders.append(slider)

    for slider in sliders:
        window.push_handlers(slider)  # Register each slider as an event handler

    return sliders

def generate_pss_sliders(window):
    # Slider Desceptions
    slider_descriptions = [
        ("Perceived Stress", "How stressed do you feel?", "Not stressed at all", "As stressed as can be"),
        ("Perceived Tiredness", "How tired do you feel?", "Not tired at all", "Exhausted ")
    ]
    num_sliders = len(slider_descriptions)
    total_height = num_sliders * sl_slider_height

    # Calculate starting y-coordinate to center the sliders on the screen
    start_y = (window.height - total_height) / 2 + (num_sliders - 1) * sl_slider_height

    sliders = []

    for i, (label, prompt, min_label, max_label) in enumerate(slider_descriptions):
        slider = Slider(window.width / 2 - (sl_total_width/2), start_y - i * sl_slider_height, sl_total_width, label=label, prompt=prompt,
                        min_label=min_label, max_label=max_label)
        sliders.append(slider)

    for slider in sliders:
        window.push_handlers(slider)  # Register each slider as an event handler

    return sliders





