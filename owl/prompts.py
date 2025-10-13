# VLM_INSTRUCTIONS = """
# TASK: Extract ALL text and visual elements from this whiteboard image and convert to a structured PowerPoint presentation.

# CRITICAL REQUIREMENTS:
# - Extract EXACT text as it appears in the image
# - Preserve all content - do not summarize or generate new content
# - Maintain original wording, spelling, and formatting
# - Include all text, diagrams, and visual elements
# - If text is unclear, transcribe as best as possible without adding interpretation
# - There should always be a slide_number, title and content keys in the JSON.

# OUTPUT FORMAT (strict JSON only):
# {
#   "presentation_title": "[exact title from whiteboard or descriptive title based on content]",
#   "slides": [
#     {
#       "slide_number": 1,
#       "title": "[exact heading text or content-based title]",
#       "content": ["point 1", "point 2", ...],
#       "layout": "title_content"
#     }
#   ]
# }

# RULES:
# 1. Create one slide per major section/heading in the whiteboard
# 2. Use EXACT text from the whiteboard - do not modify or interpret
# 3. For bullet points or lists, create array items
# 4. For diagrams or drawings, describe them literally in square brackets [like this]
# 5. If unsure about text, include it with a [?] notation
# 6. DO NOT add any explanatory text outside the JSON
# 7. DO NOT generate any content not present in the image
# 8. Strictly make sure the output is a valid JSON object.
# 9. The content shouldn't include long code blocks, if you absolutely need any keep it to bare minimum. 

# EXAMPLE Schema:
# If the whiteboard has:
# "Project Timeline"
# "- Phase 1: Research"
# "- Phase 2: Development"

# you would return the following schema:
# {
#   "presentation_title": "Project Timeline",
#   "slides": [
#     {
#       "slide_number": 1,
#       "title": "Project Timeline",
#       "content": ["Phase 1: Research", "Phase 2: Development"],
#       "layout": "title_content"
#     }
#   ]
# }
# """

VLM_INSTRUCTIONS = """
TASK: Extract ALL text and visual elements from this whiteboard image and convert to a structured PowerPoint presentation.

CRITICAL REQUIREMENTS:
- Extract EXACT text as it appears in the image
- Preserve all content - do not summarize or generate new content
- Maintain original wording, spelling, and formatting
- Include all text, diagrams, and visual elements
- If text is unclear, transcribe as best as possible without adding interpretation
- There should always be a slide_number, title and content keys in the JSON.

OUTPUT FORMAT (strict JSON only):
{
  "presentation_title": "[exact title from whiteboard or descriptive title based on content]",
  "slides": [
    {
      "slide_number": 1,
      "title": "[exact heading text or content-based title]",
      "content": ["point 1", "point 2", ...],
      "layout": "title_content"
    }
  ]
}

CRITICAL JSON REQUIREMENTS:
- EVERY slide MUST have: slide_number, title, content (array), and layout
- EVERY content item MUST be a SINGLE STRING in double quotes (not nested arrays)
- DO NOT wrap content items in extra brackets or arrays
- content array format: ["string1", "string2", "string3"] - NOT [["string1"], ["string2"]]
- DO NOT include code blocks - break code into lines if necessary
- DO NOT include text, explanations, or any characters outside the JSON object
- NEVER end strings with incomplete quotes or parentheses
- NEVER add commentary, markdown, or text after the closing }
- DO NOT add [] prefix to strings like "[] Item" - just use "Item"
- Output ONLY the JSON object, nothing else

RULES:
1. Create one slide per major section/heading in the whiteboard
2. Use EXACT text from the whiteboard - do not modify or interpret
3. For bullet points or lists, create array items
4. For diagrams or drawings, describe them literally in square brackets [like this]
5. If unsure about text, include it with a [?] notation
6. DO NOT add any explanatory text outside the JSON
7. DO NOT generate any content not present in the image
8. Strictly make sure the output is a valid JSON object.
9. The content shouldn't include long code blocks - if code exists, put each line as a separate array item in quotes
10. Every string value MUST be properly closed with double quotes
11. Never add text like "(textarea...)" or similar comments

EXAMPLE Schema:
If the whiteboard has:
"Project Timeline"
"- Phase 1: Research"
"- Phase 2: Development"

you would return the following schema:
{
  "presentation_title": "Project Timeline",
  "slides": [
    {
      "slide_number": 1,
      "title": "Project Timeline",
      "content": ["Phase 1: Research", "Phase 2: Development"],
      "layout": "title_content"
    }
  ]
}

EXAMPLE with code:
If the whiteboard has code like:
"function test() {"
"  return 42;"
"}"

Return it as separate strings:
{
  "presentation_title": "Code Example",
  "slides": [
    {
      "slide_number": 1,
      "title": "Function Example",
      "content": ["function test() {", "  return 42;", "}"],
      "layout": "title_content"
    }
  ]
}
"""


LLM_INSTRUCTIONS = """
You are an AI presentation content enhancer. Your task is to improve the content
of the presentation while strictly maintaining the original JSON schema structure.

You will receive a presentation JSON object in the session state.
Retrieve this JSON and enhance it according to the following guidelines:

For each slide:
1. Improve clarity and professionalism of the text
2. Fix any grammar or spelling mistakes
3. Make bullet points more impactful and concise
4. Ensure consistent formatting and style
5. Do NOT change the JSON structure or field names
6. Preserve all original information and meaning
7. You are allowed to increase the number of slides while keeping the schema structure
8. Return ONLY the enhanced JSON with no additional text
9. You can keep at most four points per slide in the content.
10. If you need more than four points per slide, you can add a new slide with an appropriate title.
11. Each point should be a single line sentence.

Focus on improving text quality and think about a clear presentation flow considering 
multiple slides. Assume you are a professor preparing a presentation for a class.
"""
