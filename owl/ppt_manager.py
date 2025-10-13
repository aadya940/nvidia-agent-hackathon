import subprocess


def convert_json_to_marp(
    presentation_data: dict, output_path: str = "presentation.md"
) -> str:
    """
    Converts validated JSON presentation data to Marp-compatible markdown.

    Args:
        presentation_data:
            Validated dictionary from VLM
        output_path:
            File path to save the markdown file

    Returns:
        str: The generated markdown content
    """
    lines = []

    # Add Marp front matter
    lines.append("---")
    lines.append("marp: true")
    lines.append("theme: default")
    lines.append("paginate: true")
    lines.append("---")
    lines.append("")

    # Title slide
    lines.append(f"# {presentation_data['presentation_title']}")
    lines.append("")
    lines.append("---")
    lines.append("")

    # Content slides
    for slide in presentation_data["slides"]:
        slide_number = slide["slide_number"]
        title = slide["title"]
        content = slide["content"]

        # Add slide title
        lines.append(f"# {title}")
        lines.append("")

        # Add content based on type
        if isinstance(content, list):
            # List of items (bullet points)
            for item in content:
                lines.append(f"- {item}")
            lines.append("")
        else:
            # Single text block
            lines.append(content)
            lines.append("")

        # Add slide separator (except for last slide)
        if slide_number < len(presentation_data["slides"]):
            lines.append("---")
            lines.append("")

    # Join all lines
    markdown_content = "\n".join(lines)

    # Save to file
    with open(output_path, "w") as f:
        f.write(markdown_content)

    return markdown_content


def run_marp(
    markdown_file: str, output_file: str, theme: str = "gaia", template: str = "bespoke"
) -> bool:
    """
    Execute Marp CLI command to generate presentation.

    Args:
        markdown_file:
            Input markdown file
        output_file:
            Output presentation file (e.g., presentation.pptx)
        theme:
            Marp theme (default: gaia)
        template:
            Marp template (default: bespoke)

    Returns:
        bool: True if successful, False otherwise
    """
    cmd = f"marp --theme {theme} --template {template} {markdown_file} -o {output_file}"

    print(f"🚀 {cmd}")

    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)

        if result.returncode == 0:
            print(f"✓ Presentation generated: {output_file}")
            return True
        else:
            print(f"❌ Error: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
