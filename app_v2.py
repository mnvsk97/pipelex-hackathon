"""Streamlit UI for Social Media Content Generator - Extended Version."""

import asyncio
import sys
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

import streamlit as st
from pipelex.pipelex import Pipelex
from pipelex.pipeline.execute import execute_pipeline

from social_content.social_content_struct import CompanyInput, SocialMediaContent


# Initialize Pipelex (only once)
@st.cache_resource
def init_pipelex():
    """Initialize Pipelex."""
    return Pipelex.make()


init_pipelex()


async def generate_content_async(company_name: str, topic: str, brand_voice: str) -> SocialMediaContent:
    """Generate social media content asynchronously."""
    company_input = CompanyInput(
        company_name=company_name,
        topic=topic,
        brand_voice=brand_voice
    )
    
    pipe_output = await execute_pipeline(
        pipe_code="generate_social_content",
        inputs={
            "company_input": {
                "concept": "social_content.CompanyInput",
                "content": company_input,
            }
        },
    )
    
    return pipe_output.main_stuff_as(content_type=SocialMediaContent)


def generate_content(company_name: str, topic: str, brand_voice: str) -> SocialMediaContent:
    """Synchronous wrapper for async content generation."""
    return asyncio.run(generate_content_async(company_name, topic, brand_voice))


# Streamlit UI
st.set_page_config(page_title="Social Media Content Generator", page_icon="🚀", layout="wide")

st.title("🚀 Social Media Content Generator")
st.markdown("Generate Instagram, Twitter, and LinkedIn content based on competitor research")

# Sidebar for inputs
with st.sidebar:
    st.header("📝 Input Details")
    
    company_name = st.text_input(
        "Company Name",
        placeholder="e.g., TechFlow AI",
        help="Enter your company name"
    )
    
    topic = st.text_area(
        "Content Topic",
        placeholder="e.g., How AI is transforming customer service",
        help="What do you want to post about?",
        height=100
    )
    
    brand_voice = st.selectbox(
        "Brand Voice",
        ["professional", "casual", "playful", "authoritative", "friendly", "inspirational"],
        help="Choose your brand's tone"
    )
    
    st.markdown("---")
    
    generate_images = st.checkbox(
        "🎨 Generate Images (Replicate)",
        value=False,
        help="Generate actual images using Replicate API (requires API key)"
    )
    
    generate_button = st.button("🎨 Generate Content", type="primary", use_container_width=True)

# Main content area
if generate_button:
    if not company_name or not topic:
        st.error("⚠️ Please fill in both Company Name and Content Topic")
    else:
        with st.spinner("🔍 Researching competitors and generating content... (30-60 seconds)"):
            try:
                result = generate_content(company_name, topic, brand_voice)
                
                # Create tabs for different platforms
                tab1, tab2, tab3 = st.tabs(["📸 Instagram", "🐦 Twitter", "💼 LinkedIn"])
                
                with tab1:
                    st.subheader("Instagram Posts (3 Variations)")
                    
                    for i, post in enumerate(result.instagram, 1):
                        with st.expander(f"📱 Variation {i}: {post.variation_angle}", expanded=(i==1)):
                            col1, col2 = st.columns([1, 1])
                            
                            with col1:
                                st.markdown("**🎨 Image Prompt**")
                                st.info(post.image_prompt)
                                
                                if generate_images and i <= 2:
                                    st.markdown("**Generated Images**")
                                    st.warning("🚧 Image generation coming soon! Use the prompt above with DALL-E or Midjourney.")
                            
                            with col2:
                                st.markdown("**✍️ Caption**")
                                st.text_area(
                                    "Caption",
                                    value=post.caption,
                                    height=120,
                                    key=f"ig_caption_{i}",
                                    label_visibility="collapsed"
                                )
                                
                                st.markdown("**#️⃣ Hashtags**")
                                st.code(post.hashtags, language=None)
                
                with tab2:
                    st.subheader("Twitter Post")
                    
                    col1, col2 = st.columns([1, 1])
                    
                    with col1:
                        st.markdown("**🎨 Image Prompt**")
                        st.info(result.twitter.image_prompt)
                        st.caption("Use this prompt with an AI image generator")
                    
                    with col2:
                        st.markdown("**✍️ Tweet**")
                        tweet_length = len(result.twitter.tweet_text)
                        st.text_area(
                            "Tweet",
                            value=result.twitter.tweet_text,
                            height=100,
                            key="tw_tweet",
                            label_visibility="collapsed"
                        )
                        st.caption(f"Character count: {tweet_length}/280")
                
                with tab3:
                    st.subheader("LinkedIn Posts (3 Variations)")
                    
                    for i, post in enumerate(result.linkedin, 1):
                        with st.expander(f"💼 Variation {i}: {post.variation_angle}", expanded=(i==1)):
                            col1, col2 = st.columns([1, 1])
                            
                            with col1:
                                if post.image_prompt:
                                    st.markdown("**🎨 Image Prompt**")
                                    st.info(post.image_prompt)
                                    
                                    if generate_images and i <= 2:
                                        st.markdown("**Generated Image**")
                                        st.warning("🚧 Image generation coming soon!")
                                else:
                                    st.info("📝 Text-only post (no image)")
                            
                            with col2:
                                st.markdown("**✍️ Post Text**")
                                st.text_area(
                                    "Post",
                                    value=post.post_text,
                                    height=200,
                                    key=f"li_post_{i}",
                                    label_visibility="collapsed"
                                )
                                char_count = len(post.post_text)
                                st.caption(f"Character count: {char_count}")
                
                st.success("✅ Content generated successfully!")
                
            except Exception as e:
                st.error(f"❌ Error generating content: {str(e)}")
                st.exception(e)

else:
    # Show placeholder when no content is generated
    st.info("👈 Fill in the details in the sidebar and click 'Generate Content' to get started!")
    
    st.markdown("### How it works:")
    st.markdown("""
    1. **Enter your company details** - Tell us about your company and what you want to post about
    2. **Choose your brand voice** - Select the tone that matches your brand
    3. **Generate content** - Our AI will:
       - Research your top 5 competitors' social media strategies
       - Analyze what makes their content engaging
       - Create unique content tailored to your brand
       - Generate 3 variations for Instagram and LinkedIn
       - Create image prompts and captions for all platforms
    """)
    
    st.markdown("### What you'll get:")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**📸 Instagram**")
        st.markdown("- 3 variations with different angles")
        st.markdown("- 2 with image prompts")
        st.markdown("- 1 text-only")
        st.markdown("- Captions & hashtags")
    
    with col2:
        st.markdown("**🐦 Twitter**")
        st.markdown("- Image prompt")
        st.markdown("- Punchy tweet text")
        st.markdown("- Character count")
    
    with col3:
        st.markdown("**💼 LinkedIn**")
        st.markdown("- 3 professional variations")
        st.markdown("- 2 with image prompts")
        st.markdown("- 1 text-only")
        st.markdown("- Long-form content")

# Footer
st.markdown("---")
st.caption("Built with Pipelex 🚀 | Powered by AI")
