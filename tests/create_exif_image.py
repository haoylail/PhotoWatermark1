from PIL import Image
from PIL.ExifTags import TAGS
import piexif

# Create a blank image
image = Image.new('RGB', (200, 200), color = 'white')
image.save('tests/test_with_exif.jpg')

# Add EXIF data
exif_dict = {
    "0th": {
        piexif.ImageIFD.Make: b"TestCamera",
        piexif.ImageIFD.Model: b"TestModel",
    },
    "Exif": {
        piexif.ExifIFD.DateTimeOriginal: b"2023:09:18 12:00:00",
    },
    "1st": {},
    "thumbnail": None,
}
exif_bytes = piexif.dump(exif_dict)
piexif.insert(exif_bytes, 'tests/test_with_exif.jpg')

print("Image with EXIF data created at tests/test_with_exif.jpg")