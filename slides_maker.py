# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "anthropic==0.54.0",
#     "ipython==9.3.0",
#     "llamabot[all]==0.12.7",
#     "marimo",
#     "pydantic==2.11.5",
# ]
# ///

import marimo

__generated_with = "0.13.15"
app = marimo.App(width="medium")


@app.cell
def _():
    import llamabot as lmb
    from pydantic import BaseModel, Field

    return BaseModel, Field, lmb


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell
def _(BaseModel, Field):
    from typing import Literal
    from pydantic import model_validator
    import re

    class Slide(BaseModel):
        title: str
        content: str = Field(description="Arbitrary markdown or HTML content")
        type: Literal["HTML", "Markdown"]

        @model_validator(mode="after")
        def check_no_header_in_content(self):
            """Check that there are no headers in the content, this is explicitly not allowed."""
            # Check for Markdown headers (# Header, ## Header, etc.)
            if self.type == "Markdown":
                # Look for lines starting with one or more # followed by a space
                header_pattern = re.compile(r"^#{1,6}\s", re.MULTILINE)
                if header_pattern.search(self.content):
                    raise ValueError(
                        "Headers are not allowed in slide content. Use regular text formatting instead."
                    )

            # For HTML content, check for header tags
            elif self.type == "HTML":
                header_tags = ["<h1", "<h2", "<h3", "<h4", "<h5", "<h6"]
                for tag in header_tags:
                    if tag in self.content.lower():
                        raise ValueError(
                            "HTML header tags (h1-h6) are not allowed in slide content."
                        )

            return self

        def render(self):
            return f"""## {self.title}

    {self.content}
            """

    return (Slide,)


@app.cell
def _(Slide, lmb):
    @lmb.prompt("system")
    def slidemaker_sysprompt():
        """You are an expert at making markdown slides.

        Your job is to produce a single slide that represents the content
        that a user asks for.
        Tables should be in HTML.
        """

    slidemaker = lmb.StructuredBot(slidemaker_sysprompt(), Slide)
    return (slidemaker,)


@app.cell
def _(mo, slidemaker):
    eatwell_slide = slidemaker("Why it is important to eat well.")
    mo.md(eatwell_slide.render())
    return


@app.cell
def _(mo, slidemaker):
    sales_slide = slidemaker("Table showing growth in sales.")
    mo.md(sales_slide.render())
    return


@app.cell
def _(mo, slidemaker):
    two_column_slide = slidemaker(
        "Two columns of bullet points. One column says pros of buying a thing, other is cons."
    )
    mo.md(two_column_slide.render())
    return


@app.cell
def _(image, mo, slidemaker):
    picture_slide = slidemaker(f"A slide that shows a picture of this dog: {image}")
    mo.md(picture_slide.render())
    return


@app.cell
def _(mo, slidemaker):
    youtube_embed_slide = slidemaker(
        "I want to use this youtube talk: https://www.youtube.com/watch?v=3ZTGwcHQfLY, which outlines why it's important to know how to make the tools that make the things that we use, to make the case that we should make our own tools. Embed this in the talk slide, and give me just the conclusion. Title should be 'The importance of making our own tools'"
    )
    mo.md(youtube_embed_slide.render())
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    Notes to self:

    1. This is a bit unsatisfactory, in that I cannot preview the dog in a marimo notebook, but I am quite sure that if the image is generated and the markdown is written to disk, it'll be fine.
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""Now I am going to try a different thing: we'll try compiling a whole slide deck."""
    )
    return


@app.cell
def _(BaseModel, Slide, lmb, slidemaker):
    from pathlib import Path
    from slugify import slugify
    from typing import Optional

    @lmb.prompt("user")
    def slidemaker_edit(new_request, existing_slide):
        """This is the request for an edit on a slide.

        {{ new_request }}

        The existing content is here:

        {{ existing_slide }}

        Help me create a new slide based on the new request,
        using the existing slide as inspiration or basis where appropriate.
        """

    @lmb.prompt("user")
    def slidemaker_insert(
        new_request: str,
        existing_slides: str,
    ):
        """This is the request to insert a slide.

        {{ new_request }}

        ---

        Here is the current state of the slides:

        {{ existing_slides }}

        ---

        Help me create a new slide based on the new request,
        weaving it seamlessly with the slide before and after.
        """

    class SlideDeck(BaseModel):
        slides: list[Slide]
        talk_title: str

        def render(self) -> str:
            """Render all slides as markdown with slide separators."""
            markdown_content = []

            for i, slide in enumerate(self.slides):
                # Add slide content
                slide_content = f"## {slide.title}\n\n{slide.content}"
                markdown_content.append(slide_content)
                markdown_content.append(f"\nSlide {i}")

                # Add separator after each slide except the last one
                if i < len(self.slides) - 1:
                    markdown_content.append("---")

            # Join all slides with newlines
            return "\n\n".join(markdown_content)

        def save(self, path: Path):
            """Save the slide deck as a markdown file."""
            markdown_content = self.render()

            # Ensure the directory exists
            path.parent.mkdir(parents=True, exist_ok=True)

            # Write the content to the file
            with open(path, "w", encoding="utf-8") as f:
                f.write(markdown_content)

            return f"Slide deck saved to {path}"

        def edit(self, index: int, change: str):
            """Edit the slide at a given index."""
            current_slide = self.slides[index].render()

            new_slide = slidemaker(slidemaker_edit(change, current_slide))
            self.slides[index] = new_slide

        def select(self, description: str):
            """Return a slide's index by natural language."""
            docstore = lmb.LanceDBDocStore(
                table_name="deckbot", storage_path=Path("/tmp")
            )
            docstore.reset()
            docstore.extend([slide.render() for slide in self.slides])
            index = {slide.render(): i for i, slide in enumerate(self.slides)}

            docs = docstore.retrieve(description)
            return index[docs[0]]

        def insert(self, index, description):
            """Insert a slide just before a given index."""
            current_slides = self.render()  # used for context
            new_slide = slidemaker(slidemaker_insert(description, current_slides))
            self.slides.insert(index, new_slide)

    return Path, SlideDeck


@app.cell
def _(SlideDeck, lmb):
    @lmb.prompt("system")
    def deckbot_sysprompt():
        """You are a bot that helps people make slides for a presentation.
        Vary the style of slides when you generate them, do not stick to only bullet points.
        Quotes should be formatted as such."""

    chat_memory = lmb.LanceDBDocStore(table_name="deckbot-chat-memory")
    chat_memory.reset()

    deckbot = lmb.StructuredBot(
        system_prompt=deckbot_sysprompt(),
        pydantic_model=SlideDeck,
        chat_memory=chat_memory,
    )
    return (deckbot,)


@app.cell
def _(deckbot):
    deck = deckbot("A talk on DeckBot, which is what I now use to make slides.")
    return (deck,)


@app.cell
def _(deck, mo):
    mo.md(deck.render())
    return


@app.cell
def _(deck, mo):
    deck.edit(1, "Change this to use an appropriate quote from scripture.")
    mo.md(deck.render())
    return


@app.cell
def _(deck):
    deck.edit(
        deck.select("User testimonial"),
        "Change to two testimonials, side-by-side, in two columns.",
    )
    return


@app.cell
def _(deck, mo):
    mo.md(deck.render())
    return


@app.cell
def _(deck):
    deck.edit(
        deck.select("What users say"),
        "Two testimonials instead, but make it two columns in HTML.",
    )
    return


@app.cell
def _(deck, mo):
    mo.md(deck.render())
    return


@app.cell
def _(deck, mo):
    deck.insert(1, "A slide that uses a mermaid diagram that shows how to use deckbot.")
    mo.md(deck.render())
    return


@app.cell
def _(Path, deck):
    deck.save(Path("deckbot.md"))
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
