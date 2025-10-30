"""Multi-page Streamlit app for Social Media Content Generator."""

import streamlit as st

st.set_page_config(
    page_title="Social Media Suite",
    page_icon="🚀",
    layout="wide",
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
    }
    .feature-card {
        background-color: rgba(240, 242, 246, 0.1);
        border: 1px solid rgba(128, 128, 128, 0.3);
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        color: inherit;
    }
    .feature-card h3 {
        color: #1f77b4;
        margin-bottom: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# Title
st.markdown('<div class="main-header">🚀 Social Media Suite</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">AI-Powered Content Generation & Analytics</div>', unsafe_allow_html=True)

# Introduction
st.markdown("""
Welcome to the Social Media Suite! This powerful tool helps you create and analyze social media content across multiple platforms.
""")

# Features
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="feature-card">
        <h3>📝 Content Generation</h3>
        <p>Create professional social media content with AI:</p>
        <ul>
            <li>🔍 Competitor research & analysis</li>
            <li>📸 Instagram posts (3 variations)</li>
            <li>🐦 Twitter/X optimized posts</li>
            <li>💼 LinkedIn professional content</li>
            <li>🎨 AI-generated images</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card">
        <h3>📊 Post Analysis</h3>
        <p>Analyze your social media performance:</p>
        <ul>
            <li>📈 KPI calculations & metrics</li>
            <li>🎯 Benchmark comparisons</li>
            <li>💡 Performance diagnostics</li>
            <li>✨ AI-powered recommendations</li>
            <li>📋 Executive summaries</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# Getting Started
st.markdown("---")
st.markdown("## 🚀 Getting Started")

st.markdown("""
Choose a page from the sidebar to get started:

1. **Content Generation** - Create new social media content with AI assistance
2. **Post Analysis** - Analyze existing posts and get actionable insights

Each tool is powered by advanced AI pipelines built with Pipelex.
""")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 2rem;">
    Built with ❤️ using Streamlit & Pipelex
</div>
""", unsafe_allow_html=True)
