from google import genai


class GeminiAIError(Exception):
    """Custom exception for Gemini AI related errors."""

    pass


def generate_financial_tesis(financial_data: dict) -> str:
    # The client gets the API key from the environment variable `GEMINI_API_KEY`.
    client = genai.Client()
    gemini_model = "gemini-2.5-pro"
    gemini_config = genai.types.GenerateContentConfig(
        system_instruction="Senior Equity Research Analyst (Microsoft Specialist)",
    )

    prompt = f"""
**Objective:**
Act as a Senior Equity Research Analyst at a top-tier investment bank (e.g., Morgan Stanley, Goldman Sachs). Analyze the provided historical financial data of Microsoft (MSFT) from Fiscal Year 2014 to Fiscal Year 2025. Based on the financial trends and the structural shift in the business model, generate a forward-looking investment thesis and future expectations for institutional investors.

**Data Source (Financials FY2014-FY2025):**
{financial_data}

**Instructions for Analysis:**

1.  **Structural Revenue Shift (The Core Thesis):**
    * Compare the composition of revenue in 2016 (Product: ~$61.5B vs. Service: ~$23.8B) against 2025 (Product: ~$63.9B vs. Service: ~$217.7B).
    * Analyze what this inversion means for business stability, recurring revenue (SaaS), and long-term valuation multiples.
    * Highlight that "Product" revenue has remained relatively flat/stable over a decade, while "Service and other" has grown nearly 10x.

2.  **Margin & Efficiency Analysis:**
    * Calculate the **Net Profit Margin** trend from 2015 to 2025 (Net Income / Revenue).
    * Evaluate the **Operating Leverage**. Is Operating Income growing faster than Revenue?
    * Analyze R&D efficiency. R&D spending has tripled from ~$12B (2015) to ~$32.5B (2025). Are the returns on this innovation capital (ROI) reflected in the Net Income growth?

3.  **Future Investor Expectations (2026-2030):**
    * Based on the data trend (specifically the acceleration in Service revenue between 2023 and 2025), project the sustainability of double-digit growth.
    * **Cost Management:** Note that despite massive revenue growth, General & Administrative costs have only risen from ~$4.6B (2015) to ~$7.2B (2025). Analyze how this discipline impacts future earnings power.
    * **EPS Growth:** Analyze the Diluted EPS trajectory ($1.48 in 2015 to $13.64 in 2025). What does this imply for share buybacks and shareholder value creation?

4.  **Risk & Verdict:**
    * Identify key risks (e.g., rising infrastructure costs/CapEx for AI).
    * Provide a clear Buy/Hold/Sell verdict with a Price Target.

4.  **Final Output:**
    * Produce a structured **"Investor Outlook Note"**.
    * Include a section on **"Key Risks"** derived from the data (e.g., rising Cost of Revenue in Services suggesting higher infrastructure/AI costs).
    * Provide a **Verdict**: Is the stock a Buy/Hold/Sell based on the fundamentals shown in this 10-year snapshot and the actual stocks price?

**STRICT OUTPUT RULES (CRITICAL):**
1.  **NO Conversational Filler:** Do not output text like "Here is the analysis," "Sure," or "I hope this helps."
2.  **NO Error Logging:** If data for a specific year (e.g., 2014) is missing or incomplete, ignore it silently. Do not print "Skipping year..." or any debug notes.
3.  **Direct Start:** Your output must start immediately with the Report Title (e.g., `### [INTERNAL MEMO]`).
4.  **Format:** Use strict Markdown. Use bolding for key metrics.
        * Use professional financial terminology (CAGR, Operating Leverage, ARPU, Gross Margin Expansion).
        * Use bullet points for readability.
5.  **Language:** Spanish.
"""
    try:
        response = client.models.generate_content(
            model=gemini_model, contents=prompt, config=gemini_config
        )
    except Exception as e:
        print(f"Error al generar contenido con Gemini AI: {e}")

    if response.prompt_feedback:
        raise GeminiAIError(
            f"Gemini AI reported an issue with the prompt: {response.prompt_feedback}."
        )

    if not response.candidates:
        raise GeminiAIError("La respuesta de Gemini vino vacía (sin candidatos).")

    candidate = response.candidates[0]

    if candidate.finish_reason != "STOP":
        raise GeminiAIError(
            f"Gemini no terminó correctamente. Razón: {candidate.finish_reason}"
        )

    return response.text
