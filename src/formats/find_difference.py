from PIL import Image, ImageDraw, ImageFont


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


def generate_find_difference_image(config):
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
    output_path = config["output_path"]

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

    image.save(output_path)

    print(f"Imagen generada en: {output_path}")