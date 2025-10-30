# 🚀 Social Media Content Generator

> AI-powered content creation platform built with Pipelex and Streamlit for hackathon

[![Pipelex](https://img.shields.io/badge/Pipelex-0.14.3-blue)](https://pipelex.ai)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.51.0-red)](https://streamlit.io)
[![Python](https://img.shields.io/badge/Python-3.12+-green)](https://python.org)

## 🎯 What It Does

Generate professional social media content across **Instagram**, **Twitter**, and **LinkedIn** in under 90 seconds:

- 📸 **Instagram**: 3 variations + 5 AI-generated images + optional voiceover
- 🐦 **Twitter**: Optimized 280-char posts with images
- 💼 **LinkedIn**: 3 professional variations with 2 AI-generated images

**Plus**: Automated competitor research and market insights!

## ✨ Key Features

- 🤖 **AI-Powered**: GPT-4o-mini for content, Replicate for images/audio
- ⚡ **Fast**: Parallel processing (60% faster than sequential)
- 🎨 **High-Quality Images**: bytedance/seedream-4 via Replicate
- 🎵 **Audio Generation**: minimax/speech-02-hd for voiceovers
- 🔍 **Market Research**: Automatic competitor analysis
- 🎯 **Platform-Optimized**: Content tailored for each platform
- 🌓 **Dark Mode**: Professional UI in any theme
- ✏️ **Editable**: Customize all generated content

## 🚀 Quick Start

### 1. Install Dependencies

```bash
# Using uv (recommended)
uv sync

# Or using pip
pip install -r requirements.txt
```

### 2. Set Up API Keys

Create a `.env` file:

```bash
REPLICATE_API_TOKEN=your_replicate_token
BLACKBOX_API_KEY=your_blackbox_key
```

Get your keys:
- Replicate: https://replicate.com/account/api-tokens
- BLACKBOX AI: https://www.blackbox.ai/

### 3. Run the App

```bash
streamlit run app_v3.py
```

### 4. Generate Content

1. Enter company name and topic
2. Select brand voice
3. Click "Generate Content"
4. Wait ~60-90 seconds
5. Review and copy your content!

## 📊 What You Get

### Instagram (3 Variations)
- **Educational**: Informative content with data
- **Visual Guide**: Step-by-step infographics
- **Inspirational**: Motivational messaging
- **5 AI Images**: Multiple style variations
- **Optional Audio**: Professional voiceover

### Twitter
- **Optimized Text**: Perfect 280-character posts
- **Engaging Copy**: Punchy and shareable
- **AI Image**: Professional visuals

### LinkedIn (3 Variations)
- **Thought Leadership**: Industry insights
- **Professional Analysis**: Data-driven content
- **Storytelling**: Engaging narratives
- **2 AI Images**: Professional graphics

## 🏗️ Architecture

```
┌─────────────────────────────────────────────┐
│           Streamlit UI (app_v3.py)          │
└─────────────────┬───────────────────────────┘
                  │
┌─────────────────▼───────────────────────────┐
│         Pipelex Pipeline Engine             │
│  ┌──────────────────────────────────────┐   │
│  │  1. Competitor Research (PipeLLM)    │   │
│  └──────────────┬───────────────────────┘   │
│                 │                            │
│  ┌──────────────▼───────────────────────┐   │
│  │  2. Parallel Content Gen (3 pipes)   │   │
│  │     • Instagram (PipeLLM)            │   │
│  │     • Twitter (PipeLLM)              │   │
│  │     • LinkedIn (PipeLLM)             │   │
│  └──────────────┬───────────────────────┘   │
│                 │                            │
│  ┌──────────────▼───────────────────────┐   │
│  │  3. Combine Content (PipeLLM)        │   │
│  └──────────────────────────────────────┘   │
└─────────────────┬───────────────────────────┘
                  │
┌─────────────────▼───────────────────────────┐
│      Replicate API (Post-Processing)        │
│  • Image Generation (bytedance/seedream-4)  │
│  • Audio Generation (minimax/speech-02-hd)  │
└─────────────────────────────────────────────┘
```

## 📁 Project Structure

```
pipelex-hackathon/
├── app_v3.py                    # Main Streamlit app ⭐
├── social_content/
│   ├── social_content.plx       # Pipeline definition
│   ├── social_content_struct.py # Data structures
│   └── replicate_functions.py   # Image/audio generation
├── examples/
│   └── run_social_content.py    # CLI example
├── test_app.py                  # Test suite
├── test_replicate.py            # Replicate setup test
├── .env                         # API keys (create this)
├── pyproject.toml               # Dependencies
└── Documentation/
    ├── HACKATHON_FINAL.md       # Complete documentation
    ├── QUICK_START.md           # Quick start guide
    └── TEST_REPORT.md           # Test results
```

## 🧪 Testing

Run the test suite:

```bash
python test_app.py
```

Test Replicate setup:

```bash
python test_replicate.py
```

## 📈 Performance

- **Content Generation**: ~30-40 seconds
- **Image Generation**: ~30-50 seconds (7 images)
- **Audio Generation**: ~10-15 seconds (optional)
- **Total**: ~60-90 seconds for complete package

**Parallel Processing**: 60% faster than sequential execution ⚡

## 🎨 Screenshots

### Main Interface
![Main UI](https://via.placeholder.com/800x400?text=Social+Media+Content+Generator)

### Generated Content
![Content Display](https://via.placeholder.com/800x400?text=Generated+Content+Display)

### Competitor Research
![Research](https://via.placeholder.com/800x400?text=Competitor+Research)

## 🔧 Configuration

### Brand Voices
- Professional
- Casual
- Playful
- Authoritative
- Friendly
- Inspirational

### Customization
Edit `social_content/social_content.plx` to:
- Adjust prompts
- Change LLM models
- Modify content structure
- Add new platforms

## 📚 Documentation

- **[HACKATHON_FINAL.md](HACKATHON_FINAL.md)**: Complete project documentation
- **[QUICK_START.md](QUICK_START.md)**: Step-by-step setup guide
- **[TEST_REPORT.md](TEST_REPORT.md)**: Test results and metrics
- **[DEMO.md](DEMO.md)**: Demo instructions

## 🤝 Contributing

This is a hackathon project, but contributions are welcome!

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📝 License

MIT License - feel free to use and modify!

## 🙏 Acknowledgments

- **Pipelex**: Amazing pipeline orchestration framework
- **Streamlit**: Rapid UI development
- **Replicate**: High-quality AI model hosting
- **BLACKBOX AI**: Powerful LLM capabilities

## 🐛 Known Issues

- Minor JSON parsing issue in performance tests (83% pass rate)
- Audio generation requires additional setup
- Image generation takes ~30-50 seconds

## 🚀 Future Enhancements

- [ ] Video generation for Instagram Reels
- [ ] Scheduling integration
- [ ] A/B testing suggestions
- [ ] Analytics dashboard
- [ ] Multi-language support

## 📞 Support

For questions or issues:
- Open a GitHub issue
- Check documentation in `/Documentation`
- Run `python test_replicate.py` for setup verification

---

**Built with ❤️ for the hackathon using Pipelex, Streamlit, and AI**

⭐ Star this repo if you find it useful!
