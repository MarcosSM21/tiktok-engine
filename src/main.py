from formats.find_difference import generate_find_difference_image

def main():
    config = {
        "width": 1080,
        "height": 1920,
        "hook_text": "Encuentra el numero diferente antes de 7 segundos",
        "base_number": "8",
        "odd_number": "3",
        "rows": 9,
        "cols": 6,
        "answer_index": 22,
        "background_color": (10,12,28),
        "text_color": (245,245,245),
        "accent_color": (255,196,0),
        "output_path": "output/images/find_diference_002.png"
    }


    generate_find_difference_image(config)


if __name__ == "__main__":
    main()