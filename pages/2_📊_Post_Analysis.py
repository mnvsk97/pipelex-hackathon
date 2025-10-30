"""Post Analysis page with campaign analytics."""

import asyncio
import json
import streamlit as st
from pipelex.pipelex import Pipelex
from pipelex.pipeline.execute import execute_pipeline
from social_media_analysis.analytics_struct import PostMetrics, AnalysisOutput
from pipelex.core.stuffs.text_content import TextContent

st.set_page_config(
    page_title="Post Analysis",
    page_icon="📊",
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
    .metric-card {
        background-color: rgba(240, 242, 246, 0.1);
        border: 1px solid rgba(128, 128, 128, 0.3);
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    .strength {
        color: #2ca02c;
        font-weight: bold;
    }
    .weakness {
        color: #d62728;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Initialize Pipelex
@st.cache_resource
def init_pipelex():
    return Pipelex.make()

pipelex = init_pipelex()

# Title
st.markdown('<div class="main-header">📊 Social Media Post Analysis</div>', unsafe_allow_html=True)

# Dummy data
DUMMY_POSTS = [
    {
        "post_id": "IG_001",
        "platform": "Instagram",
        "topic": "AI Technology",
        "format": "image",
        "timestamp": "2024-01-15T10:00:00",
        "likes": 1250,
        "comments": 85,
        "shares": 42,
        "impressions": 15000,
        "clicks": 450,
        "saves": 120
    },
    {
        "post_id": "TW_001",
        "platform": "Twitter",
        "topic": "AI Technology",
        "format": "text",
        "timestamp": "2024-01-15T14:00:00",
        "likes": 890,
        "comments": 45,
        "shares": 120,
        "impressions": 12000,
        "clicks": 380,
        "saves": 0
    },
    {
        "post_id": "LI_001",
        "platform": "LinkedIn",
        "topic": "AI Technology",
        "format": "image",
        "timestamp": "2024-01-16T09:00:00",
        "likes": 650,
        "comments": 32,
        "shares": 78,
        "impressions": 8500,
        "clicks": 290,
        "saves": 45
    },
    {
        "post_id": "IG_002",
        "platform": "Instagram",
        "topic": "Product Launch",
        "format": "carousel",
        "timestamp": "2024-01-17T11:00:00",
        "likes": 2100,
        "comments": 156,
        "shares": 89,
        "impressions": 22000,
        "clicks": 680,
        "saves": 245
    },
    {
        "post_id": "TW_002",
        "platform": "Twitter",
        "topic": "Product Launch",
        "format": "image",
        "timestamp": "2024-01-17T15:00:00",
        "likes": 1450,
        "comments": 92,
        "shares": 210,
        "impressions": 18000,
        "clicks": 540,
        "saves": 0
    }
]

# Sidebar
with st.sidebar:
    st.header("📊 Analysis Settings")
    
    # Select post
    post_ids = [post["post_id"] for post in DUMMY_POSTS]
    selected_post_id = st.selectbox("Select Post to Analyze", post_ids)
    
    # Show post details
    selected_post = next(p for p in DUMMY_POSTS if p["post_id"] == selected_post_id)
    
    st.subheader("Post Details")
    st.write(f"**Platform:** {selected_post['platform']}")
    st.write(f"**Topic:** {selected_post['topic']}")
    st.write(f"**Format:** {selected_post['format']}")
    st.write(f"**Date:** {selected_post['timestamp'][:10]}")
    
    st.markdown("---")
    
    analyze_button = st.button("🔍 Analyze Post", type="primary", use_container_width=True)

# Main content
if analyze_button:
    try:
        with st.spinner("Analyzing post performance..."):
            # Create PostMetrics
            post_metrics = PostMetrics(**selected_post)
            
            # Create all posts data as text
            all_posts_text = json.dumps(DUMMY_POSTS, indent=2)
            
            # Execute pipeline
            async def run_analysis():
                return await execute_pipeline(
                    pipe_code="campaign_analytics",
                    inputs={
                        "post": {
                            "concept": "social_media_analysis.PostMetrics",
                            "content": post_metrics,
                        },
                        "all_posts": all_posts_text,  # Pass text directly
                    },
                )
            
            pipe_output = asyncio.run(run_analysis())
            
            # Extract analysis
            analysis: AnalysisOutput = pipe_output.main_stuff_as(content_type=AnalysisOutput)
        
        # Display results
        st.success("✅ Analysis Complete!")
            
        # KPIs Section
        st.markdown("## 📈 Key Performance Indicators")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Engagement Rate", f"{analysis.post_kpis.engagement_rate:.2f}%")
        
        with col2:
            st.metric("Click-Through Rate", f"{analysis.post_kpis.click_through_rate:.2f}%")
        
        with col3:
            st.metric("Comment Rate", f"{analysis.post_kpis.comment_rate:.2f}%")
        
        with col4:
            st.metric("Share Rate", f"{analysis.post_kpis.share_rate:.2f}%")
        
        # Baselines Section
        st.markdown("---")
        st.markdown("## 🎯 Benchmark Comparison")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Platform Baselines")
            st.metric(
                "Platform Avg Engagement",
                f"{analysis.platform_baselines.platform_avg_engagement:.2f}%",
                delta=f"{analysis.post_kpis.engagement_rate - analysis.platform_baselines.platform_avg_engagement:.2f}%"
            )
            st.metric(
                "Platform Avg CTR",
                f"{analysis.platform_baselines.platform_avg_ctr:.2f}%",
                delta=f"{analysis.post_kpis.click_through_rate - analysis.platform_baselines.platform_avg_ctr:.2f}%"
            )
        
        with col2:
            st.markdown("### Cohort Baselines")
            st.markdown(f"*Same platform, topic, and format*")
            st.metric(
                "Cohort Avg Engagement",
                f"{analysis.platform_baselines.cohort_avg_engagement:.2f}%",
                delta=f"{analysis.post_kpis.engagement_rate - analysis.platform_baselines.cohort_avg_engagement:.2f}%"
            )
            st.metric(
                "Cohort Avg CTR",
                f"{analysis.platform_baselines.cohort_avg_ctr:.2f}%",
                delta=f"{analysis.post_kpis.click_through_rate - analysis.platform_baselines.cohort_avg_ctr:.2f}%"
            )
        
        # Diagnostics Section
        st.markdown("---")
        st.markdown("## 🔍 Performance Diagnostics")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### ✅ Strengths")
            for strength in analysis.diagnostics.strengths:
                st.markdown(f"- <span class='strength'>{strength}</span>", unsafe_allow_html=True)
        
        with col2:
            st.markdown("### ⚠️ Areas for Improvement")
            for weakness in analysis.diagnostics.weaknesses:
                st.markdown(f"- <span class='weakness'>{weakness}</span>", unsafe_allow_html=True)
        
        # Recommendations Section
        st.markdown("---")
        st.markdown("## 💡 Recommendations")
        
        for idx, rec in enumerate(analysis.recommendations, 1):
            with st.expander(f"📌 {rec.category.title()}", expanded=(idx == 1)):
                st.markdown(rec.suggestion)
        
        # Executive Summary
        st.markdown("---")
        st.markdown("## 📋 Executive Summary")
        st.markdown(analysis.summary_md)
        
    except Exception as e:
        st.error(f"❌ Error analyzing post: {str(e)}")
        st.exception(e)

else:
    # Welcome message
    st.info("""
    ### 👋 Welcome to Post Analysis!
    
    This tool analyzes your social media posts and provides:
    - 📈 Detailed KPI calculations
    - 🎯 Benchmark comparisons
    - 🔍 Performance diagnostics
    - 💡 Actionable recommendations
    
    **Get Started:**
    1. Select a post from the sidebar
    2. Click "Analyze Post"
    3. Review the insights and recommendations
    """)
    
    # Show sample data
    st.markdown("### 📊 Available Posts")
    
    for post in DUMMY_POSTS:
        with st.expander(f"{post['post_id']} - {post['platform']} ({post['topic']})"):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Likes", post['likes'])
                st.metric("Comments", post['comments'])
            
            with col2:
                st.metric("Shares", post['shares'])
                st.metric("Impressions", post['impressions'])
            
            with col3:
                st.metric("Clicks", post['clicks'])
                st.metric("Saves", post['saves'])
