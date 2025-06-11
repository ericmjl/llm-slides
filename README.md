# LLM Slides

A command-line tool for creating and managing slide presentations using LLMs and Markdown.

## Features

- Create and manage slide decks using Markdown
- Generate slide content using LLMs (via LlamaBot)
- Generate and embed images in slides
- Interactive slide editing mode
- Live preview with MkSlides
- Atomic operations for slide management

## Installation

```bash
pip install llm-slides
```

## Quick Start

1. Create a new presentation:
```bash
llm-slides init "My Presentation"
```

2. Add a slide:
```bash
llm-slides add --title "Introduction" --type "title"
```

3. Start interactive mode:
```bash
llm-slides interactive
```

4. Serve the presentation:
```bash
llm-slides serve
```

## Documentation

For detailed documentation, please see the [docs](docs/) directory:

- [Design Document](docs/design.md)
- [User Guide](docs/user-guide.md) (coming soon)
- [API Reference](docs/api.md) (coming soon)

## Development

### Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/llm-slides.git
cd llm-slides
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -e ".[dev]"
```

### Running Tests

```bash
pytest
```

## License

MIT License - see [LICENSE](LICENSE) for details.