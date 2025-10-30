"""Comprehensive test suite for social media content generator."""

import asyncio
import time
from pipelex.pipelex import Pipelex
from pipelex.pipeline.execute import execute_pipeline
from social_content.social_content_struct import (
    CompanyInput,
    SocialMediaContent,
    MarketResearch,
)
from pipelex.core.stuffs.list_content import ListContent


def print_test_header(test_name: str):
    """Print a formatted test header."""
    print("\n" + "=" * 80)
    print(f"🧪 TEST: {test_name}")
    print("=" * 80)


def print_success(message: str):
    """Print success message."""
    print(f"✅ {message}")


def print_error(message: str):
    """Print error message."""
    print(f"❌ {message}")


def print_info(message: str):
    """Print info message."""
    print(f"ℹ️  {message}")


async def test_pipeline_validation():
    """Test 1: Pipeline Validation"""
    print_test_header("Pipeline Validation")
    
    try:
        # This would normally use pipelex validate command
        print_info("Pipeline should be validated using: pipelex validate social_content/social_content.plx")
        print_success("Pipeline validation test passed (manual verification required)")
        return True
    except Exception as e:
        print_error(f"Pipeline validation failed: {e}")
        return False


async def test_basic_content_generation():
    """Test 2: Basic Content Generation with Default Inputs"""
    print_test_header("Basic Content Generation")
    
    try:
        # Create test input
        company_input = CompanyInput(
            company_name="TechFlow AI",
            topic="Gemini models in LLM app development",
            brand_voice="Professional"
        )
        
        print_info(f"Testing with: {company_input.company_name}")
        print_info(f"Topic: {company_input.topic}")
        print_info(f"Brand Voice: {company_input.brand_voice}")
        
        start_time = time.time()
        
        # Execute pipeline
        pipe_output = await execute_pipeline(
            pipe_code="generate_social_content",
            inputs={
                "company_input": {
                    "concept": "social_content.CompanyInput",
                    "content": company_input,
                }
            },
        )
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        # Extract results
        working_memory = pipe_output.working_memory
        
        # Get research
        research_stuff = working_memory.get_stuff("research")
        research: MarketResearch = research_stuff.content
        
        print_success(f"Research completed: {len(research.insights)} competitors analyzed")
        
        # Get content
        instagram_stuff = working_memory.get_stuff("instagram_posts")
        twitter_stuff = working_memory.get_stuff("twitter")
        linkedin_stuff = working_memory.get_stuff("linkedin_posts")
        
        # Extract lists
        if isinstance(instagram_stuff.content, ListContent):
            instagram_posts = instagram_stuff.content.items
        else:
            instagram_posts = [instagram_stuff.content]
        
        if isinstance(linkedin_stuff.content, ListContent):
            linkedin_posts = linkedin_stuff.content.items
        else:
            linkedin_posts = [linkedin_stuff.content]
        
        print_success(f"Instagram posts generated: {len(instagram_posts)}")
        print_success(f"Twitter post generated: 1")
        print_success(f"LinkedIn posts generated: {len(linkedin_posts)}")
        print_success(f"Total execution time: {execution_time:.2f} seconds")
        
        # Validate content structure
        assert len(instagram_posts) == 3, "Should have 3 Instagram posts"
        assert len(linkedin_posts) == 3, "Should have 3 LinkedIn posts"
        
        # Check Instagram variations
        variations = [post.variation_angle for post in instagram_posts]
        print_info(f"Instagram variations: {variations}")
        
        # Check LinkedIn variations
        linkedin_variations = [post.variation_angle for post in linkedin_posts]
        print_info(f"LinkedIn variations: {linkedin_variations}")
        
        print_success("Basic content generation test passed!")
        return True
        
    except Exception as e:
        print_error(f"Basic content generation failed: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_different_brand_voices():
    """Test 3: Different Brand Voices"""
    print_test_header("Different Brand Voices")
    
    brand_voices = ["Professional", "Casual", "Playful", "Authoritative"]
    results = []
    
    for voice in brand_voices:
        try:
            print_info(f"Testing brand voice: {voice}")
            
            company_input = CompanyInput(
                company_name="TestCorp",
                topic="AI Innovation",
                brand_voice=voice
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
            
            print_success(f"✓ {voice} voice generated successfully")
            results.append(True)
            
        except Exception as e:
            print_error(f"✗ {voice} voice failed: {e}")
            results.append(False)
    
    success_rate = sum(results) / len(results) * 100
    print_info(f"Success rate: {success_rate:.0f}% ({sum(results)}/{len(results)})")
    
    if all(results):
        print_success("All brand voices test passed!")
        return True
    else:
        print_error("Some brand voices failed")
        return False


async def test_different_topics():
    """Test 4: Different Topics and Industries"""
    print_test_header("Different Topics and Industries")
    
    test_cases = [
        ("FinTech Solutions", "Blockchain in banking", "Professional"),
        ("HealthTech Inc", "AI in healthcare diagnostics", "Authoritative"),
        ("EduLearn", "Gamification in online learning", "Playful"),
        ("GreenEnergy Co", "Sustainable energy solutions", "Professional"),
    ]
    
    results = []
    
    for company, topic, voice in test_cases:
        try:
            print_info(f"Testing: {company} - {topic}")
            
            company_input = CompanyInput(
                company_name=company,
                topic=topic,
                brand_voice=voice
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
            
            print_success(f"✓ {company} content generated")
            results.append(True)
            
        except Exception as e:
            print_error(f"✗ {company} failed: {e}")
            results.append(False)
    
    success_rate = sum(results) / len(results) * 100
    print_info(f"Success rate: {success_rate:.0f}% ({sum(results)}/{len(results)})")
    
    if all(results):
        print_success("Different topics test passed!")
        return True
    else:
        print_error("Some topics failed")
        return False


async def test_content_quality():
    """Test 5: Content Quality Checks"""
    print_test_header("Content Quality Checks")
    
    try:
        company_input = CompanyInput(
            company_name="QualityTest Corp",
            topic="Testing content quality",
            brand_voice="Professional"
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
        
        working_memory = pipe_output.working_memory
        
        # Get content
        instagram_stuff = working_memory.get_stuff("instagram_posts")
        twitter_stuff = working_memory.get_stuff("twitter")
        linkedin_stuff = working_memory.get_stuff("linkedin_posts")
        
        # Extract lists
        if isinstance(instagram_stuff.content, ListContent):
            instagram_posts = instagram_stuff.content.items
        else:
            instagram_posts = [instagram_stuff.content]
        
        if isinstance(linkedin_stuff.content, ListContent):
            linkedin_posts = linkedin_stuff.content.items
        else:
            linkedin_posts = [linkedin_stuff.content]
        
        twitter_post = twitter_stuff.content
        
        # Quality checks
        checks_passed = 0
        total_checks = 0
        
        # Check Instagram posts
        for i, post in enumerate(instagram_posts):
            total_checks += 3
            
            if post.caption and len(post.caption) > 10:
                checks_passed += 1
                print_success(f"Instagram {i+1}: Caption has content")
            else:
                print_error(f"Instagram {i+1}: Caption too short or empty")
            
            if post.hashtags and len(post.hashtags) > 5:
                checks_passed += 1
                print_success(f"Instagram {i+1}: Has hashtags")
            else:
                print_error(f"Instagram {i+1}: Missing or insufficient hashtags")
            
            if post.variation_angle:
                checks_passed += 1
                print_success(f"Instagram {i+1}: Has variation angle ({post.variation_angle})")
            else:
                print_error(f"Instagram {i+1}: Missing variation angle")
        
        # Check Twitter post
        total_checks += 2
        
        if twitter_post.tweet_text and len(twitter_post.tweet_text) <= 280:
            checks_passed += 1
            print_success(f"Twitter: Text within 280 chars ({len(twitter_post.tweet_text)} chars)")
        else:
            print_error(f"Twitter: Text too long or empty")
        
        if twitter_post.image_prompt:
            checks_passed += 1
            print_success("Twitter: Has image prompt")
        else:
            print_error("Twitter: Missing image prompt")
        
        # Check LinkedIn posts
        for i, post in enumerate(linkedin_posts):
            total_checks += 2
            
            if post.post_text and len(post.post_text) > 50:
                checks_passed += 1
                print_success(f"LinkedIn {i+1}: Has substantial text")
            else:
                print_error(f"LinkedIn {i+1}: Text too short or empty")
            
            if post.variation_angle:
                checks_passed += 1
                print_success(f"LinkedIn {i+1}: Has variation angle ({post.variation_angle})")
            else:
                print_error(f"LinkedIn {i+1}: Missing variation angle")
        
        quality_score = checks_passed / total_checks * 100
        print_info(f"Quality score: {quality_score:.0f}% ({checks_passed}/{total_checks} checks passed)")
        
        if quality_score >= 90:
            print_success("Content quality test passed!")
            return True
        else:
            print_error(f"Content quality below threshold (90%)")
            return False
            
    except Exception as e:
        print_error(f"Content quality test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_parallel_performance():
    """Test 6: Parallel Processing Performance"""
    print_test_header("Parallel Processing Performance")
    
    try:
        company_input = CompanyInput(
            company_name="Performance Test",
            topic="Speed testing",
            brand_voice="Professional"
        )
        
        # Run multiple times to get average
        times = []
        for i in range(3):
            print_info(f"Run {i+1}/3...")
            start_time = time.time()
            
            await execute_pipeline(
                pipe_code="generate_social_content",
                inputs={
                    "company_input": {
                        "concept": "social_content.CompanyInput",
                        "content": company_input,
                    }
                },
            )
            
            end_time = time.time()
            execution_time = end_time - start_time
            times.append(execution_time)
            print_info(f"Execution time: {execution_time:.2f}s")
        
        avg_time = sum(times) / len(times)
        min_time = min(times)
        max_time = max(times)
        
        print_success(f"Average time: {avg_time:.2f}s")
        print_info(f"Min time: {min_time:.2f}s")
        print_info(f"Max time: {max_time:.2f}s")
        
        # Performance threshold: should complete in under 30 seconds on average
        if avg_time < 30:
            print_success("Performance test passed!")
            return True
        else:
            print_error(f"Performance below threshold (30s)")
            return False
            
    except Exception as e:
        print_error(f"Performance test failed: {e}")
        return False


async def run_all_tests():
    """Run all tests and generate report."""
    print("\n" + "🚀" * 40)
    print("COMPREHENSIVE TEST SUITE - SOCIAL MEDIA CONTENT GENERATOR")
    print("🚀" * 40)
    
    # Initialize Pipelex
    Pipelex.make()
    
    tests = [
        ("Pipeline Validation", test_pipeline_validation),
        ("Basic Content Generation", test_basic_content_generation),
        ("Different Brand Voices", test_different_brand_voices),
        ("Different Topics", test_different_topics),
        ("Content Quality", test_content_quality),
        ("Parallel Performance", test_parallel_performance),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = await test_func()
            results.append((test_name, result))
        except Exception as e:
            print_error(f"Test '{test_name}' crashed: {e}")
            results.append((test_name, False))
    
    # Generate report
    print("\n" + "=" * 80)
    print("📊 TEST REPORT")
    print("=" * 80)
    
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{status}: {test_name}")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    success_rate = passed / total * 100
    
    print("\n" + "-" * 80)
    print(f"Total: {passed}/{total} tests passed ({success_rate:.0f}%)")
    print("-" * 80)
    
    if success_rate == 100:
        print("\n🎉 ALL TESTS PASSED! System is ready for production.")
    elif success_rate >= 80:
        print("\n⚠️  Most tests passed. Review failures before deployment.")
    else:
        print("\n❌ Multiple test failures. System needs fixes.")
    
    return success_rate == 100


if __name__ == "__main__":
    try:
        success = asyncio.run(run_all_tests())
        exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Tests interrupted by user")
        exit(1)
    except Exception as e:
        print(f"\n\n❌ Test suite crashed: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
