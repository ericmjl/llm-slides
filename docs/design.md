# LLM Slides CLI Design Document

## Overview

LLM Slides is a command-line tool that leverages Large Language Models (LLMs) to create, edit, and manage Markdown-based slide presentations. The tool integrates with MkSlides for serving presentations and uses LlamaBot's StructuredBot and ImageBot for intelligent content generation.

## Core Features

- Create and manage slide decks using Markdown
- Generate slide content using LLMs
- Generate and embed images in slides
- Interactive slide editing mode
- Live preview with MkSlides
- Atomic operations for slide management

## Architecture

### 1. CLI Interface

The tool provides a command-line interface with the following commands:

```bash
llm-slides [command] [options]
```

#### Available Commands
- `init`: Create a new slide deck
- `add`: Add a new slide
- `edit`: Edit an existing slide
- `delete`: Remove a slide
- `serve`: Start the MkSlides server
- `interactive`: Enter interactive mode for slide management

### 2. Project Structure

```
slides/
  ├── 01-introduction.md
  ├── 02-content.md
  ├── 03-conclusion.md
  └── assets/
      └── images/
```

### 3. Slide Format

Each slide is stored as a separate Markdown file with frontmatter:

```markdown
---
title: "Slide Title"
type: "content"  # or "title", "section", etc.
---

# Main Content

- Bullet point 1
- Bullet point 2

![Generated Image](assets/images/slide-01.png)
```

## Core Operations

### Insert Operation

```python
def insert_slide(position: int, content: str) -> None:
    """
    Insert a new slide at the specified position.
    Uses StructuredBot to generate content if not provided.
    """
```

### Edit Operation

```python
def edit_slide(slide_number: int, new_content: str) -> None:
    """
    Edit an existing slide's content.
    Can use StructuredBot to suggest improvements.
    """
```

### Delete Operation

```python
def delete_slide(slide_number: int) -> None:
    """
    Remove a slide and renumber remaining slides.
    """
```

## LLM Integration

### StructuredBot

- Used for generating slide content
- Ensures proper structure and formatting
- Can suggest improvements to existing content

### ImageBot

- Generates relevant images for slides
- Handles image embedding and optimization
- Manages image assets

## Interactive Mode

The interactive mode provides a user-friendly interface for slide management:

```python
def interactive_mode():
    """
    Start an interactive session for slide management.
    Commands:
    - i: Insert slide
    - e: Edit slide
    - d: Delete slide
    - p: Preview current slide
    - s: Save changes
    - q: Quit
    """
```

## Dependencies

- `llamabot`: For LLM integration
- `mkslides`: For serving presentations
- `typer`: For CLI interface
- `rich`: For interactive terminal UI
- `pydantic`: For data validation

## Example Usage

### 1. Create a new presentation

```bash
llm-slides init "My Presentation"
```

### 2. Add a slide

```bash
llm-slides add --title "Introduction" --type "title"
```

### 3. Edit a slide

```bash
llm-slides edit 1 --content "New content"
```

### 4. Start interactive mode

```bash
llm-slides interactive
```

### 5. Serve the presentation

```bash
llm-slides serve
```

## Implementation Plan

### Phase 1: Core Infrastructure

1. Set up project structure
2. Implement basic CLI interface
3. Create slide management functions

### Phase 2: LLM Integration

1. Integrate StructuredBot
2. Integrate ImageBot
3. Implement content generation

### Phase 3: Interactive Features

1. Develop interactive mode
2. Add preview functionality
3. Implement save/load operations

### Phase 4: MkSlides Integration

1. Set up MkSlides server
2. Implement live preview
3. Add export options

### Phase 5: Testing and Documentation

1. Write unit tests
2. Create user documentation
3. Add example presentations

## Future Enhancements

- Support for multiple themes
- Custom slide templates
- Collaborative editing
- Version control integration
- Export to other formats (PDF, PPTX)
- AI-powered slide suggestions
- Real-time collaboration