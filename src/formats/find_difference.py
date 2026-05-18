from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

import numpy as np
from moviepy import ImageClip, concatenate_videoclips


def load_font(size):
    try:
        return ImageFont.truetype("DejaVuSans-Bold.ttf", size)
    except OSError:
        return ImageFont.load_default()


def wrap_text(draw, text, font, max_width):
    words = text.split()
    lines = []
    current_line = ""

    for word in words:
        candidate = word if not current_line else f"{current_line} {word}"
        bbox = draw.textbbox((0, 0), candidate, font=font)
        candidate_width = bbox[2] - bbox[0]

        if candidate_width <= max_width:
            current_line = candidate
        else:
            if current_line:
                lines.append(current_line)
            current_line = word

    if current_line:
        lines.append(current_line)

    return lines


def draw_centered_multiline_text(draw, lines, font, fill, center_x, start_y, line_spacing):
    y = start_y

    for line in lines:
        draw.text(
            (center_x, y),
            line,
            fill=fill,
            font=font,
            anchor="ma",
        )
        y += line_spacing


def build_find_difference_image(config):
    width = config["width"]
    height = config["height"]
    background_color = config["background_color"]
    text_color = config["text_color"]
    hook_text = config["hook_text"]
    base_number = config["base_number"]
    odd_number = config["odd_number"]
    rows = config["rows"]
    cols = config["cols"]
    answer_index = config["answer_index"]


    image = Image.new("RGB", (width, height), background_color)
    draw = ImageDraw.Draw(image)

    hook_font = load_font(50)
    grid_font = load_font(90)

    top_margin = 360
    bottom_margin = 180
    left_margin = 100
    right_margin = 100

    hook_max_width = width - left_margin - right_margin
    hook_lines = wrap_text(draw, hook_text, hook_font, hook_max_width)

    draw_centered_multiline_text(
        draw=draw,
        lines=hook_lines,
        font=hook_font,
        fill=text_color,
        center_x=width // 2,
        start_y=100,
        line_spacing=78,
    )

    grid_width = width - left_margin - right_margin
    grid_height = height - top_margin - bottom_margin

    cell_width = grid_width / cols
    cell_height = grid_height / rows

    for row in range(rows):
        for col in range(cols):
            index = row * cols + col
            value = odd_number if index == answer_index else base_number

            x = left_margin + (col * cell_width) + (cell_width / 2)
            y = top_margin + (row * cell_height) + (cell_height / 2)

            draw.text(
                (x, y),
                value,
                fill=text_color,
                font=grid_font,
                anchor="mm",
            )


    return image


def add_countdown_to_image(image, config, seconds_left):
    draw = ImageDraw.Draw(image)

    width = config["width"]
    height = config["height"]
    accent_color = config["accent_color"]
    background_color = config["background_color"]

    countdown_font = load_font(86)

    center_x = width // 2
    center_y = height - 110
    radius = 72

    draw.ellipse(
        (
            center_x - radius,
            center_y - radius,
            center_x + radius,
            center_y + radius,
        ),
        fill=accent_color,
    )

    draw.text(
        (center_x, center_y),
        str(seconds_left),
        fill=background_color,
        font=countdown_font,
        anchor="mm",
    )

    return image


def get_grid_position(config, index):
    width = config["width"]
    height = config["height"]
    rows = config["rows"]
    cols = config["cols"]

    top_margin = 360
    bottom_margin = 180
    left_margin = 100
    right_margin = 100

    grid_width = width - left_margin - right_margin
    grid_height = height - top_margin - bottom_margin

    cell_width = grid_width / cols
    cell_height = grid_height / rows

    row = index // cols
    col = index % cols

    x = left_margin + (col * cell_width) + (cell_width / 2)
    y = top_margin + (row * cell_height) + (cell_height / 2)

    return x, y, cell_width, cell_height


def add_reveal_to_image(image, config):
    draw = ImageDraw.Draw(image)

    width = config["width"]
    height = config["height"]
    answer_index = config["answer_index"]
    accent_color = config["accent_color"]
    text_color = config["text_color"]

    x, y, cell_width, cell_height = get_grid_position(config, answer_index)

    radius = min(cell_width, cell_height) * 0.38

    draw.ellipse(
        (
            x - radius,
            y - radius,
            x + radius,
            y + radius,
        ),
        outline=accent_color,
        width=10,
    )

    final_font = load_font(58)
    final_text = "Lo viste a tiempo?"

    draw.text(
        (width // 2, height - 120),
        final_text,
        fill=text_color,
        font=final_font,
        anchor="mm",
    )

    return image

## GENERACIÓN IMAGENES

def generate_find_difference_image(config):
    image = build_find_difference_image(config)
    output_path = config["output_path"]
    image.save(output_path)
    print(f"Imagen generada en: {output_path}")

def generate_find_difference_countdown_image(config, seconds_left):
    image = build_find_difference_image(config)
    image = add_countdown_to_image(image, config, seconds_left)

    output_path = f"output/images/find_difference_countdown_{seconds_left}.png"
    image.save(output_path)

    print(f"Imagen con cuenta atras generada en: {output_path}")

def generate_find_difference_reveal_image(config):
    image = build_find_difference_image(config)
    image = add_reveal_to_image(image, config)

    output_path = "output/images/find_difference_reveal.png"
    image.save(output_path)

    print(f"Imagen de revelacion generada en: {output_path}")



## VÍDEOS 

def image_to_clip(image, duration):
    return ImageClip(np.array(image)).with_duration(duration)


def generate_find_difference_video(config):
    output_path = config["video_output_path"]
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)

    challenge_image = build_find_difference_image(config)

    countdown_6 = add_countdown_to_image(build_find_difference_image(config), config, 6)
    countdown_5 = add_countdown_to_image(build_find_difference_image(config), config, 5)
    countdown_4 = add_countdown_to_image(build_find_difference_image(config), config, 4)
    countdown_3 = add_countdown_to_image(build_find_difference_image(config), config, 3)
    countdown_2 = add_countdown_to_image(build_find_difference_image(config), config, 2)
    countdown_1 = add_countdown_to_image(build_find_difference_image(config), config, 1)

    reveal_image = add_reveal_to_image(build_find_difference_image(config), config)

    clips = [
        image_to_clip(challenge_image, 2),
        image_to_clip(countdown_6, 1),
        image_to_clip(countdown_5, 1),
        image_to_clip(countdown_4, 1),
        image_to_clip(countdown_3, 1),
        image_to_clip(countdown_2, 1),
        image_to_clip(countdown_1, 1),
        image_to_clip(reveal_image, 3),
    ]

    video = concatenate_videoclips(clips)
    video.write_videofile(
        output_path,
        fps=24,
        codec="libx264",
        audio=False,
    )

    print(f"Video generado en: {output_path}")