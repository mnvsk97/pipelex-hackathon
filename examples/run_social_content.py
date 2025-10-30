"""Example runner for social media content generation."""

import asyncio
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from pipelex import pretty_print
from pipelex.pipelex import Pipelex
from pipelex.pipeline.execute import execute_pipeline

from social_content.social_content_struct import CompanyInput, SocialMediaContent


async def generate_content(
    company_name: str,
    topic: str,
    brand_voice: str = "professional"
) -> SocialMediaContent:
    """Generate social media content for a company."""
    
    # Create input
    company_input = CompanyInput(
        company_name=company_name,
        topic=topic,
        brand_voice=brand_voice
    )
    
    # Run the pipeline
    pipe_output = await execute_pipeline(
        pipe_code="generate_social_content",
        inputs={
            "company_input": {
                "concept": "social_content.CompanyInput",
                "content": company_input,
            }
        },
    )
    
    # Return the result
    return pipe_output.main_stuff_as(content_type=SocialMediaContent)


# Start Pipelex
Pipelex.make()

# Example usage
if __name__ == "__main__":
    # Test with a sample company
    result = asyncio.run(
        generate_content(
            company_name="TechFlow AI",
            topic="How AI is transforming customer service",
            brand_voice="professional but friendly"
        )
    )
    
    print("\n" + "="*80)
    print("📸 INSTAGRAM POST")
    print("="*80)
    print(f"\nImage Prompt: {result.instagram.image_prompt}")
    print(f"\nCaption: {result.instagram.caption}")
    print(f"\nHashtags: {result.instagram.hashtags}")
    
    print("\n" + "="*80)
    print("🐦 TWITTER POST")
    print("="*80)
    print(f"\nImage Prompt: {result.twitter.image_prompt}")
    print(f"\nTweet: {result.twitter.tweet_text}")
    print("\n" + "="*80)
