# streamlit_content_gen_app.py
# To run: streamlit run streamlit_content_gen_app.py

import re
import streamlit as st
import openai

# --------------- Brand Tone Dictionary ---------------
brand_tones = {
    "Cotton On Women": (
        "You are writing for Cotton On Women.\n\n"
        "👤 Persona: Effortlessly confident, inclusive and real — like a friend who gets it.\n\n"
        "💬 Tone of Voice:\n"
        "- Optimistic, self-aware and relatable\n"
        "- Playful but never try-hard\n"
        "- Conversational, short and punchy\n"
        "- Natural rhythm with contractions\n\n"
        "🛠️ Style Guidelines:\n"
        "- Write conversationally — short sentences, natural rhythm\n"
        "- Use contractions (it's, you'll, we're)\n"
        "- Keep copy punchy and scroll-friendly\n"
        "- Be optimistic and relatable without being over the top\n"
        "- Boost these keywords where natural: women, everyday, style, denim, on repeat, just landed\n\n"
        "🚫 Avoid:\n"
        "- Luxury, elegant, sexy, fashion-forward, trendy\n"
        "- Formal, editorial, elitist, long-winded language"
    ),
    "Cotton On Men": (
        "You are writing for Cotton On Men.\n\n"
        "👤 Persona: Relaxed, confident and grounded — effortless everyday style.\n\n"
        "💬 Tone of Voice:\n"
        "- Cool, laid-back and real\n"
        "- Slightly witty, never loud\n"
        "- Direct, minimal and clear\n"
        "- No fluff — straight to the point\n\n"
        "🛠️ Style Guidelines:\n"
        "- Keep copy short and direct\n"
        "- Say more with less — no padding\n"
        "- Sound grounded and confident, not boastful\n"
        "- Subtle wit is fine; avoid forced humour\n"
        "- Boost these keywords where natural: men, tees, denim, essential, fresh, everyday\n\n"
        "🚫 Avoid:\n"
        "- Hypebeast, luxury, sartorial, pretentious language\n"
        "- Verbose, fake or overly expressive copy"
    ),
    "Cotton On Kids": (
        "You are writing for Cotton On Kids.\n\n"
        "👤 Persona: Joyful, caring and real — made for kids, written for parents.\n\n"
        "💬 Tone of Voice:\n"
        "- Playful and positive\n"
        "- Warm and easy to read\n"
        "- Never overcomplicated or overly cutesy\n\n"
        "🛠️ Style Guidelines:\n"
        "- Write simply and warmly — parents are the audience\n"
        "- Keep sentences short and easy to scan\n"
        "- Be cheerful without being saccharine\n"
        "- Focus on comfort, fun and everyday moments\n"
        "- Boost these keywords where natural: kids, play, comfort, everyday, fun\n\n"
        "🚫 Avoid:\n"
        "- Technical, formal or complex language\n"
        "- Overly descriptive or long-winded copy"
    ),
    "Cotton On Body": (
        "You are writing for Cotton On Body.\n\n"
        "👤 Persona: Supportive, real and confidence-building — like a friend in your corner.\n\n"
        "💬 Tone of Voice:\n"
        "- Encouraging, inclusive and grounded\n"
        "- Confident but never pushy\n"
        "- Conversational, calm and clear\n\n"
        "🛠️ Style Guidelines:\n"
        "- Write with warmth and reassurance\n"
        "- Focus on how products make people feel — not just look\n"
        "- Keep copy balanced and easy to follow\n"
        "- Celebrate real bodies and real life\n"
        "- Boost these keywords where natural: comfort, confidence, movement, everyday, wellness\n\n"
        "🚫 Avoid:\n"
        "- Judgmental, intimidating or exclusive language\n"
        "- Overly technical descriptions"
    ),
    "Factorie": (
        "You are writing for Factorie.\n\n"
        "👤 Persona: Youth-driven, expressive and culture-aware — plugged into now.\n\n"
        "💬 Tone of Voice:\n"
        "- Energetic and confident\n"
        "- Playful but not chaotic or cringey\n"
        "- Conversational, fast and punchy\n"
        "- Slightly edgy but controlled\n\n"
        "🛠️ Style Guidelines:\n"
        "- Keep copy short and high-energy\n"
        "- Reflect current youth culture without forcing it\n"
        "- Write like you're talking to a close friend\n"
        "- Be bold but never offensive\n"
        "- Boost these keywords where natural: streetwear, fit, fresh, trend, everyday\n\n"
        "🚫 Avoid:\n"
        "- Corporate, formal or overly slang-heavy language\n"
        "- Forced humour or try-hard vibes"
    ),
    "Rubi": (
        "You are writing for Rubi.\n\n"
        "👤 Persona: Style-obsessed, confident and easygoing — fashion made simple.\n\n"
        "💬 Tone of Voice:\n"
        "- Playful and confident\n"
        "- Never overhyped or try-hard\n"
        "- Short, clean and conversational\n\n"
        "🛠️ Style Guidelines:\n"
        "- Keep copy quick and scroll-friendly\n"
        "- Let the product shine — don't over-describe\n"
        "- Sound effortlessly stylish, not salesy\n"
        "- Boost these keywords where natural: shoes, accessories, style, everyday, fresh\n\n"
        "🚫 Avoid:\n"
        "- Expensive, luxury, formal or overly editorial language"
    ),
    "Typo": (
        "You are writing for Typo.\n\n"
        "👤 Persona: Playful, creative and a little chaotic — your fun friend with ideas for everything.\n\n"
        "💬 Tone of Voice:\n"
        "- Cheeky, upbeat and self-aware\n"
        "- Playful but never cringe or try-hard\n"
        "- Expressive and conversational\n\n"
        "🛠️ Style Guidelines:\n"
        "- Use short lines with lots of personality\n"
        "- Celebrate creativity and individuality\n"
        "- Be punchy — get to the fun fast\n"
        "- A little chaos is on-brand; total chaos is not\n"
        "- Boost these keywords where natural: fun, desk, gift, vibes, creative, everyday\n\n"
        "🚫 Avoid:\n"
        "- Formal, luxury, overly polished or corporate language"
    ),
    "Supre": (
        "You are writing for Supre.\n\n"
        "👤 Persona: Confident, expressive and trend-aware — owns the moment.\n\n"
        "💬 Tone of Voice:\n"
        "- Empowered and playful\n"
        "- Never overdone or overly polished\n"
        "- Conversational with attitude\n"
        "- Short, bold and clear\n\n"
        "🛠️ Style Guidelines:\n"
        "- Write with confidence and energy\n"
        "- Keep it short — bold statements over long paragraphs\n"
        "- Speak to a young, fashion-forward audience\n"
        "- Boost these keywords where natural: denim, fit, style, confidence, new\n\n"
        "🚫 Avoid:\n"
        "- Formal, safe, flat or overly descriptive copy"
    ),
    "Ceres Life": (
        "You are writing for Ceres Life.\n\n"
        "👤 Persona: Calm, conscious and grounded — simple living, done well.\n\n"
        "💬 Tone of Voice:\n"
        "- Warm, honest and optimistic\n"
        "- Never preachy or heavy\n"
        "- Minimal, clear and thoughtful\n\n"
        "🛠️ Style Guidelines:\n"
        "- Use fewer words with more meaning\n"
        "- Let products speak through feel and function, not hype\n"
        "- Be genuine about sustainability — grounded, never preachy\n"
        "- Keep copy calm and considered\n"
        "- Boost these keywords where natural: natural, everyday, comfort, considered, timeless\n\n"
        "🚫 Avoid:\n"
        "- Loud, overstyled, greenwashing or technical jargon"
    ),
    "Upstate Sport": (
        "You are writing for Upstate Sport.\n\n"
        "👤 Persona: Supportive, energetic and community-driven — your workout hype partner.\n\n"
        "💬 Tone of Voice:\n"
        "- Empowering and positive\n"
        "- Confident but never aggressive\n"
        "- Short, punchy and motivating\n\n"
        "🛠️ Style Guidelines:\n"
        "- Write with energy and encouragement\n"
        "- Focus on movement, community and feeling good\n"
        "- Keep copy clear and action-oriented\n"
        "- Celebrate all fitness levels — inclusive and welcoming\n"
        "- Boost these keywords where natural: movement, energy, confidence, community, active\n\n"
        "🚫 Avoid:\n"
        "- Intimidating, hardcore fitness, technical jargon or exclusive language"
    ),
    "Cotton On Foundation": (
        "You are writing for Cotton On Foundation.\n\n"
        "👤 Persona: Purpose-led, optimistic and human — focused on real impact.\n\n"
        "💬 Tone of Voice:\n"
        "- Hopeful, positive and genuine\n"
        "- Celebrates progress, not guilt\n"
        "- Simple, clear and inclusive\n\n"
        "🛠️ Style Guidelines:\n"
        "- Use 'we', 'us' and 'together' to build community\n"
        "- Focus on positive outcomes and real stories\n"
        "- Keep language accessible and human\n"
        "- Inspire action through hope, not obligation\n"
        "- Boost these keywords where natural: impact, positive change, together, good choice, community, support, feel-good\n\n"
        "🚫 Avoid:\n"
        "- 'Save the planet', 'charity', 'eco-friendly'\n"
        "- Guilt-driven messaging, negative framing or greenwashing"
    ),
}

# --------------- Markdown to HTML Converter ---------------
def markdown_to_html(text: str) -> str:
    lines = text.splitlines()
    html_lines = []
    paragraph_lines = []

    def flush_paragraph():
        nonlocal paragraph_lines
        if paragraph_lines:
            html_lines.append("<p>" + "<br>\n".join(paragraph_lines) + "</p>")
            paragraph_lines = []

    for line in lines:
        stripped = line.strip()
        if not stripped:
            flush_paragraph()
            continue

        m_h2 = re.match(r"^## (.+)$", stripped)
        m_h3 = re.match(r"^### (.+)$", stripped)
        m_h4 = re.match(r"^#### (.+)$", stripped)

        if m_h2:
            flush_paragraph()
            heading_text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", m_h2.group(1))
            html_lines.append(f"<h2>{heading_text}</h2>")
            continue
        if m_h3:
            flush_paragraph()
            heading_text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", m_h3.group(1))
            html_lines.append(f"<h3>{heading_text}</h3>")
            continue
        if m_h4:
            flush_paragraph()
            heading_text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", m_h4.group(1))
            html_lines.append(f"<h4>{heading_text}</h4>")
            continue

        line_html = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", stripped)
        paragraph_lines.append(line_html)

    flush_paragraph()
    return "<html><body>\n" + "\n".join(html_lines) + "\n</body></html>"

# --------------- UI ---------------
st.set_page_config(page_title="COG SEO Content Generator 3.0", page_icon="📝", layout="wide")
st.title("📝 COG SEO Content Generator 3.0")
st.caption("Generate SEO‑friendly titles, meta descriptions, and page copy in brand tone.")

with st.sidebar:
    st.header("Settings")
    api_key = st.text_input("OpenAI API Key", type="password", help="Your API key is used only for this session.")
    brand = st.selectbox("Brand", list(brand_tones.keys()))
    model = st.selectbox("Model", ["gpt-5", "gpt-4o", "gpt-4.1", "gpt-4-turbo", "gpt-4", "gpt-3.5-turbo"], index=0)
    word_pref = st.radio("Length (soft preference)", options=[300, 500, 750], index=1, format_func=lambda x: {300:"Short (~300)",500:"Medium (~500)",750:"Long (~750)"}[x])

col1, col2 = st.columns(2)
with col1:
    primary = st.text_input("Primary Keyword*", help="Required.")
    category = st.text_input("Page Category*", help="Required. E.g., 'Women's Lingerie'")
    extra_context = st.text_area("Extra Context (Optional)", placeholder="Optional: campaign goals, audience insight, seasonal trend, product USP, content angle, etc.", height=100)
with col2:
    secondary = st.text_input("Secondary Keywords (comma‑separated)")
    num_topics = st.number_input("Number of Topics", min_value=0, max_value=10, value=3, step=1)

topic_inputs = []
for i in range(int(num_topics)):
    topic_inputs.append(st.text_input(f"Topic {i+1}", key=f"topic_{i+1}"))

st.markdown("---")
generate = st.button("🚀 Generate Content", use_container_width=True)

# --------------- Generation Logic ---------------
if generate:
    if not api_key or not primary or not category:
        st.error("Please provide your API key, Primary Keyword, and Page Category.")
    else:
        topics = [t.strip() for t in topic_inputs if t and t.strip()]
        brand_tone = brand_tones.get(brand, "")

        prompt = f"{brand_tone}\n\n"
        if extra_context.strip():
            prompt += (
                "🧭 Context to guide the writing (must be reflected throughout):\n"
                f"{extra_context.strip()}\n\n"
                "Every section should explicitly connect to this context with examples, angles, or language choices.\n\n"
            )

        prompt += (
            f"Write SEO content for the page category '{category}' for the brand '{brand}'.\n\n"
            "Your task:\n"
            f"1. Create a punchy, SEO-optimized **Page Title** using the primary keyword: '{primary}'.\n"
            f"2. Suggest a strong **Meta Description** under 160 characters that includes secondary keywords: {secondary}.\n"
            "3. Write comprehensive, SEO-friendly content with a friendly intro paragraph (no heading) and sections covering each topic.\n"
            "4. Ensure the content is informative, valuable, and fully answers each topic.\n"
            "5. Let depth be driven by relevance to the provided context—do **not** pad for length. Be concise when possible; expand only when helpful.\n"
            "6. Write naturally with no bullet points or lists; use normal paragraphs only.\n"
        )

        if word_pref:
            prompt += (
                f"\nLength preference (soft): Aim roughly around {word_pref} words for the main content if the context warrants it; "
                "otherwise keep it as short as possible while being complete.\n"
            )

        if topics:
            prompt += (
                "\nStructure the content as follows:\n"
                "- Start with an intro paragraph tied to the Extra Context.\n"
                "- Then provide sections with these headings (use ### for every topic heading):\n"
            )
            for topic in topics:
                prompt += f"### {topic} \u2014 Connect this topic clearly back to the Extra Context.\n"

        try:
            client = openai.OpenAI(api_key=api_key)
            with st.spinner("Generating..."):
                response = client.chat.completions.create(
                    model=model,
                    messages=[{"role": "user", "content": prompt}]
                )
            generated = response.choices[0].message.content or ""
        except Exception as e:
            st.error(f"OpenAI error: {e}")
            st.stop()

        def clean_output(text):
            lines = text.splitlines()
            cleaned = []
            for line in lines:
                # Remove # markers from Page Title and Meta Description label lines
                if re.match(r'^#{1,6}\s*(page title|meta description)', line, re.IGNORECASE):
                    line = re.sub(r'^#{1,6}\s*', '', line)
                # Normalise all other headings to H3
                elif re.match(r'^#{1,6}\s', line):
                    line = re.sub(r'^#{1,6}\s+', '', line)
                    line = "### " + line
                cleaned.append(line)
            return "\n".join(cleaned)

        generated = clean_output(generated)

        content_only = re.sub(r'(?i)(title|meta description):.*', '', generated)
        word_count = len(re.findall(r'\b\w+\b', content_only))

        st.success("Done!")
        st.caption(f"Word count (reference only): {word_count}")
        st.markdown("### Generated Content")
        st.markdown(generated)

        # Downloads
        html_output = markdown_to_html(generated)
        st.download_button("📥 Download HTML", data=html_output, file_name="generated_content.html", mime="text/html")
        st.download_button("📥 Download Markdown", data=generated, file_name="generated_content.md", mime="text/markdown")
