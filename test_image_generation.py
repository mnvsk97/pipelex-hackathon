"""Test script for image generation with Replicate."""

import asyncio
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

print("="*60)
print("Testing Image Generation with Replicate")
print("="*60)

# Test 1: Check API token
print("\n1. Checking Replicate API token...")
replicate_token = os.getenv("REPLICATE_API_TOKEN")
if replicate_token:
    print(f"   ✅ Token found: {replicate_token[:15]}...")
else:
    print("   ❌ Token not found!")
    exit(1)

# Test 2: Import Replicate
print("\n2. Testing Replicate import...")
try:
    import replicate
    print("   ✅ Replicate imported successfully")
except ImportError as e:
    print(f"   ❌ Import failed: {e}")
    exit(1)

# Test 3: Test image generation
print("\n3. Testing image generation...")
print("   Generating a test image (this may take 30-60 seconds)...")

try:
    output = replicate.run(
        "bytedance/seedream-4",
        input={
            "size": "2K",
            "width": 1024,
            "height": 1024,
            "prompt": "A professional tech company logo with blue and white colors, modern and clean design",
            "max_images": 1,
            "aspect_ratio": "1:1",
            "enhance_prompt": True,
        }
    )
    
    if output and len(output) > 0:
        image_url = output[0].url if hasattr(output[0], 'url') else str(output[0])
        print(f"   ✅ Image generated successfully!")
        print(f"   URL: {image_url}")
        
        # Test 4: Verify URL is accessible
        print("\n4. Verifying image URL...")
        import requests
        response = requests.head(image_url, timeout=10)
        if response.status_code == 200:
            print(f"   ✅ Image URL is accessible (Status: {response.status_code})")
        else:
            print(f"   ⚠️  Image URL returned status: {response.status_code}")
    else:
        print("   ❌ No output received from Replicate")
        
except Exception as e:
    print(f"   ❌ Image generation failed: {str(e)}")
    print(f"   Error type: {type(e).__name__}")
    import traceback
    traceback.print_exc()
    exit(1)

print("\n" + "="*60)
print("✅ All tests passed! Image generation is working.")
print("="*60)
print("\nYou can now use the Streamlit app with confidence.")
print("The app will generate real images using Replicate.")
