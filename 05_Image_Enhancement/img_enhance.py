from PIL import Image, ImageEnhance, ImageFilter
import os

# ---------------------------------------------------
# IMAGE ENHANCEMENT PROJECT
# ---------------------------------------------------

# Input and output file names
input_image = "sample_image.png"
output_image = "enhanced_image.jpg"

# Check whether input image exists
if not os.path.exists(input_image):
    print(f"Error: {input_image} was not found.")
    print("Place your image in the same folder as this Python file.")
    exit()

try:
    # ------------------------------------------------
    # 1. Open the image
    # ------------------------------------------------
    image = Image.open(input_image)

    print("Image loaded successfully!")
    print("Original image size:", image.size)
    print("Original image mode:", image.mode)

    # Convert to RGB
    image = image.convert("RGB")

    # ------------------------------------------------
    # 2. Enhance Brightness
    # ------------------------------------------------
    brightness = ImageEnhance.Brightness(image)
    image = brightness.enhance(1.2)

    # ------------------------------------------------
    # 3. Enhance Contrast
    # ------------------------------------------------
    contrast = ImageEnhance.Contrast(image)
    image = contrast.enhance(1.3)

    # ------------------------------------------------
    # 4. Enhance Color
    # ------------------------------------------------
    color = ImageEnhance.Color(image)
    image = color.enhance(1.2)

    # ------------------------------------------------
    # 5. Enhance Sharpness
    # ------------------------------------------------
    sharpness = ImageEnhance.Sharpness(image)
    image = sharpness.enhance(1.5)

    # ------------------------------------------------
    # 6. Apply additional sharpening filter
    # ------------------------------------------------
    image = image.filter(ImageFilter.SHARPEN)

    # ------------------------------------------------
    # 7. Save enhanced image
    # ------------------------------------------------
    image.save(output_image, quality=95)

    print("\nImage enhancement completed successfully!")
    print("Enhanced image saved as:", output_image)

except Exception as e:
    print("An error occurred:", e)