"""Structured content models for social media analytics."""

from pipelex.core.stuffs.structured_content import StructuredContent
from pydantic import Field


class PostMetrics(StructuredContent):
    """Social media post metrics."""
    
    post_id: str = Field(description="Unique post identifier")
    platform: str = Field(description="Social media platform (Twitter, Instagram, LinkedIn)")
    topic: str = Field(description="Content topic/category")
    format: str = Field(description="Content format (image, video, text, carousel)")
    timestamp: str = Field(description="Post timestamp")
    likes: int = Field(description="Number of likes")
    comments: int = Field(description="Number of comments")
    shares: int = Field(description="Number of shares")
    impressions: int = Field(description="Number of impressions")
    clicks: int = Field(description="Number of clicks", default=0)
    saves: int = Field(description="Number of saves", default=0)


class PostKPIs(StructuredContent):
    """Calculated KPIs for a post."""
    
    engagement_rate: float = Field(description="Engagement rate percentage")
    click_through_rate: float = Field(description="Click-through rate percentage", default=0.0)
    save_rate: float = Field(description="Save rate percentage", default=0.0)
    comment_rate: float = Field(description="Comment rate percentage")
    share_rate: float = Field(description="Share rate percentage")


class Baselines(StructuredContent):
    """Baseline metrics for comparison."""
    
    platform_avg_engagement: float = Field(description="Platform average engagement rate")
    cohort_avg_engagement: float = Field(description="Cohort average engagement rate")
    platform_avg_ctr: float = Field(description="Platform average CTR", default=0.0)
    cohort_avg_ctr: float = Field(description="Cohort average CTR", default=0.0)


class Diagnostics(StructuredContent):
    """Performance diagnostics."""
    
    strengths: list[str] = Field(description="List of performance strengths")
    weaknesses: list[str] = Field(description="List of performance weaknesses")


class Recommendation(StructuredContent):
    """Individual recommendation."""
    
    category: str = Field(description="Recommendation category (caption, hashtags, visual, CTA, timing)")
    suggestion: str = Field(description="Specific actionable suggestion")


class AnalysisOutput(StructuredContent):
    """Complete analysis output."""
    
    post_kpis: PostKPIs = Field(description="Calculated KPIs")
    platform_baselines: Baselines = Field(description="Platform and cohort baselines")
    diagnostics: Diagnostics = Field(description="Strengths and weaknesses")
    recommendations: list[Recommendation] = Field(description="Tailored recommendations")
    summary_md: str = Field(description="Executive summary in markdown")
