"""Example: Running the campaign analytics pipeline."""

import asyncio
import json
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from pipelex import pretty_print
from pipelex.pipelex import Pipelex
from pipelex.pipeline.execute import execute_pipeline
from pipelex.core.stuffs.text_content import TextContent
from social_media_analysis.analytics_struct import PostMetrics, AnalysisOutput

# Sample post data
SAMPLE_POST = {
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
}

# All posts for baseline calculation
ALL_POSTS = [
    SAMPLE_POST,
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
]


async def analyze_post() -> AnalysisOutput:
    """
    Analyze a social media post and get KPIs, benchmarks, and recommendations.
    """
    # Create PostMetrics
    post_metrics = PostMetrics(**SAMPLE_POST)
    
    # Create all posts data as text
    all_posts_text = json.dumps(ALL_POSTS, indent=2)
    
    # Run the analytics pipeline
    pipe_output = await execute_pipeline(
        pipe_code="campaign_analytics",
        inputs={
            "post": {
                "concept": "social_media_analysis.PostMetrics",
                "content": post_metrics,
            },
            "all_posts": all_posts_text,  # Pass text directly
        },
    )
    
    # Extract the analysis output
    return pipe_output.main_stuff_as(content_type=AnalysisOutput)


# Start Pipelex
Pipelex.make()

# Run the analysis
print("🔍 Analyzing post performance...\n")
analysis = asyncio.run(analyze_post())

# Display results
print("=" * 80)
print("📊 POST ANALYSIS RESULTS")
print("=" * 80)

print(f"\n📈 KPIs for {SAMPLE_POST['post_id']}:")
print(f"  • Engagement Rate: {analysis.post_kpis.engagement_rate:.2f}%")
print(f"  • Click-Through Rate: {analysis.post_kpis.click_through_rate:.2f}%")
print(f"  • Comment Rate: {analysis.post_kpis.comment_rate:.2f}%")
print(f"  • Share Rate: {analysis.post_kpis.share_rate:.2f}%")
print(f"  • Save Rate: {analysis.post_kpis.save_rate:.2f}%")

print(f"\n🎯 Benchmarks:")
print(f"  Platform Avg Engagement: {analysis.platform_baselines.platform_avg_engagement:.2f}%")
print(f"  Cohort Avg Engagement: {analysis.platform_baselines.cohort_avg_engagement:.2f}%")

print(f"\n✅ Strengths:")
for strength in analysis.diagnostics.strengths:
    print(f"  • {strength}")

print(f"\n⚠️ Weaknesses:")
for weakness in analysis.diagnostics.weaknesses:
    print(f"  • {weakness}")

print(f"\n💡 Recommendations:")
for rec in analysis.recommendations:
    print(f"  • [{rec.category.upper()}] {rec.suggestion}")

print(f"\n📋 Executive Summary:")
print(analysis.summary_md)

print("\n" + "=" * 80)
print("✅ Analysis complete!")
print("=" * 80)
