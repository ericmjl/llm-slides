# LLM Slides

A Python-based tool for creating and managing slide presentations using LLMs and Markdown, built with LlamaBot and Marimo.

## Features

- Create slides using natural language prompts
- Generate content with LLMs (via LlamaBot)
- Support for both Markdown and HTML content
- Interactive slide editing and preview
- Automatic slide deck management
- Semantic slide selection and editing
- Support for:
  - Tables (in HTML)
  - Two-column layouts
  - Mermaid diagrams
  - YouTube embeds
  - Images

## Development

### Requirements

- Python >= 3.13
- Dependencies:
  - anthropic==0.54.0
  - ipython==9.3.0
  - llamabot[all]==0.12.7
  - marimo
  - pydantic==2.11.5


### Interactive Development

For interactive development and experimentation, use Marimo:

```bash
uvx marimo edit --sandbox https://raw.githubusercontent.com/ericmjl/llm-slides/refs/heads/main/slides_maker.py
```

You can also clone the repo directly and edit the notebook:

```bash
uvx marimo edit --sandbox slides_maker.py
```

This opens an interactive notebook where you can:

- Create and edit slides using natural language
- Preview slide content in real-time
- Test different LLM prompts
- Debug and refine your presentation
