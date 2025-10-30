"""Quick test script for Replicate integration."""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Test if Replicate is properly configured
replicate_token = os.getenv("REPLICATE_API_TOKEN")
if replicate_token:
    print("✅ Replicate API token found")
    print(f"   Token: {replicate_token[:10]}...")
else:
    print("❌ Replicate API token not found in .env")
    print("   Please add: REPLICATE_API_TOKEN=your_token_here")

# Test import
try:
    import replicate
    print("✅ Replicate package installed")
except ImportError:
    print("❌ Replicate package not installed")
    print("   Run: uv pip install replicate")

# Test Pipelex
try:
    from pipelex.pipelex import Pipelex
    print("✅ Pipelex installed")
except ImportError:
    print("❌ Pipelex not installed")

print("\n" + "="*50)
print("Ready to generate content!")
print("="*50)
print("\nRun the app with: streamlit run app_v3.py")
