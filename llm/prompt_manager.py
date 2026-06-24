class PromptManager:
    """
    Builds prompts for each tenant including agent bits.
    """

    def __init__(self, tenant):
        self.tenant = tenant

    def _agent_bits_text(self) -> str:
        """
        Convert agent bits (list of strings) into a formatted prompt block.
        """
        bits = self.tenant.config.get("agent_bits") or []
        if not bits:
            return ""

        formatted = "\n".join(f"- {bit}" for bit in bits)

        return (
            "\n\nIMPORTANT BUSINESS CONTEXT:\n"
            "The following temporary business notices MUST be considered when answering:\n"
            f"{formatted}\n"
        )

    def build_full_prompt(self, user_query, context_docs):
        style_prompt = self.tenant.config.get("style_prompt", "")
        guardrails_prompt = self.tenant.config.get("guardrails", "")
        agent_bits_prompt = self._agent_bits_text()

        print("DOC TYPE:", type(context_docs[0]))
        print("DOC SAMPLE:", context_docs[0])

        context_section = "\n".join(
            doc.page_content for doc in context_docs
        )
        print("CONTEXT DOC COUNT:", len(context_docs))
        print("FINAL CONTEXT:")
        print(context_section[:1000])

        return f"""
SYSTEM INSTRUCTIONS:
{self.tenant.config.get("system_prompt")}

STYLE:
{style_prompt}

RULES:
{guardrails_prompt}

{agent_bits_prompt}

KNOWLEDGE BASE CONTEXT:
{context_section}

USER QUERY:
{user_query}

INSTRUCTIONS:
You MUST ONLY answer using the information from the KNOWLEDGE BASE CONTEXT above.
Do NOT use external knowledge or general internet knowledge.
Follow the STYLE and RULES strictly.
If the answer is NOT found in the KNOWLEDGE BASE CONTEXT, you MUST say "I don't know based on the available documents."
Do NOT attempt to answer from general knowledge.
""".strip()
