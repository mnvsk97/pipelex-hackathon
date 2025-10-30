"""Replicate API integration for image and audio generation."""

import os
import replicate
from pathlib import Path

from pipelex.system.registries.func_registry import func_registry
from pipelex.core.working_memory import WorkingMemory
from pipelex.core.stuffs.image_content import ImageContent
from pipelex.core.stuffs.text_content import TextContent


@func_registry.register("generate_instagram_images")
async def generate_instagram_images(working_memory: WorkingMemory) -> list[ImageContent]:
    """Generate 5 Instagram image variations using Replicate's bytedance/seedream-4."""
    
    # Get the Instagram posts from working memory
    instagram_posts = working_memory.get_stuff("instagram_posts")
    
    # We'll generate images for the first 2 variations (with images)
    # The 3rd variation will be text-only
    images = []
    
    # Create output directory
    output_dir = Path("generated_images")
    output_dir.mkdir(exist_ok=True)
    
    # Generate 5 variations for the first Instagram post
    base_prompt = instagram_posts.content[0].image_prompt
    
    # Create 5 slightly different prompts
    prompt_variations = [
        base_prompt,
        f"{base_prompt}, vibrant colors, high contrast",
        f"{base_prompt}, soft lighting, pastel tones",
        f"{base_prompt}, dramatic lighting, bold composition",
        f"{base_prompt}, minimalist style, clean design"
    ]
    
    for i, prompt in enumerate(prompt_variations):
        try:
            # Run the model
            output = replicate.run(
                "bytedance/seedream-4",
                input={
                    "size": "2K",
                    "width": 1024,
                    "height": 1024,
                    "prompt": prompt,
                    "max_images": 1,
                    "image_input": [],
                    "aspect_ratio": "1:1",
                    "enhance_prompt": True,
                    "sequential_image_generation": "disabled"
                }
            )
            
            # Get the image URL
            if output and len(output) > 0:
                image_url = output[0].url()
                
                # Save the image locally
                image_path = output_dir / f"instagram_{i+1}.png"
                with open(image_path, "wb") as file:
                    file.write(output[0].read())
                
                # Create ImageContent with both URL and local path
                images.append(ImageContent(
                    url=image_url,
                    local_path=str(image_path)
                ))
        except Exception as e:
            print(f"Error generating image {i+1}: {e}")
            # Continue with other images even if one fails
            continue
    
    return images


@func_registry.register("generate_linkedin_images")
async def generate_linkedin_images(working_memory: WorkingMemory) -> list[ImageContent]:
    """Generate 2 LinkedIn images using Replicate's bytedance/seedream-4."""
    
    # Get the LinkedIn posts from working memory
    linkedin_posts = working_memory.get_stuff("linkedin_posts")
    
    images = []
    
    # Create output directory
    output_dir = Path("generated_images")
    output_dir.mkdir(exist_ok=True)
    
    # Generate images for the first 2 LinkedIn posts (3rd is text-only)
    for i in range(2):
        if i >= len(linkedin_posts.content):
            break
            
        prompt = linkedin_posts.content[i].image_prompt
        
        if not prompt:
            continue
        
        try:
            # Run the model with 16:9 aspect ratio for LinkedIn
            output = replicate.run(
                "bytedance/seedream-4",
                input={
                    "size": "2K",
                    "width": 1024,
                    "height": 576,  # 16:9 ratio
                    "prompt": prompt,
                    "max_images": 1,
                    "image_input": [],
                    "aspect_ratio": "16:9",
                    "enhance_prompt": True,
                    "sequential_image_generation": "disabled"
                }
            )
            
            # Get the image URL
            if output and len(output) > 0:
                image_url = output[0].url()
                
                # Save the image locally
                image_path = output_dir / f"linkedin_{i+1}.png"
                with open(image_path, "wb") as file:
                    file.write(output[0].read())
                
                # Create ImageContent
                images.append(ImageContent(
                    url=image_url,
                    local_path=str(image_path)
                ))
        except Exception as e:
            print(f"Error generating LinkedIn image {i+1}: {e}")
            continue
    
    return images


@func_registry.register("generate_instagram_audio")
async def generate_instagram_audio(working_memory: WorkingMemory) -> TextContent:
    """Generate voiceover for Instagram post using Replicate's minimax/speech-02-hd."""
    
    # Get the Instagram posts from working memory
    instagram_posts = working_memory.get_stuff("instagram_posts")
    
    # Use the caption from the first Instagram post as the script
    script = instagram_posts.content[0].caption
    
    # Create output directory
    output_dir = Path("generated_audio")
    output_dir.mkdir(exist_ok=True)
    
    try:
        # Run the model
        output = replicate.run(
            "minimax/speech-02-hd",
            input={
                "text": script,
                "pitch": 0,
                "speed": 1,
                "volume": 1,
                "bitrate": 128000,
                "channel": "mono",
                "emotion": "happy",
                "voice_id": "Friendly_Person",
                "sample_rate": 32000,
                "language_boost": "English",
                "english_normalization": True
            }
        )
        
        # Get the audio URL
        audio_url = output.url()
        
        # Save the audio locally
        audio_path = output_dir / "instagram_voiceover.mp3"
        with open(audio_path, "wb") as file:
            file.write(output.read())
        
        return TextContent(text=f"Audio generated: {audio_url}")
    
    except Exception as e:
        print(f"Error generating audio: {e}")
        return TextContent(text=f"Audio generation error: {str(e)}")
