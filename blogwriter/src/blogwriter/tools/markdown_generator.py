from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field


class MarkdownGeneratorInput(BaseModel):
    """Input schema for MarkdownGenerator."""
    title: str = Field(..., description="Title of the blog post.")
    content: str = Field(..., description="Content of the blog post.")
    filename: str = Field(..., description="Name of the file to save the blog post.")


class MarkdownGenerator(BaseTool):
    name: str = "Markdown Generator"
    description: str = (
        "This tool generates a markdown file with the given title and content."
    )
    args_schema: Type[BaseModel] = MarkdownGeneratorInput

    def _run(self, title: str, date: str, content: str, filename: str) -> str:
        with open(filename, "w") as f:
            # Write front matter
            f.write("---\n")
            f.write(f"title: {title}\n")
            f.write(f"date: {date}\n")
            f.write(f"draft: true\n")
            f.write("---\n\n")
            f.write(f"# {title}\n\n{content}")
        return f"Markdown file saved at {filename}."
