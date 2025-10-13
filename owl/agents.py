from google.adk.models.lite_llm import LiteLlm
from google.adk.agents import LoopAgent, LlmAgent, SequentialAgent
from google.adk.agents import BaseAgent
from google.adk.events import Event, EventActions
from google.adk.agents.invocation_context import InvocationContext
from typing import AsyncGenerator
import logging
import json
import re
import pythonmonkey

jsonrepair = pythonmonkey.require('jsonrepair').jsonrepair

from .prompts import VLM_INSTRUCTIONS, LLM_INSTRUCTIONS
from .validators import validate_vlm_output, PresentationSchema
from .ppt_manager import convert_json_to_marp, run_marp

logger = logging.getLogger(__name__)

# Tag for `cosmos-nemotron-34b`
VLM_MODEL = LiteLlm(model="nvidia_nim/nvidia/llama-3.1-nemotron-nano-vl-8b-v1")
# LLM_MODEL = LiteLlm(model="nvidia_nim/nvidia/llama-3.1-nemotron-ultra-253b-v1")


class VLMAgent(BaseAgent):
    """Custom VLM Agent that captures output to session state."""

    vlm_llm_agent: LlmAgent

    model_config = {"arbitrary_types_allowed": True}

    def __init__(
        self, name: str, description: str, instructions: str, model, output_schema
    ):
        # Create an LlmAgent to wrap the model
        # Use output_key to automatically save the LLM response to session state
        vlm_llm_agent = LlmAgent(
            name=f"{name}_llm",
            model=model,
            instruction=instructions,
            output_key="vlm_raw_response",  # Automatically saves response to state
        )

        # Pydantic will validate and assign them based on the class annotations
        super().__init__(
            name=name,
            vlm_llm_agent=vlm_llm_agent,
        )

    async def _run_async_impl(
        self, ctx: InvocationContext
    ) -> AsyncGenerator[Event, None]:
        """Runs the VLM model and stores output in session state."""
        logger.info(f"[{self.name}] Running VLM Agent...")

        # Clear previous state to avoid context bloat
        try:
            # Call the LLM agent with a timeout
            async for event in self.vlm_llm_agent.run_async(ctx):
                yield event

            # Get the raw response from the LLM agent
            llm_response_text = ctx.session.state.pop("vlm_raw_response", "")

            logger.info(
                f"[{self.name}] Raw LLM response length: {len(llm_response_text)}"
            )
            logger.info(f"[{self.name}] Response preview: {llm_response_text}")

            try:
                # Extract and parse JSON from the response.
                # json_match = re.search(r"\{[\s\S]*?\}", llm_response_text)
                json_match = re.search(r"\{[\s\S]*?\}", llm_response_text)
                if json_match:
                    json_str = json_match.group(0)
                    json_str = jsonrepair(json_str)

                    ctx.session.state["vlm_output"] = json.loads(json_str)
                    
                    logger.info(
                        f"[{self.name}] VLM output parsed and stored successfully"
                    )
                
                else:
                    logger.error(f"[{self.name}] No JSON found in LLM response")
                    ctx.session.state["vlm_output"] = None
            
            except json.JSONDecodeError as e:
                logger.error(f"[{self.name}] Failed to parse JSON: {e}")
                ctx.session.state["vlm_output"] = None

        except Exception as e:
            logger.error(f"[{self.name}] Error running VLM: {str(e)}")
            ctx.session.state["vlm_output"] = None
            yield Event(author=self.name, actions=EventActions(escalate=False))
            return

        # Continue to next agent
        yield Event(author=self.name, actions=EventActions(escalate=False))


class ValidateVLMOutputAgent(BaseAgent):
    """Custom agent to validate VLM output against the presentation schema.
    Escalates if validation is successful, stays in loop if it fails.
    """

    async def _run_async_impl(
        self, ctx: InvocationContext
    ) -> AsyncGenerator[Event, None]:
        """Checks if VLM output is valid.
        Escalates if valid, continues loop if invalid.
        """

        # Get VLM output from session state
        vlm_output = ctx.session.state.get("vlm_output", None)

        if vlm_output is None:
            # No output yet, continue loop
            yield Event(author=self.name, actions=EventActions(escalate=False))
            return

        # Validate schema
        is_valid = self._validate_schema(vlm_output)

        # Update state with validation result
        ctx.session.state["validation_passed"] = is_valid

        logger.info(f"[{self.name}] Validation result: {is_valid}")

        if is_valid:
            yield Event(author=self.name, actions=EventActions(escalate=True))
        else:
            yield Event(author=self.name, actions=EventActions(escalate=False))

    def _validate_schema(self, vlm_output: dict) -> bool:
        """Validates VLM output using the imported validation function.
        Returns True if valid, False otherwise.
        """
        return validate_vlm_output(vlm_output)


class EnhancerAgent(BaseAgent):
    """Enhances the textual information extracted from the whiteboarding image
    while maintaining the JSON schema structure."""

    llm_agent: LlmAgent
    model_config = {"arbitrary_types_allowed": True}

    def __init__(self, name: str):
        llm_agent = LlmAgent(
            name=f"{name}_llm",
            model="gemini-2.5-flash",
            instruction=LLM_INSTRUCTIONS,
            output_key="enhanced_output",  # Automatically saves response to state
        )
        super().__init__(
            name=name,
            llm_agent=llm_agent,
        )

    async def _run_async_impl(
        self, ctx: InvocationContext
    ) -> AsyncGenerator[Event, None]:
        """Enhances the VLM output using LLM while preserving the schema."""
        # Get validated VLM output from session state
        vlm_output = ctx.session.state.get("vlm_output", None)

        if vlm_output is None:
            logger.error(f"[{self.name}] No VLM output found in session state")
            yield Event(author=self.name, actions=EventActions(escalate=False))
            return

        try:
            # Get enhanced content from LLM
            logger.info(f"[{self.name}] Enhancing presentation content...")
            async for event in self.llm_agent.run_async(ctx):
                yield event

            # Parse the enhanced output
            try:
                enhanced_output = ctx.session.state.pop("enhanced_output", "")
                logger.info(f"[{self.name}] Enhanced output: {enhanced_output}")

                # Remove gemini markdown quotes.

                enhanced_output = enhanced_output.strip()
                if enhanced_output.startswith("```"):
                    enhanced_output = enhanced_output[3:]
                    if enhanced_output.startswith("json"):
                        enhanced_output = enhanced_output[4:]

                if enhanced_output.endswith("```"):
                    enhanced_output = enhanced_output[:-3]

                enhanced_output = enhanced_output.strip()
                enhanced_output = json.loads(enhanced_output)

                markdown_content = convert_json_to_marp(enhanced_output)
                run_success = run_marp("presentation.md", "presentation.pptx")

                if run_success:
                    logger.info(f"[{self.name}] Content enhancement successful")
                    yield Event(author=self.name, actions=EventActions(escalate=True))
                else:
                    logger.error(f"[{self.name}] Failed to run MARP")
                    yield Event(author=self.name, actions=EventActions(escalate=False))

            except json.JSONDecodeError as e:
                logger.error(f"[{self.name}] Failed to parse enhanced output: {str(e)}")
                logger.debug(
                    f"Raw response: {ctx.session.state.pop("enhanced_output", "")}"
                )
                yield Event(author=self.name, actions=EventActions(escalate=False))

        except Exception as e:
            logger.error(f"[{self.name}] Error in enhancement: {str(e)}")
            yield Event(author=self.name, actions=EventActions(escalate=False))


vlm_agent = VLMAgent(
    name="core_vlm_agent",
    description="Core VLM Agent to understand whiteboarding images",
    instructions=VLM_INSTRUCTIONS,
    model=VLM_MODEL,
    output_schema=PresentationSchema,
)
validation_agent = ValidateVLMOutputAgent(name="ValidationAgent")
enhancer_agent = EnhancerAgent(name="ContentEnhancer")

# Core Loop to generate and enhance the VLM output
_core_loop = LoopAgent(
    name="_CoreLoop", sub_agents=[vlm_agent, validation_agent], max_iterations=5
)
core_loop = SequentialAgent(
    name="CoreLoop",
    sub_agents=[_core_loop, enhancer_agent],
)
