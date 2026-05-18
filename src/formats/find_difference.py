from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

import numpy as np
from moviepy import AudioFileClip, CompositeAudioClip, ImageClip, concatenate_videoclips

def load_font(size):
    try:
        return ImageFont.truetype("DejaVuSans-Bold.ttf", size)
    except OSError:
        return ImageFont.load_default()
    
def clamp_color_value(value):
    return max(0, min(255, value))


def brighten_color(color, amount):
    return tuple(clamp_color_value(channel + amount) for channel in color)

def darken_color(color, amount):
    return tuple(clamp_color_value(channel - amount) for channel in color)


def create_vertical_gradient(width, height, start_color, end_color):
    image = Image.new("RGB", (width, height))

    for y in range(height):
        ratio = y / max(height - 1, 1)

        red = int(start_color[0] * (1 - ratio) + end_color[0] * ratio)
        green = int(start_color[1] * (1 - ratio) + end_color[1] * ratio)
        blue = int(start_color[2] * (1 - ratio) + end_color[2] * ratio)

        ImageDraw.Draw(image).line(
            [(0, y), (width, y)],
            fill=(red, green, blue),
        )

    return image


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


def get_multiline_text_size(draw, lines, font, line_gap):
    if not lines:
        return 0, 0

    widths = []
    heights = []

    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font)
        widths.append(bbox[2] - bbox[0])
        heights.append(bbox[3] - bbox[1])

    total_height = sum(heights) + line_gap * (len(lines) - 1)

    return max(widths), total_height


def draw_centered_multiline_text_in_box(draw, lines, font, fill, box, line_gap):
    text_width, text_height = get_multiline_text_size(draw, lines, font, line_gap)
    box_left, box_top, box_right, box_bottom = box
    box_width = box_right - box_left
    box_height = box_bottom - box_top

    current_y = box_top + ((box_height - text_height) / 2)

    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font)
        line_width = bbox[2] - bbox[0]
        line_height = bbox[3] - bbox[1]
        x = box_left + ((box_width - line_width) / 2) - bbox[0]
        y = current_y - bbox[1]

        draw.text((x, y), line, fill=fill, font=font)
        current_y += line_height + line_gap


def get_layout_bounds(config):
    width = config["width"]
    height = config["height"]

    return {
        "top_margin": 340,
        "bottom_margin": 430,
        "left_margin": 100,
        "right_margin": 100,
        "grid_panel_padding": 28,
        "grid_bottom": height - 430,
        "grid_right": width - 100,
    }


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
    accent_color = config["accent_color"]


    gradient_end_color = brighten_color(background_color, 35)
    image = create_vertical_gradient(width, height, background_color, gradient_end_color)
    draw = ImageDraw.Draw(image)

    hook_font = load_font(54)
    grid_font = load_font(72)

    layout = get_layout_bounds(config)
    top_margin = layout["top_margin"]
    bottom_margin = layout["bottom_margin"]
    left_margin = layout["left_margin"]
    right_margin = layout["right_margin"]
    grid_panel_padding = layout["grid_panel_padding"]
    grid_bottom = layout["grid_bottom"]
    grid_right = layout["grid_right"]

    hook_box = (
        left_margin,
        70,
        width - right_margin,
        230,
    )

    hook_padding = 42
    hook_inner_box = (
        hook_box[0] + hook_padding,
        hook_box[1] + hook_padding,
        hook_box[2] - hook_padding,
        hook_box[3] - hook_padding,
    )
    hook_inner_width = hook_inner_box[2] - hook_inner_box[0]
    hook_lines = wrap_text(draw, hook_text, hook_font, hook_inner_width)
    hook_line_gap = 10

    draw.rounded_rectangle(
        hook_box,
        radius=28,
        fill=(0, 0, 0),
        outline=accent_color,
        width=5,
    )

    draw_centered_multiline_text_in_box(
        draw=draw,
        lines=hook_lines,
        font=hook_font,
        fill=text_color,
        box=hook_inner_box,
        line_gap=hook_line_gap,
    )

    grid_width = width - left_margin - right_margin
    grid_height = grid_bottom - top_margin

    cell_width = grid_width / cols
    cell_height = grid_height / rows

    grid_panel_box = (
        left_margin - grid_panel_padding,
        top_margin - grid_panel_padding,
        grid_right + grid_panel_padding,
        grid_bottom + grid_panel_padding,
    )

    draw.rounded_rectangle(
        grid_panel_box,
        radius=34,
        fill=darken_color(background_color, 20),
        outline=accent_color,
        width=3,
    )

    grid_line_color = brighten_color(background_color, 55)

    for col in range(1, cols):
        x = left_margin + (col * cell_width)
        draw.line(
            [(x, top_margin), (x, grid_bottom)],
            fill=grid_line_color,
            width=2,
        )

    for row in range(1, rows):
        y = top_margin + (row * cell_height)
        draw.line(
            [(left_margin, y), (grid_right, y)],
            fill=grid_line_color,
            width=2,
        )

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
    text_color = config["text_color"]

    countdown_font = load_font(92)
    center_x = width // 2
    center_y = height - 255
    radius = 82

    box = (
        340,
        center_y - 112,
        width - 340,
        center_y + 112,
    )

    draw.rounded_rectangle(
        box,
        radius=36,
        fill=darken_color(background_color, 25),
        outline=accent_color,
        width=4,
    )

    draw.ellipse(
        (
            center_x - radius,
            center_y - radius,
            center_x + radius,
            center_y + radius,
        ),
        fill=accent_color,
    )

    draw.ellipse(
        (
            center_x - radius + 10,
            center_y - radius + 10,
            center_x + radius - 10,
            center_y + radius - 10,
        ),
        outline=text_color,
        width=4,
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
    rows = config["rows"]
    cols = config["cols"]

    layout = get_layout_bounds(config)
    top_margin = layout["top_margin"]
    left_margin = layout["left_margin"]
    grid_right = layout["grid_right"]
    grid_bottom = layout["grid_bottom"]

    grid_width = grid_right - left_margin
    grid_height = grid_bottom - top_margin

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
    background_color = config["background_color"]

    x, y, cell_width, cell_height = get_grid_position(config, answer_index)

    radius = min(cell_width, cell_height) * 0.46

    glow_radius = radius + 18
    draw.ellipse(
        (
            x - glow_radius,
            y - glow_radius,
            x + glow_radius,
            y + glow_radius,
        ),
        outline=accent_color,
        width=8,
    )

    inner_radius = radius + 5
    draw.ellipse(
        (
            x - inner_radius,
            y - inner_radius,
            x + inner_radius,
            y + inner_radius,
        ),
        outline=text_color,
        width=6,
    )

    draw.ellipse(
        (
            x - radius,
            y - radius,
            x + radius,
            y + radius,
        ),
        outline=accent_color,
        width=14,
    )

    final_font = load_font(58)
    final_text = "Lo viste a tiempo?"

    final_box = (
        140,
        height - 220,
        width - 140,
        height - 70,
    )

    draw.rounded_rectangle(
        final_box,
        radius=34,
        fill=darken_color(background_color, 25),
        outline=accent_color,
        width=4,
    )

    draw.text(
        (width // 2, height - 145),
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

def build_audio_track(video, config):
    audio_clips = []

    music_path = config.get("background_music_path")
    if music_path:
        music_file = Path(music_path)

        if music_file.exists():
            music_volume = config.get("background_music_volume", 0.25)
            music_start = config.get("background_music_start", 0)
            music_end = music_start + video.duration

            music = AudioFileClip(str(music_file))

            if music_end > music.duration:
                music_start = 0
                music_end = video.duration

            music = music.subclipped(music_start, music_end)
            music = music.with_volume_scaled(music_volume)
            audio_clips.append(music)
        else:
            print(f"Musica no encontrada, se omite: {music_path}")

    voiceover_path = config.get("voiceover_path")
    if voiceover_path:
        voiceover_file = Path(voiceover_path)

        if voiceover_file.exists():
            voiceover_volume = config.get("voiceover_volume", 1.0)

            voiceover = AudioFileClip(str(voiceover_file))
            voiceover = voiceover.subclipped(0, min(voiceover.duration, video.duration))
            voiceover = voiceover.with_volume_scaled(voiceover_volume)
            audio_clips.append(voiceover)
        else:
            print(f"Voz no encontrada, se omite: {voiceover_path}")

    if not audio_clips:
        return video

    return video.with_audio(CompositeAudioClip(audio_clips))

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
    video = build_audio_track(video, config)
    video.write_videofile(
        output_path,
        fps=24,
        codec="libx264",
        audio_codec="aac",
    )

    print(f"Video generado en: {output_path}")
