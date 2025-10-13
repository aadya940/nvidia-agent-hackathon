import json


def convert_llm_io_to_pydict(llm_output: str):
    try:
        return json.loads(llm_output)
    except json.JSONDecodeError:
        return llm_output
