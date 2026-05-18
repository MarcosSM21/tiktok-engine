import json
import random
from datetime import datetime
from pathlib import Path
from uuid import uuid4

from formats.find_difference import generate_find_difference_video

PRESET_PATH = Path("data/presets/find_difference.json")

def load_presets():
    with PRESET_PATH.open("r", encoding="utf-8") as file:
        return json.load(file)

def generate_random_config(video_number, presets):
    base_number, odd_number = random.sample(presets["numbers"], 2)

    rows, cols = random.choice(presets["grid_sizes"])
    answer_index = random.randrange(rows * cols)

    palette = random.choice(presets["color_palettes"])

    background_color = tuple(palette["background_color"])
    text_color = tuple(palette["text_color"])
    accent_color = tuple(palette["accent_color"])

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    unique_id = uuid4().hex[:8]

    return {
        "width": presets["width"],
        "height": presets["height"],
        "hook_text": presets["hook_text"],
        "base_number": base_number,
        "odd_number": odd_number,
        "rows": rows,
        "cols": cols,
        "answer_index": answer_index,
        "background_color": background_color,
        "text_color": text_color,
        "accent_color": accent_color,
        "output_path": f"output/images/find_difference_{video_number:02d}_{timestamp}_{unique_id}.png",
        "video_output_path": f"output/videos/find_difference_{video_number:02d}_{timestamp}_{unique_id}.mp4",
        "background_music_path": presets.get("background_music_path"),
        "background_music_volume": presets.get("background_music_volume", 0.25),
        "background_music_start": presets.get("background_music_start", 0),
    }

def main():
    presets = load_presets()
    videos_to_generate = presets["videos_to_generate"]
    generated_videos = []

    for video_number in range(1, videos_to_generate + 1):
        print(f"Generando video {video_number}/{videos_to_generate}")

        config = generate_random_config(video_number, presets)
        generate_find_difference_video(config)

        generated_videos.append(config["video_output_path"])

    print("\nLote completado")
    print(f"Videos generados: {len(generated_videos)}")

    for video_path in generated_videos:
        print(f"- {video_path}")


if __name__ == "__main__":
    main()
