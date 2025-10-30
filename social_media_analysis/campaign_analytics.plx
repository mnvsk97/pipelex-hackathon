domain = "social_media_analysis"
description = "Campaign analytics pipeline for social media posts"

[concept]
PostMetrics = "Social media post metrics with engagement data"
PostKPIs = "Calculated KPIs for a post"
Baselines = "Baseline metrics for comparison"
Diagnostics = "Performance diagnostics with strengths and weaknesses"
Recommendation = "Individual recommendation for improvement"
AnalysisOutput = "Complete analysis output with KPIs, baselines, diagnostics, and recommendations"
AllPostsData = "Collection of all posts data for baseline calculations"

[pipe.calculate_kpis]
type = "PipeLLM"
description = "Calculate KPIs from post metrics"
inputs = { post = "PostMetrics" }
output = "PostKPIs"
model = { model = "gpt-4o-mini", temperature = 0.1, max_tokens = 500 }
prompt = """
Calculate KPIs for this social media post:

@post

Calculate:
1. Engagement rate = ((likes + comments + shares + saves) / impressions) * 100
2. Click-through rate = (clicks / impressions) * 100 (if clicks > 0)
3. Save rate = (saves / impressions) * 100 (if saves > 0)
4. Comment rate = (comments / impressions) * 100
5. Share rate = (shares / impressions) * 100

Return the calculated KPIs. Handle missing fields gracefully (use 0 if not present).
"""

[pipe.calculate_baselines]
type = "PipeLLM"
description = "Calculate platform and cohort baselines"
inputs = { post = "PostMetrics", all_posts = "AllPostsData" }
output = "Baselines"
model = { model = "gpt-4o-mini", temperature = 0.1, max_tokens = 800 }
prompt = """
Calculate baseline metrics for comparison:

Current post:
@post

All posts data:
@all_posts

Calculate:
1. Platform average engagement rate (all posts on same platform)
2. Cohort average engagement rate (same platform + topic + format)
3. Platform average CTR (if clicks data available)
4. Cohort average CTR (if clicks data available)

Return the baseline metrics.
"""

[pipe.diagnose_performance]
type = "PipeLLM"
description = "Diagnose post performance strengths and weaknesses"
inputs = { post = "PostMetrics", kpis = "PostKPIs", baselines = "Baselines" }
output = "Diagnostics"
model = { model = "gpt-4o-mini", temperature = 0.7, max_tokens = 800 }
prompt = """
Analyze this post's performance:

Post details:
@post

KPIs:
@kpis

Baselines:
@baselines

Identify:
1. Strengths: What metrics are performing above baseline? (3-5 points)
2. Weaknesses: What metrics are underperforming? (3-5 points)

Be specific and actionable.
"""

[pipe.generate_recommendations]
type = "PipeLLM"
description = "Generate tailored recommendations"
inputs = { post = "PostMetrics", diagnostics = "Diagnostics" }
output = "Recommendation[]"
model = { model = "gpt-4o-mini", temperature = 0.8, max_tokens = 1200 }
prompt = """
Generate 4-5 actionable recommendations for this post:

Post details:
@post

Diagnostics:
@diagnostics

Create recommendations in these categories:
1. Caption tweak
2. Hashtag strategy
3. Visual style/prompt
4. Call-to-action (CTA)
5. Posting time window

Each recommendation should be specific, actionable, and tailored to the platform ($post.platform) and format ($post.format).
"""

[pipe.create_summary]
type = "PipeLLM"
description = "Create executive summary"
inputs = { post = "PostMetrics", kpis = "PostKPIs", diagnostics = "Diagnostics" }
output = "Text"
model = { model = "gpt-4o-mini", temperature = 0.7, max_tokens = 600 }
prompt = """
Create a concise executive summary (3-4 paragraphs) for this post analysis:

Post: $post.post_id on $post.platform
Topic: $post.topic
Format: $post.format

KPIs:
@kpis

Diagnostics:
@diagnostics

Write in markdown format. Include:
1. Overall performance assessment
2. Key strengths
3. Main areas for improvement
4. Strategic recommendation

Keep it professional and actionable.
"""

[pipe.combine_analysis]
type = "PipeLLM"
description = "Combine all analysis components into final output"
inputs = { kpis = "PostKPIs", baselines = "Baselines", diagnostics = "Diagnostics", recommendations = "Recommendation[]", summary = "Text" }
output = "AnalysisOutput"
model = { model = "gpt-4o-mini", temperature = 0.1, max_tokens = 1000 }
prompt = """
Combine the analysis components into the final output:

KPIs:
@kpis

Baselines:
@baselines

Diagnostics:
@diagnostics

Recommendations:
@recommendations

Summary:
@summary

Return the complete analysis output with all components.
"""

[pipe.campaign_analytics]
type = "PipeSequence"
description = "Main analytics pipeline"
inputs = { post = "PostMetrics", all_posts = "AllPostsData" }
output = "AnalysisOutput"
steps = [{ pipe = "calculate_kpis", result = "kpis" }, { pipe = "calculate_baselines", result = "baselines" }, { pipe = "diagnose_performance", result = "diagnostics" }, { pipe = "generate_recommendations", result = "recommendations" }, { pipe = "create_summary", result = "summary" }, { pipe = "combine_analysis", result = "analysis" }]
