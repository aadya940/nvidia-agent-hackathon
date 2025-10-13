from pydantic import BaseModel, ValidationError
from typing import Union, Optional


class Slide(BaseModel):
    slide_number: int
    title: str
    content: Union[str, list[str]]
    layout: Optional[str] = "title_content"


class PresentationSchema(BaseModel):
    presentation_title: str
    slides: list[Slide]


def validate_vlm_output(vlm_output: dict) -> bool:
    """
    Validates VLM output against the presentation schema.

    Args:
        vlm_output: Dictionary returned from NVIDIA NIM VLM

    Returns:
        bool: True if output is valid, False otherwise
    """
    try:
        # Validate against Pydantic schema
        PresentationSchema(**vlm_output)
        return True

    except ValidationError as e:
        print(f"Schema validation error: {e}")
        return False
    except Exception as e:
        print(f"Unexpected error during validation: {e}")
        return False
