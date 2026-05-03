def generate(sections: dict) -> list[dict]:
    recs = []

    def add(section, priority, title, detail, effort):
        recs.append({"section": section, "priority": priority, "title": title, "detail": detail, "effort": effort})

    # --- Brand Authority ---
    ba = sections.get("brand_authority", {}).get("details", {})
    if not ba.get("wikipedia_en"):
        add("brand_authority", "high",
            "Create a Wikipedia page (English)",
            "LLMs are heavily trained on Wikipedia. A well-sourced English Wikipedia article about your brand is one of the highest-ROI GEO actions. Start with Wikidata, then draft a neutral, citation-backed article.",
            "high")
    if not ba.get("wikipedia_pl") and not ba.get("wikipedia_en"):
        add("brand_authority", "high",
            "Create a Wikipedia page (Polish)",
            "Polish Wikipedia is a strong local signal. Even a short, well-cited stub helps LLMs associate your brand with relevant queries in Polish-language contexts.",
            "medium")
    if not ba.get("trustpilot"):
        add("brand_authority", "high",
            "Claim and build your Trustpilot profile",
            "Trustpilot is a top source LLMs cite for brand reputation. Create a profile, respond to reviews, and actively encourage customers to leave feedback. Aim for 100+ reviews.",
            "medium")
    if not ba.get("youtube"):
        add("brand_authority", "medium",
            "Launch a branded YouTube channel",
            "YouTube content (product reviews, tutorials, brand stories) gets indexed by LLMs. A channel with consistent uploads also builds brand search volume, a strong indirect signal.",
            "medium")
    if not ba.get("linkedin"):
        add("brand_authority", "medium",
            "Claim your LinkedIn company page",
            "LinkedIn is used by LLMs to verify company existence and size. A complete page with description, logo, and regular posts improves brand entity recognition.",
            "low")

    # --- Structured Data ---
    sd = sections.get("structured_data", {}).get("details", {})
    matched = sd.get("valuable_schemas_matched", [])
    missing_schemas = [s for s in ["Organization", "Product", "FAQPage", "BreadcrumbList", "AggregateRating", "ItemList"] if s not in matched]
    if missing_schemas:
        add("structured_data", "high",
            f"Add JSON-LD schemas: {', '.join(missing_schemas[:4])}",
            f"Structured data lets LLMs extract precise facts about your brand and products. Missing: {', '.join(missing_schemas)}. Implement JSON-LD in the <head> — use Google's Rich Results Test to verify. Priority: Organization (brand facts), Product (for category pages), FAQPage (for Q&A content).",
            "medium")
    if not sd.get("has_json_ld"):
        add("structured_data", "high",
            "No JSON-LD found — implement structured data from scratch",
            "Your site has no machine-readable structured data. Start with an Organization schema on every page, then add Product schemas on product/category pages. Google's structured data documentation and schema.org are your references.",
            "medium")

    # --- Content & E-E-A-T ---
    ce = sections.get("content_eeat", {}).get("details", {})
    if not ce.get("good_heading_structure"):
        h1 = ce.get("h1_count", 0)
        add("content_eeat", "medium",
            f"Fix heading structure (found {h1} H1 tags, expected exactly 1)",
            "LLMs extract page topics from headings. Each page should have exactly one H1 (the main topic) and multiple H2s that break down subtopics. Missing or duplicate H1s confuse both LLMs and traditional search.",
            "low")
    if not ce.get("faq_detected"):
        add("content_eeat", "high",
            "Add FAQ sections to key pages",
            "FAQ content directly maps to conversational AI queries. Add a FAQ section to your homepage, category pages, and top product pages. Use FAQPage JSON-LD schema alongside it. Target 5–10 questions per page covering common customer queries.",
            "low")
    if not ce.get("about_page_linked"):
        add("content_eeat", "medium",
            "Add a clearly linked About page",
            "An About page signals brand legitimacy and helps LLMs build an accurate entity profile for your company. Include founding date, mission, key facts, and press mentions. Link it prominently in the header or footer.",
            "low")
    if not ce.get("author_signals"):
        add("content_eeat", "medium",
            "Add author attribution to editorial content",
            "E-E-A-T (Experience, Expertise, Authoritativeness, Trust) matters for LLM citation likelihood. For blog posts, guides, and reviews — add named authors with credentials. Use Person schema to reinforce this.",
            "low")

    # --- LLM Access ---
    la = sections.get("llm_access", {}).get("details", {})
    if not la.get("llms_txt"):
        add("llm_access", "high",
            "Create /llms.txt",
            "llms.txt is an emerging standard (like robots.txt for LLMs) that tells AI crawlers what your site is about and what they can use. Create a plain-text file at yourdomain.com/llms.txt with a concise brand/product description, key pages, and contact info. Early adoption is a competitive advantage.",
            "low")
    if not la.get("llms_full_txt"):
        add("llm_access", "medium",
            "Create /llms-full.txt",
            "llms-full.txt is a verbose companion to llms.txt — it provides AI crawlers with rich context: full product catalogue summaries, FAQs, brand story. Think of it as a briefing document for AI systems.",
            "low")
    blocked = la.get("ai_bots_blocked", [])
    if blocked:
        add("llm_access", "high",
            f"Unblock AI crawlers in robots.txt: {', '.join(blocked)}",
            f"Your robots.txt is blocking the following AI crawlers: {', '.join(blocked)}. These bots index your content for LLM training and retrieval. Unless you have a specific legal reason, unblocking them is essential for GEO.",
            "low")

    # --- Discoverability ---
    disc = sections.get("discoverability", {}).get("details", {})
    if not disc.get("sitemap_found"):
        add("discoverability", "high",
            "Create and submit a sitemap.xml",
            "A sitemap helps AI crawlers discover all your pages systematically. Generate one at /sitemap.xml covering all canonical URLs. Submit it in Google Search Console and reference it in robots.txt with 'Sitemap: https://yourdomain.com/sitemap.xml'.",
            "low")
    if not disc.get("meta_description"):
        add("discoverability", "medium",
            "Add meta descriptions to all pages",
            "Meta descriptions are used by LLMs to understand page intent before crawling. Each page should have a unique, 150–160 character description that includes the primary entity and value proposition.",
            "low")
    if not disc.get("open_graph"):
        add("discoverability", "low",
            "Add Open Graph tags",
            "OG tags (og:title, og:description, og:image) are used by social platforms and increasingly by AI systems to understand page content. Add them to all key pages.",
            "low")

    # Sort by priority
    priority_order = {"high": 0, "medium": 1, "low": 2}
    recs.sort(key=lambda r: priority_order.get(r["priority"], 3))
    return recs
