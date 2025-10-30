# Multi-Page Streamlit App - Social Media Suite

## Overview

The application has been converted to a multi-page Streamlit app with two main features:

1. **Content Generation** - AI-powered social media content creation
2. **Post Analysis** - Campaign analytics with KPIs and recommendations

## Structure

```
pipelex-hackathon/
├── app.py                          # Home page (landing page)
├── pages/
│   ├── 1_📝_Content_Generation.py  # Content generation page
│   └── 2_📊_Post_Analysis.py       # Post analysis page
├── social_content/                 # Content generation pipeline
│   ├── social_content.plx
│   ├── social_content_struct.py
│   └── __init__.py
└── social_media_analysis/          # Analytics pipeline (NEW)
    ├── campaign_analytics.plx
    ├── analytics_struct.py
    └── __init__.py
```

## Running the App

```bash
# Activate virtual environment
source .venv/bin/activate

# Run the app
streamlit run app.py
```

The app will open at `http://localhost:8501`

## Features

### Page 1: Content Generation 📝

- **Competitor Research**: AI-powered analysis of top 5 competitors
- **Multi-Platform Content**: Generate content for Instagram, Twitter, and LinkedIn
- **AI Image Generation**: Automatic image generation using Replicate
- **Brand Voice**: Customizable tone and style
- **Multiple Variations**: 3 variations for Instagram and LinkedIn

### Page 2: Post Analysis 📊

- **KPI Calculations**: Engagement rate, CTR, comment rate, share rate
- **Benchmark Comparisons**: Platform and cohort baselines
- **Performance Diagnostics**: Strengths and weaknesses analysis
- **AI Recommendations**: 4-5 tailored suggestions for improvement
- **Executive Summary**: Markdown-formatted summary report

## New Pipeline: Campaign Analytics

### Location
`social_media_analysis/campaign_analytics.plx`

### Features
- Ingests JSON data with social metrics
- Calculates KPIs (engagement rate, CTR, save/comment/share rates)
- Benchmarks against platform and cohort baselines
- Diagnoses performance strengths and weaknesses
- Generates tailored recommendations
- Creates executive summary

### Data Structure

**Input: PostMetrics**
```python
{
    "post_id": str,
    "platform": str,  # Twitter, Instagram, LinkedIn
    "topic": str,
    "format": str,    # image, video, text, carousel
    "timestamp": str,
    "likes": int,
    "comments": int,
    "shares": int,
    "impressions": int,
    "clicks": int,
    "saves": int
}
```

**Output: AnalysisOutput**
```python
{
    "post_kpis": PostKPIs,
    "platform_baselines": Baselines,
    "diagnostics": Diagnostics,
    "recommendations": List[Recommendation],
    "summary_md": str
}
```

## Dummy Data

The Post Analysis page includes 5 sample posts:
- 2 Instagram posts (AI Technology, Product Launch)
- 2 Twitter posts (AI Technology, Product Launch)
- 1 LinkedIn post (AI Technology)

## Pipeline Validation

Both pipelines have been validated:

```bash
# Validate content generation pipeline
pipelex validate social_content/social_content.plx

# Validate analytics pipeline
pipelex validate social_media_analysis/campaign_analytics.plx
```

## Navigation

Use the sidebar to navigate between pages:
- **Home** - Overview and getting started
- **📝 Content Generation** - Create new content
- **📊 Post Analysis** - Analyze existing posts

## Technologies Used

- **Streamlit**: Multi-page web application framework
- **Pipelex**: AI pipeline orchestration
- **OpenAI GPT-4o-mini**: LLM for content generation and analysis
- **Replicate**: AI image generation (Seedream-4)
- **Pydantic**: Data validation and structured outputs

## Next Steps

Potential enhancements:
1. Add file upload for custom post data (CSV/JSON)
2. Integrate Tavily web search for best practices
3. Add export functionality (PDF reports)
4. Implement batch analysis for multiple posts
5. Add visualization charts for KPIs
6. Connect to real social media APIs

## Notes

- The app uses dummy data for the Post Analysis feature
- Image generation requires a valid Replicate API token
- All pipelines use GPT-4o-mini for cost efficiency
- The analytics pipeline handles missing fields gracefully
