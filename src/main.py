import random 
from datetime import datetime
from uuid import uuid4

from formats.find_difference import generate_find_difference_video

VIDEOS_TO_GENERATE = 10

def generate_random_config(video_number):
    hooks = [
        "Encuentra el numero diferente antes de que acabe el tiempo",
        "Solo los mas atentos encuentran el numero distinto",
        "Tienes pocos segundos para encontrar el intruso",
        "El numero diferente esta escondido a simple vista",
        "Si lo ves rapido tienes muy buena vista",
    ]

    grid_sizes = [
        (8, 6),
        (9, 6),
        (10, 6),
        (9, 7),
    ]

    color_palettes = [
        {
            "background_color": (10, 12, 28),
            "text_color": (255, 255, 255),
            "accent_color": (255, 196, 0),
        },
        {
            "background_color": (0, 0, 0),
            "text_color": (245, 245, 245),
            "accent_color": (0, 220, 180),
        },
        {
            "background_color": (255,0 , 0),
            "text_color": (255, 248, 240),
            "accent_color": (255, 90, 120),
        },
    ]

    base_number, odd_number = random.sample(
        ["1", "2", "3", "4", "5", "6", "7", "8", "9"],
        2,
    )

    rows, cols = random.choice(grid_sizes)
    answer_index = random.randrange(rows * cols)
    palette = random.choice(color_palettes)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    unique_id = uuid4().hex[:8]

    return {
        "width": 1080,
        "height": 1920,
        "hook_text": random.choice(hooks),
        "base_number": base_number,
        "odd_number": odd_number,
        "rows": rows,
        "cols": cols,
        "answer_index": answer_index,
        "background_color": palette["background_color"],
        "text_color": palette["text_color"],
        "accent_color": palette["accent_color"],
        "output_path": f"output/images/find_difference_{video_number:02d}_{timestamp}_{unique_id}.png",
        "video_output_path": f"output/videos/find_difference_{video_number:02d}_{timestamp}_{unique_id}.mp4",
    }

def main():
    generated_videos = []

    for video_number in range(1, VIDEOS_TO_GENERATE + 1):
        print(f"Generando video {video_number}/{VIDEOS_TO_GENERATE}")

        config = generate_random_config(video_number)
        generate_find_difference_video(config)

        generated_videos.append(config["video_output_path"])

    print("\nLote completado")
    print(f"Videos generados: {len(generated_videos)}")

    for video_path in generated_videos:
        print(f"- {video_path}")


if __name__ == "__main__":
    main()