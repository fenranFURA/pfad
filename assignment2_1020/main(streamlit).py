import streamlit as st
from diffusers import DiffusionPipeline
import torch

# Initialize the pipeline if not already done
if "pipeline" not in st.session_state:
    model = "runwayml/stable-diffusion-v1-5"
    st.session_state["pipeline"] = DiffusionPipeline.from_pretrained(model, torch_dtype=torch.float16)
    st.session_state["pipeline"].to("cuda")

# Input prompt
prompt = st.text_input("Your wish is my command:")

# Generate the initial image
if prompt and "initial_image" not in st.session_state:
    with st.spinner("Painting with pixels..."):
        img = st.session_state["pipeline"](prompt).images[0]
        st.session_state["initial_image"] = img
        st.image(img, use_column_width=True)

# Display the initial image
if "initial_image" in st.session_state:
    st.image(st.session_state["initial_image"], caption="Initial Image", use_column_width=True)

# Adjust intensity level
level = st.slider("How wild do you want the image to be? (0-5):", 0, 5, 0)

# Generate new images based on intensity level
if prompt and level > 0:
    en_prompt = f"{prompt}, detailed and vibrant, level {level}"
    if "images" not in st.session_state:
        st.session_state["images"] = []
    if en_prompt:
        with st.spinner("Generating..."):
            images = st.session_state["pipeline"](en_prompt, num_inference_steps=8, guidance_scale=2, num_images_per_prompt=1).images
            for image in images:
                st.session_state["images"].append(image)

        # Display the new images
        for img in st.session_state["images"][::-1]:
            st.image(img, caption=f"Intensity Level {level}", use_column_width=True)