import textwrap
import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import rembg  # Background removal
import os
import cv2

# st.title("🔥 Meme, GIF & Sticker Generator 🎨")
st.title("🔥 Mematic 🎨")
# Sidebar for selection
option = st.sidebar.selectbox("Choose a feature:", ["Meme Generator", "GIF Creator", "Sticker Maker"])

# --------------------- MEME GENERATOR ---------------------
if option == "Meme Generator":
    st.header("🖼️ Meme Generator")

    meme_option = st.radio("Choose Meme Source:", ["Use Template", "Upload Your Own Image"])

    if meme_option == "Use Template":
        meme_templates = ["drake", "doge", "success", "wonka", "joker", "spongegar"]
        template = st.selectbox("Choose a Meme Template:", meme_templates)
        top_text = st.text_input("Top Text", "Top Caption").replace(" ", "_")
        bottom_text = st.text_input("Bottom Text", "Bottom Caption").replace(" ", "_")
        text_color = st.color_picker("Pick Text Color", "#FFFFFF")

        if st.button("Generate Meme"):
            meme_url = f"https://memegen.link/{template}/{top_text}/{bottom_text}.jpg?text_color={text_color[1:]}"
            st.image(meme_url, caption="Generated Meme", use_column_width=True)
            st.download_button("Download Meme", meme_url, "meme.jpg")

    else:  # User uploads an image
        uploaded_file = st.file_uploader("Upload an image", type=["jpg", "png", "jpeg"])

        if uploaded_file:
            # Save uploaded file
            image = Image.open(uploaded_file)
            img_path = "uploaded_meme.jpg"
            image.save(img_path)

            st.image(image, caption="Uploaded Image", use_column_width=True)

            top_text = st.text_input("Top Text", "Top Caption")
            bottom_text = st.text_input("Bottom Text", "Bottom Caption")
            text_color = st.color_picker("Pick Text Color", "#FFFFFF")
            font_size = st.slider("Font Size", min_value=20, max_value=100, value=40)

            if st.button("Generate Meme"):
                # Load image using OpenCV
                img = cv2.imread(img_path)
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                pil_img = Image.fromarray(img)

                # Load Impact font
                font_path = "impact.ttf"  # Ensure you have 'impact.ttf' in the working directory
                try:
                    font = ImageFont.truetype(font_path, font_size)
                except IOError:
                    font = ImageFont.load_default()  # Fallback if font is not found

                draw = ImageDraw.Draw(pil_img)

                # Get image dimensions
                width, height = pil_img.size

                def draw_text_with_outline(draw, text, y_position):
                # """Draws text centered with an outline effect."""

                    # if not text:
                    #     return  # Avoid errors if text is empty or None
                    # text = str(text).strip()
                    wrapped_text = textwrap.fill(text, width=20)  # Wrap long text
                    text_width, text_height = draw.textbbox((0, 0), wrapped_text, font=font)[2:]

                    x_position = (width - text_width) // 2  # Center horizontally
                    y_position = y_position - text_height // 2  # Adjust vertically for better positioning
                
                    outline_color = "black"
                    for dx in [-2, 0, 2]:
                        for dy in [-2, 0, 2]:
                            draw.text((x_position + dx, y_position + dy), wrapped_text, font=font, fill=outline_color)

                    draw.text((x_position, y_position), wrapped_text, font=font, fill=text_color)


                # Centered top and bottom text
                # draw_text_with_outline(draw, top_text, (width // 2, 10))
                # draw_text_with_outline(draw, bottom_text, (width // 2, height - font_size - 10))
                # Draw top and bottom text
                draw_text_with_outline(draw, top_text, 10)
                draw_text_with_outline(draw, bottom_text, height - font_size - 10)


                # Save and display final meme
                output_path = "final_meme.jpg"
                pil_img.save(output_path)

                st.image(pil_img, caption="Your Meme", use_column_width=True)
                with open(output_path, "rb") as file:
                    st.download_button("Download Meme", file, "meme.jpg")


# --------------------- GIF CREATOR ---------------------


if option == "GIF Creator":
    st.header("🎞️ GIF Creator")

    gif_option = st.radio("Choose Input Type", ["Images", "Video"])

    if gif_option == "Images":
        uploaded_files = st.file_uploader("Upload multiple images", accept_multiple_files=True, type=["jpg", "png", "jpeg"])
        speed = st.selectbox("GIF Speed", ["0.5x (Slow)", "1x (Normal)", "2x (Fast)", "3x (Very Fast)"])
        speed_multiplier = {"0.5x (Slow)": 200, "1x (Normal)": 100, "2x (Fast)": 50, "3x (Very Fast)": 30}
        frame_duration = speed_multiplier[speed]

        add_text = st.text_input("Add Text to GIF", "")
        text_color = st.color_picker("Pick Text Color", "#FFFFFF")

        if uploaded_files and st.button("Create GIF"):
            frames = [Image.open(file).resize((300, 300)) for file in uploaded_files]

            if add_text:
                for frame in frames:
                    draw = ImageDraw.Draw(frame)
                    try:
                        font = ImageFont.truetype("impact.ttf", 40)  # Using Impact font
                    except IOError:
                        font = ImageFont.load_default()

                    text_position = (frame.width // 2, frame.height - 40)
                    draw.text(text_position, add_text, fill=text_color, font=font, anchor="mm")

            frames[0].save("animated.gif", save_all=True, append_images=frames[1:], duration=frame_duration, loop=0)
            st.image("animated.gif", caption="Generated GIF", use_column_width=True)
            st.download_button("Download GIF", open("animated.gif", "rb"), "animated.gif")

    elif gif_option == "Video":
        uploaded_video = st.file_uploader("Upload a video", type=["mp4", "avi", "mov"])
        frame_skip = st.slider("Frame Skip (higher = fewer frames)", 1, 10, 3)
        speed = st.selectbox("GIF Speed", ["0.5x (Slow)", "1x (Normal)", "2x (Fast)", "3x (Very Fast)"])
        speed_multiplier = {"0.5x (Slow)": 200, "1x (Normal)": 100, "2x (Fast)": 50, "3x (Very Fast)": 30}
        frame_duration = speed_multiplier[speed]

        add_text = st.text_input("Add Text to GIF", "")
        text_color = st.color_picker("Pick Text Color", "#FFFFFF")

        if uploaded_video and st.button("Convert Video to GIF"):
            video_path = "uploaded_video.mp4"
            with open(video_path, "wb") as f:
                f.write(uploaded_video.read())

            cap = cv2.VideoCapture(video_path)
            frames = []
            count = 0

            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break
                if count % frame_skip == 0:
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    img = Image.fromarray(frame).resize((300, 300))

                    if add_text:
                        draw = ImageDraw.Draw(img)
                        try:
                            font = ImageFont.truetype("impact.ttf", 40)  # Using Impact font
                        except IOError:
                            font = ImageFont.load_default()

                        text_position = (img.width // 2, img.height - 40)
                        draw.text(text_position, add_text, fill=text_color, font=font, anchor="mm")

                    frames.append(img)
                count += 1
            
            cap.release()

            if frames:
                frames[0].save("video_to_gif.gif", save_all=True, append_images=frames[1:], duration=frame_duration, loop=0)
                st.image("video_to_gif.gif", caption="Generated GIF from Video", use_column_width=True)
                st.download_button("Download GIF", open("video_to_gif.gif", "rb"), "video_to_gif.gif")
            else:
                st.error("No frames extracted. Try reducing the Frame Skip value.")




# --------------------- STICKER MAKER ---------------------

elif option == "Sticker Maker":
    st.header("🧩 Sticker Maker")
    uploaded_image = st.file_uploader("Upload an Image", type=["jpg", "png", "jpeg"])
    remove_bg = st.checkbox("Remove Background")
    add_text = st.text_input("Add Text to Sticker", "")
    text_color = st.color_picker("Pick Text Color", "#FFFFFF")

    def create_sticker(image, text, text_color):
        img_rgba = image.convert("RGBA")
        alpha = img_rgba.split()[3]
        alpha_array = np.array(alpha)
        edges = np.where(alpha_array > 10, 255, 0).astype(np.uint8)
        
        for _ in range(10):  # Create a bold outline effect
            edges = np.maximum(edges, np.roll(edges, 1, axis=0))
            edges = np.maximum(edges, np.roll(edges, -1, axis=0))
            edges = np.maximum(edges, np.roll(edges, 1, axis=1))
            edges = np.maximum(edges, np.roll(edges, -1, axis=1))

        outline = Image.fromarray(edges).convert("L")
        white_outline = Image.new("RGBA", img_rgba.size, (255, 255, 255, 255))
        white_outline.putalpha(outline)
        final_sticker = Image.alpha_composite(white_outline, img_rgba)

        if text:
            try:
                font = ImageFont.truetype("arial.ttf", final_sticker.width // 10)  # Adjust font size
            except:
                font = ImageFont.load_default()

            text_bbox = font.getbbox(text)  # Correct method to get text size
            text_width, text_height = text_bbox[2] - text_bbox[0], text_bbox[3] - text_bbox[1]
            caption_height = text_height + 80

            # Create a new image with space below for text
            new_height = final_sticker.height + caption_height
            sticker_with_text = Image.new("RGBA", (final_sticker.width, new_height), (255, 255, 255, 0))
            sticker_with_text.paste(final_sticker, (0, 0), final_sticker)

            draw = ImageDraw.Draw(sticker_with_text)
            text_x = (sticker_with_text.width - text_width) // 2
            text_y = final_sticker.height + 30  # Positioning text below the sticker
            draw.text((text_x, text_y), text, fill=text_color, font=font)

            return sticker_with_text

        return final_sticker

    if uploaded_image and st.button("Generate Sticker"):
        image = Image.open(uploaded_image)
        if remove_bg:
            st.write("Removing background...")
            image = rembg.remove(image)

        sticker = create_sticker(image, add_text, text_color)
        st.image(sticker, caption="Generated Sticker", use_column_width=True)
        sticker.save("sticker.png")
        st.download_button("Download Sticker", open("sticker.png", "rb"), "sticker.png")

