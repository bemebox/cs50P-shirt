import sys
import os
from PIL import Image, ImageOps


def main():
    # get the input and output files names from the command-line
    input_file_name, output_file_name = get_files_names()

    # validates if the input and output file have the same extension
    if get_file_extension(input_file_name) != get_file_extension(output_file_name):
        sys.exit("Input and output have different extensions")

    # save the output file image with the shirt image file overlaid in with the input image file
    create_photo(input_file_name, output_file_name)


def get_files_names():
    """
    extracts input and output file names from the command-line arguments.

    Returns:
        input_file_name(str), output_file_name (str)

    Raises:
        SystemExit: If the number of command-line arguments is less than 2 or more than 2.
    """
    args = sys.argv[1:]
    if len(args) < 2:
        sys.exit("Too few command-line arguments")
    elif len(args) > 2:
        sys.exit("Too many command-line arguments")
    else:
        return args[0], args[1]


def get_file_extension(file_name):
    """
    get the file extension from the given file name.

    Args:
        file_name (str): the name of the file.

    Returns:
        str: the file extension or an empty string if not found.
    """
    _, file_extension = os.path.splitext(file_name)
    if file_extension:
        return file_extension.lstrip(".")
    else:
        return ""


def is_valid_file(file_name):
    """
    checks if a given file name is valid based on its extension (".jpg", ".jpeg", or ".png").

    Args:
        file_name (str): the name of the file to be checked.

    Returns:
        bool: True if the file name is valid otherwise False.
    """
    if file_name:
        return file_name.strip().lower().endswith((".jpg", ".jpeg", ".png"))

    return False


def get_image_from_file(file_name, error_message):
    """
    retrieves an image from a file and handles with the file not found error,
    if the file do not exists in the system.

    Args:
        file_name (str): the name of the image file to be opened.
        error_message (str): the error message to display if the file is not found.

    Returns:
        Image: the image object if successfully opened.

    Raises:
        SystemExit: if the image file is not found, the program exits with the
        specified error message.
    """
    try:
        return Image.open(file_name)
    except FileNotFoundError:
        sys.exit(error_message)


def create_photo(input_file_name, output_file_name):
    """
    creates a composite photo by overlaying a shirt image onto an given input image.

    Args:
        input_file_name (str): the name of the input image file.
        output_file_name (str): the desired name for the output composite image file.

    Raises:
        SystemExit: if the output file is invalid or if there are issues with opening
        the shirt image or the input image files.
    """
    if not is_valid_file(output_file_name):
        sys.exit("Invalid output")

    # open the shirt image
    shirt_image = get_image_from_file("shirt.png", "The shirt file does not exist")

    # open the input image file
    input_image = get_image_from_file(input_file_name, "Input does not exist")

    # resize and crop the input image to fit in the shirt image size
    photo = ImageOps.fit(
        input_image,
        shirt_image.size,
        method=Image.Resampling.BICUBIC,
        bleed=0.0,
        centering=(0.0, 1.5),
    )

    # overlay the shirt in the resized and cropped input image file
    photo.paste(shirt_image, shirt_image)

    # save the output image file
    photo.save(output_file_name)


if __name__ == "__main__":
    main()
