"""Structured content models for social media generation."""

from pipelex.core.stuffs.structured_content import StructuredContent
from pydantic import Field


class CompanyInput(StructuredContent):
    """Company and topic information for content generation."""
    
    company_name: str = Field(description="Name of the company")
    topic: str = Field(description="Topic for the social media content")
    brand_voice: str = Field(description="Brand voice (e.g., professional, casual, playful)")


class CompetitorInsight(StructuredContent):
    """Insights from competitor analysis."""
    
    competitor_name: str = Field(description="Name of the competitor")
    content_style: str = Field(description="Their content style and approach")
    engagement_tactics: str = Field(description="What makes their content engaging")


class MarketResearch(StructuredContent):
    """Aggregated market research from competitors."""
    
    insights: list[CompetitorInsight] = Field(description="List of competitor insights")
    key_trends: str = Field(description="Key trends identified across competitors")
    recommendations: str = Field(description="Recommendations for content strategy")


class InstagramPost(StructuredContent):
    """Instagram post with image prompt and caption."""
    
    image_prompt: str = Field(description="Detailed prompt for image generation")
    caption: str = Field(description="Instagram caption text")
    hashtags: str = Field(description="Relevant hashtags (space-separated)")
    variation_angle: str = Field(description="The unique angle or approach of this variation")


class TwitterPost(StructuredContent):
    """Twitter/X post with image prompt and short text."""
    
    image_prompt: str = Field(description="Detailed prompt for image generation")
    tweet_text: str = Field(description="Tweet text (max 280 characters)")


class LinkedInPost(StructuredContent):
    """LinkedIn post with professional content."""
    
    post_text: str = Field(description="Professional LinkedIn post text (500-1000 characters)")
    image_prompt: str = Field(description="Detailed prompt for image generation", default="")
    variation_angle: str = Field(description="The unique angle or approach of this variation")


class SocialMediaContent(StructuredContent):
    """Complete social media content package."""
    
    instagram: list[InstagramPost] = Field(description="Instagram post variations (3 versions)")
    twitter: TwitterPost = Field(description="Twitter post content")
    linkedin: list[LinkedInPost] = Field(description="LinkedIn post variations (3 versions)")
