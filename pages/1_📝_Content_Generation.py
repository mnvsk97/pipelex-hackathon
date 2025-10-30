"""Content Generation page - moved from app_v3.py"""

import asyncio
import streamlit as st
from pipelex.pipelex import Pipelex
from pipelex.pipeline.execute import execute_pipeline
from social_content.social_content_struct import (
    CompanyInput,
    SocialMediaContent,
    MarketResearch,
)
from pipelex.core.stuffs.image_content import ImageContent

import os
os.environ["REPLICATE_API_TOKEN"] = ""

st.set_page_config(
    page_title="Content Generation",
    page_icon="📝",
    layout="wide",
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .step-header {
        font-size: 1.5rem;
        font-weight: bold;
        color: #2ca02c;
        margin-top: 1rem;
        margin-bottom: 0.5rem;
    }
    .competitor-card {
        background-color: rgba(240, 242, 246, 0.1);
        border: 1px solid rgba(128, 128, 128, 0.3);
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 0.5rem;
        color: inherit;
    }
    .competitor-card strong {
        color: #1f77b4;
    }
    .success-box {
        background-color: rgba(212, 237, 218, 0.2);
        border: 1px solid #2ca02c;
        border-radius: 0.5rem;
        padding: 1rem;
        margin: 1rem 0;
        color: inherit;
    }
    .info-box {
        background-color: rgba(209, 236, 241, 0.2);
        border: 1px solid #1f77b4;
        border-radius: 0.5rem;
        padding: 1rem;
        margin: 1rem 0;
        color: inherit;
    }
</style>
""", unsafe_allow_html=True)

# Initialize Pipelex
@st.cache_resource
def init_pipelex():
    return Pipelex.make()

pipelex = init_pipelex()

# Title
st.markdown('<div class="main-header">📝 Social Media Content Generator</div>', unsafe_allow_html=True)

# Sidebar - Inputs
with st.sidebar:
    st.header("📝 Input Details")
    
    company_name = st.text_input("Company Name", value="TechFlow AI", help="Enter your company name")
    topic = st.text_area(
        "Content Topic",
        value="How Gemini models are transforming LLM app development",
        height=100,
        help="What do you want to create content about?"
    )
    
    st.subheader("Brand Settings")
    brand_voice = st.selectbox(
        "Brand Voice",
        ["professional", "casual", "playful", "authoritative", "friendly", "inspirational"],
        help="Choose the tone for your content"
    )
    
    st.subheader("Optional Features")
    generate_audio = st.checkbox("🎵 Generate Audio for Instagram", help="Generate voiceover for Instagram posts (experimental)")
    
    generate_button = st.button("🎨 Generate Content", type="primary", use_container_width=True)

# Main content area
if generate_button:
    if not company_name or not topic:
        st.error("⚠️ Please fill in all required fields!")
    else:
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # Step 1: Research
        status_text.markdown('<div class="step-header">🔍 Researching Competitors...</div>', unsafe_allow_html=True)
        progress_bar.progress(20)
        
        research_container = st.container()
        
        # Step 2: Generate content
        status_text.markdown('<div class="step-header">✍️ Generating Content...</div>', unsafe_allow_html=True)
        progress_bar.progress(40)
        
        try:
            # Create input
            company_input = CompanyInput(
                company_name=company_name,
                topic=topic,
                brand_voice=brand_voice
            )
            
            # Execute pipeline
            async def run_pipeline():
                return await execute_pipeline(
                    pipe_code="generate_social_content",
                    inputs={
                        "company_input": {
                            "concept": "social_content.CompanyInput",
                            "content": company_input,
                        }
                    },
                )
            
            pipe_output = asyncio.run(run_pipeline())
            progress_bar.progress(60)
            
            # Extract results
            working_memory = pipe_output.working_memory
            
            # Get research data
            research_stuff = working_memory.get_stuff("research")
            research: MarketResearch = research_stuff.content
            
            # Get individual content pieces
            instagram_stuff = working_memory.get_stuff("instagram_posts")
            twitter_stuff = working_memory.get_stuff("twitter")
            linkedin_stuff = working_memory.get_stuff("linkedin_posts")
            
            # Extract lists properly
            from pipelex.core.stuffs.list_content import ListContent
            
            if isinstance(instagram_stuff.content, ListContent):
                instagram_posts = instagram_stuff.content.items
            else:
                instagram_posts = [instagram_stuff.content]
            
            if isinstance(linkedin_stuff.content, ListContent):
                linkedin_posts = linkedin_stuff.content.items
            else:
                linkedin_posts = [linkedin_stuff.content]
            
            # Convert to dicts
            result = SocialMediaContent(
                instagram=[post.model_dump() for post in instagram_posts],
                twitter=twitter_stuff.content.model_dump(),
                linkedin=[post.model_dump() for post in linkedin_posts]
            )
            
            # Display research results
            progress_bar.progress(65)
            
            with research_container:
                st.markdown('<div class="success-box">', unsafe_allow_html=True)
                st.markdown("### 🎯 Competitor Research Complete!")
                st.markdown(f"**Analyzed {len(research.insights)} top competitors in your industry**")
                st.markdown('</div>', unsafe_allow_html=True)
                
                st.markdown("#### 📊 Competitors Analyzed:")
                cols = st.columns(min(3, len(research.insights)))
                for idx, insight in enumerate(research.insights):
                    with cols[idx % 3]:
                        st.markdown(f"""
                        <div class="competitor-card">
                            <strong>{insight.competitor_name}</strong><br>
                            <small><em>{insight.content_style[:80]}...</em></small>
                        </div>
                        """, unsafe_allow_html=True)
                
                with st.expander("🔑 Key Trends & Recommendations", expanded=False):
                    st.markdown(f"**Key Trends:**\n{research.key_trends}")
                    st.markdown(f"**Recommendations:**\n{research.recommendations}")
            
            # Generate images
            status_text.markdown('<div class="step-header">🎨 Generating AI Images...</div>', unsafe_allow_html=True)
            progress_bar.progress(70)
            
            st.session_state['instagram_images'] = []
            st.session_state['linkedin_images'] = []
            
            try:
                import replicate
                
                # Generate Instagram images
                instagram_images = []
                for idx in range(min(2, len(result.instagram))):
                    post = result.instagram[idx]
                    if post.image_prompt and post.image_prompt.strip() and post.image_prompt.lower() != 'none':
                        try:
                            output = replicate.run(
                                "bytedance/seedream-4",
                                input={
                                    "size": "2K",
                                    "width": 1024,
                                    "height": 1024,
                                    "prompt": post.image_prompt,
                                    "max_images": 1,
                                    "aspect_ratio": "1:1",
                                    "enhance_prompt": True,
                                }
                            )
                            if output and len(output) > 0:
                                image_url = output[0].url if hasattr(output[0], 'url') else str(output[0])
                                instagram_images.append(ImageContent(url=image_url))
                        except Exception as e:
                            st.warning(f"Image {idx+1} generation failed: {str(e)}")
                
                st.session_state['instagram_images'] = instagram_images
                progress_bar.progress(85)
                
                # Generate LinkedIn images
                linkedin_images = []
                if len(result.linkedin) > 0:
                    post = result.linkedin[0]
                    if post.image_prompt and post.image_prompt.strip():
                        try:
                            output = replicate.run(
                                "bytedance/seedream-4",
                                input={
                                    "size": "2K",
                                    "width": 1024,
                                    "height": 576,
                                    "prompt": post.image_prompt,
                                    "max_images": 1,
                                    "aspect_ratio": "16:9",
                                    "enhance_prompt": True,
                                }
                            )
                            if output and len(output) > 0:
                                image_url = output[0].url if hasattr(output[0], 'url') else str(output[0])
                                linkedin_images.append(ImageContent(url=image_url))
                        except Exception as e:
                            st.warning(f"LinkedIn image generation failed: {str(e)}")
                
                st.session_state['linkedin_images'] = linkedin_images
                
            except Exception as e:
                st.error(f"Image generation error: {str(e)}")
            
            progress_bar.progress(100)
            status_text.markdown('<div class="step-header">✅ Complete!</div>', unsafe_allow_html=True)
            
            # Display results in tabs
            st.markdown("---")
            st.markdown("## 📱 Generated Content")
            
            tab1, tab2, tab3 = st.tabs(["📸 Instagram", "🐦 Twitter", "💼 LinkedIn"])
            
            # Instagram Tab
            with tab1:
                st.markdown("### Instagram Posts (3 Variations)")
                
                for idx, post in enumerate(result.instagram, 1):
                    with st.expander(f"✨ Variation {idx}: {post.variation_angle.title()}", expanded=(idx == 1)):
                        col1, col2 = st.columns([1, 2])
                        
                        with col1:
                            if post.image_prompt and post.image_prompt.lower() != "none" and post.image_prompt.strip():
                                instagram_images = st.session_state.get('instagram_images', [])
                                if instagram_images and idx <= len(instagram_images):
                                    st.image(instagram_images[idx-1].url, caption=f"AI Generated Image {idx}")
                                else:
                                    st.image("https://via.placeholder.com/400x400?text=Generating...", caption=f"Image for Variation {idx}")
                                
                                st.caption("🎨 Image Prompt:")
                                st.text_area(f"Image prompt {idx}", post.image_prompt, height=100, key=f"ig_img_{idx}", label_visibility="collapsed")
                            else:
                                st.info("📝 Text-only post (no image)")
                        
                        with col2:
                            st.markdown("**Caption:**")
                            st.text_area(f"Caption {idx}", post.caption, height=120, key=f"ig_cap_{idx}", label_visibility="collapsed")
                            
                            st.markdown("**Hashtags:**")
                            st.text_input(f"Hashtags {idx}", post.hashtags, key=f"ig_hash_{idx}", label_visibility="collapsed")
            
            # Twitter Tab
            with tab2:
                st.markdown("### Twitter Post")
                
                col1, col2 = st.columns([1, 2])
                
                with col1:
                    instagram_images = st.session_state.get('instagram_images', [])
                    if instagram_images:
                        st.image(instagram_images[0].url, caption="AI Generated Twitter Image")
                    else:
                        st.image("https://via.placeholder.com/400x400?text=Generating...", caption="Twitter Image")
                    
                    st.caption("🎨 Image Prompt:")
                    st.text_area("Twitter image prompt", result.twitter.image_prompt, height=100, key="tw_img", label_visibility="collapsed")
                
                with col2:
                    st.markdown("**Tweet Text:**")
                    tweet = st.text_area("Tweet", result.twitter.tweet_text, height=100, key="tw_text", label_visibility="collapsed")
                    
                    char_count = len(tweet)
                    if char_count > 280:
                        st.error(f"⚠️ Tweet is {char_count - 280} characters too long!")
                    else:
                        st.success(f"✅ {280 - char_count} characters remaining")
            
            # LinkedIn Tab
            with tab3:
                st.markdown("### LinkedIn Posts (3 Variations)")
                
                for idx, post in enumerate(result.linkedin, 1):
                    with st.expander(f"💼 Variation {idx}: {post.variation_angle.title()}", expanded=(idx == 1)):
                        if post.image_prompt and post.image_prompt.strip():
                            col1, col2 = st.columns([1, 2])
                            
                            with col1:
                                linkedin_images = st.session_state.get('linkedin_images', [])
                                if linkedin_images and idx <= len(linkedin_images):
                                    st.image(linkedin_images[idx-1].url, caption=f"AI Generated LinkedIn Image {idx}")
                                else:
                                    st.image("https://via.placeholder.com/400x400?text=Generating...", caption=f"LinkedIn Image {idx}")
                                
                                st.caption("🎨 Image Prompt:")
                                st.text_area(f"LinkedIn image prompt {idx}", post.image_prompt, height=80, key=f"li_img_{idx}", label_visibility="collapsed")
                            
                            with col2:
                                st.markdown("**Post Text:**")
                                st.text_area(f"LinkedIn post {idx}", post.post_text, height=250, key=f"li_text_{idx}", label_visibility="collapsed")
                        else:
                            st.markdown("**Post Text:**")
                            st.text_area(f"LinkedIn post {idx}", post.post_text, height=250, key=f"li_text_only_{idx}", label_visibility="collapsed")
            
            # Summary
            st.markdown("---")
            st.markdown("### 📊 Generation Summary")
            st.markdown(f"""
            - **Competitors Analyzed:** {len(research.insights)}
            - **Instagram Posts:** 3 variations
            - **Twitter Posts:** 1 post
            - **LinkedIn Posts:** 3 variations
            - **Total Content Pieces:** 7
            - **Brand Voice:** {brand_voice.title()}
            """)
            
        except Exception as e:
            st.error(f"❌ Error generating content: {str(e)}")
            st.exception(e)

else:
    # Welcome message
    st.markdown('<div class="info-box">', unsafe_allow_html=True)
    st.markdown("""
    ### 👋 Welcome to the Content Generator!
    
    This tool helps you create professional social media content across multiple platforms.
    
    **Get Started:**
    1. Fill in your company details in the sidebar
    2. Choose your brand voice
    3. Click "Generate Content"
    4. Review and edit the generated content
    """)
    st.markdown('</div>', unsafe_allow_html=True)
