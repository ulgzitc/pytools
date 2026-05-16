import sys
import argparse
from PIL import Image
from PIL.ExifTags import TAGS


parser = argparse.ArgumentParser(
    description="You can use this tool to inspect or remove metadata from images. Supports: .jpg .png - haven't tested with other formats."
)

parser.add_argument("img", help="Image file")
parser.add_argument("-s", "--show", action="store_true",
                    help="Show image metadata.")
parser.add_argument("-r", "--remove", action="store_true",
                    help="Remove image metadata")

args = parser.parse_args()


def extract(image):
    exifdata = image.getexif()
    if len(exifdata) == 0:
        print("There's no metadata in this image.")
        sys.exit()
    for tagid in exifdata:
        tagname = TAGS.get(tagid, tagid)
        value = exifdata.get(tagid)
        print(f"{tagname:25}: {value}")


def clear_all_metadata(image):
    exifdata = image.getexif()
    if len(exifdata) == 0:
        print("There's no metadata in this image.")
        sys.exit()
    data = list(image.get_flattened_data())
    img_without_metadata = Image.new(image.mode, image.size)
    img_without_metadata.putdata(data)
    img_without_metadata.save(args.img)
    print(f"Metadata successfully cleared from '{args.img}'.")


image = Image.open(args.img)
if args.show:
    extract(image)
if args.remove:
    clear_all_metadata(image)

if args.img and not (args.show or args.remove):
    image = Image.open(args.img)
    extract(image)
    a = input("Do you want to remove its metadata? <yes/no>")
    if not (a.endswith("o") or a.endswith("N") or a.endswith("n")):
        clear_all_metadata(image)
