domain = "social_content"
description = "Simple social media content generation pipeline"

[concept]
CompanyInput = "Company information and content topic"
MarketResearch = "Competitor analysis and market insights"
InstagramPost = "Instagram post with image prompt and caption"
TwitterPost = "Twitter post with image prompt and text"
LinkedInPost = "LinkedIn post with professional content"
SocialMediaContent = "Complete social media content package"

[pipe.research_competitors]
type = "PipeLLM"
description = "Research top 5 competitors and their social media approach"
inputs = { company_input = "CompanyInput" }
output = "MarketResearch"
model = { model = "gpt-4o-mini", temperature = 0.7, max_tokens = 1500 }
prompt = """
You are a social media marketing analyst. Research and analyze the top 5 competitors for $company_input.company_name in their industry.

Topic focus: $company_input.topic
Brand voice: $company_input.brand_voice

For each competitor, identify:
1. Their content style and approach
2. What makes their content engaging
3. Common themes and tactics

Then provide:
- Key trends across all competitors
- Recommendations for creating similar but unique content

Be specific and actionable.
"""

[pipe.generate_instagram]
type = "PipeLLM"
description = "Generate 3 Instagram post variations"
inputs = { company_input = "CompanyInput", research = "MarketResearch" }
output = "InstagramPost[3]"
model = { model = "gpt-4o-mini", temperature = 0.9, max_tokens = 1500 }
prompt = """
Create 3 different Instagram post variations for $company_input.company_name about: $company_input.topic

Brand voice: $company_input.brand_voice

Based on this market research:
@research

For EACH of the 3 variations, generate:
1. A unique angle/approach (e.g., educational, inspirational, behind-the-scenes)
2. A detailed image prompt (describe the visual in detail - style, colors, mood, composition)
3. An engaging caption (2-3 sentences, use the brand voice)
4. Relevant hashtags (8-12 hashtags, space-separated)

Make each variation distinct with different angles and approaches.
The first 2 variations should have image prompts for visual content.
The 3rd variation should be text-only (simple image prompt or none).
"""

[pipe.generate_twitter]
type = "PipeLLM"
description = "Generate Twitter post with image prompt and short text"
inputs = { company_input = "CompanyInput", research = "MarketResearch" }
output = "TwitterPost"
model = { model = "gpt-4o-mini", temperature = 0.9, max_tokens = 600 }
prompt = """
Create a Twitter/X post for $company_input.company_name about: $company_input.topic

Brand voice: $company_input.brand_voice

Based on this market research:
@research

Generate:
1. A detailed image prompt (describe the visual in detail - style, colors, mood, composition)
2. Tweet text (max 280 characters, punchy and engaging, use the brand voice)

Make it concise, impactful, and aligned with successful competitor strategies.
"""

[pipe.generate_linkedin]
type = "PipeLLM"
description = "Generate 3 LinkedIn post variations"
inputs = { company_input = "CompanyInput", research = "MarketResearch" }
output = "LinkedInPost[3]"
model = { model = "gpt-4o-mini", temperature = 0.8, max_tokens = 2000 }
prompt = """
Create 3 different LinkedIn post variations for $company_input.company_name about: $company_input.topic

Brand voice: $company_input.brand_voice (but adapt to LinkedIn's professional tone)

Based on this market research:
@research

For EACH of the 3 variations, generate:
1. A unique angle/approach (e.g., thought leadership, industry insights, company culture)
2. Professional post text (500-1000 characters, engaging and informative)
3. An optional image prompt (for the first 2 variations only, describe professional visuals)

Make each variation distinct:
- Variation 1: Thought leadership with image
- Variation 2: Industry insights with image
- Variation 3: Engaging story, text-only (no image prompt)

Use professional language, include relevant insights, and encourage engagement.
"""

[pipe.combine_content]
type = "PipeLLM"
description = "Combine all social media posts into final package"
inputs = { instagram_posts = "InstagramPost[]", twitter = "TwitterPost", linkedin_posts = "LinkedInPost[]" }
output = "SocialMediaContent"
model = { model = "gpt-4o-mini", temperature = 0.1, max_tokens = 1000 }
prompt = """
Package the social media content:

Instagram (3 variations):
@instagram_posts

Twitter:
@twitter

LinkedIn (3 variations):
@linkedin_posts

Return the complete package with all posts.
"""

[pipe.generate_all_content]
type = "PipeParallel"
description = "Generate Instagram, Twitter, and LinkedIn content in parallel"
inputs = { company_input = "CompanyInput", research = "MarketResearch" }
output = "Text"
add_each_output = true
parallels = [{ pipe = "generate_instagram", result = "instagram_posts" }, { pipe = "generate_twitter", result = "twitter" }, { pipe = "generate_linkedin", result = "linkedin_posts" }]

[pipe.generate_social_content]
type = "PipeSequence"
description = "Main pipeline to generate social media content"
inputs = { company_input = "CompanyInput" }
output = "SocialMediaContent"
steps = [{ pipe = "research_competitors", result = "research" }, { pipe = "generate_all_content", result = "all_content" }, { pipe = "combine_content", result = "final_content" }]
