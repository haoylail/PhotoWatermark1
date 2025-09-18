import os
import argparse
import piexif
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import shutil

def validate_path(input_path):
    if not os.path.exists(input_path):
        raise argparse.ArgumentTypeError(f"The path {input_path} does not exist.")
    return input_path

def extract_exif_date(image_path):
    try:
        exif_dict = piexif.load(image_path)
        date_taken = exif_dict["Exif"].get(piexif.ExifIFD.DateTimeOriginal, None)
        if date_taken:
            return date_taken.decode("utf-8").split(" ")[0]  # Return only the date part
        else:
            print(f"No DateTimeOriginal found in EXIF data for {image_path}. Using current date as fallback.")
            return datetime.now().strftime("%Y-%m-%d")  # Fallback to current date
    except Exception as e:
        print(f"Error reading EXIF data from {image_path}: {e}. Using current date as fallback.")
        return datetime.now().strftime("%Y-%m-%d")  # Fallback to current date

def render_watermark(image_path, text, font_size, font_color, position):
    try:
        with Image.open(image_path) as img:
            draw = ImageDraw.Draw(img)
            font = ImageFont.truetype("arial.ttf", font_size)

            # Calculate position using textbbox
            text_bbox = draw.textbbox((0, 0), text, font=font)
            text_width, text_height = text_bbox[2] - text_bbox[0], text_bbox[3] - text_bbox[1]

            if position == "top-left":
                x, y = 10, 10
            elif position == "center":
                x = (img.width - text_width) // 2
                y = (img.height - text_height) // 2
            elif position == "bottom-right":
                x = img.width - text_width - 10
                y = img.height - text_height - 10

            # Add text to image
            draw.text((x, y), text, fill=font_color, font=font)

            return img
    except Exception as e:
        print(f"Error rendering watermark on {image_path}: {e}")
        return None

def save_watermarked_image(image, original_path, output_dir):
    try:
        # Create output directory if it doesn't exist
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Generate output file path
        base_name = os.path.basename(original_path)
        output_path = os.path.join(output_dir, base_name)

        # Save the image
        image.save(output_path)
        print(f"Saved watermarked image to {output_path}")
    except Exception as e:
        print(f"Error saving watermarked image: {e}")

def parse_watermark_settings(parser):
    parser.add_argument("--font-size", type=int, default=20, help="Font size for the watermark text.")
    parser.add_argument("--font-color", type=str, default="black", help="Font color for the watermark text.")
    parser.add_argument("--position", type=str, choices=["top-left", "center", "bottom-right"], default="bottom-right", help="Position of the watermark on the image.")

    # Parse the new arguments
    args = parser.parse_args()

    # Extract settings
    font_size = args.font_size
    font_color = args.font_color
    position = args.position

    print(f"Watermark settings: Font size={font_size}, Font color={font_color}, Position={position}")
    return font_size, font_color, position

def main():
    parser = argparse.ArgumentParser(description="Add watermarks to images based on EXIF data.")
    parser.add_argument("path", type=validate_path, help="Path to an image file or a directory containing images.")
    font_size, font_color, position = parse_watermark_settings(parser)

    args = parser.parse_args()

    input_path = args.path
    output_directory = input_path + "_watermark"
    if os.path.isfile(input_path):
        print(f"Processing single image: {input_path}")
        date = extract_exif_date(input_path)
        print(f"Date extracted: {date}")
        if date:
            watermarked_image = render_watermark(input_path, date, font_size, font_color, position)
            if watermarked_image:
                watermarked_image.show()  # For testing purposes
                save_watermarked_image(watermarked_image, input_path, output_directory)
    elif os.path.isdir(input_path):
        print(f"Processing all images in directory: {input_path}")
        for filename in os.listdir(input_path):
            file_path = os.path.join(input_path, filename)
            if os.path.isfile(file_path):
                date = extract_exif_date(file_path)
                print(f"Date extracted for {filename}: {date}")
                if date:
                    watermarked_image = render_watermark(file_path, date, font_size, font_color, position)
                    if watermarked_image:
                        watermarked_image.show()  # For testing purposes
                        save_watermarked_image(watermarked_image, file_path, output_directory)

if __name__ == "__main__":
    main()