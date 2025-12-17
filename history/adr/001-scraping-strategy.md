# ADR-001: Scraping Strategy for Book Content Extraction

**Title**: Scraping Strategy for Book Content Extraction
**Status**: Accepted
**Date**: 2025-12-17

## Context

The system needs to extract clean text content from the Physical AI & Humanoid Robotics book website, which is built with Docusaurus. The content extraction must remove navigation, footer, and other boilerplate elements while preserving the actual book content. The site may contain JavaScript-rendered content that requires client-side execution.

## Decision

We will use BeautifulSoup with httpx for server-side content extraction, with the option to implement Playwright as a fallback for JavaScript-heavy sections if needed.

Specifically:
- Primary approach: `BeautifulSoup` with `httpx` for efficient async scraping
- Fallback approach: `Playwright` if content is determined to be JS-heavy after initial testing

## Alternatives Considered

1. **BeautifulSoup + httpx**: Standard approach for static content, faster, lighter, handles most Docusaurus sites well
   - Pros: Lightweight, async support, mature ecosystem, good for mostly static content
   - Cons: Cannot execute JavaScript, might miss dynamic content

2. **Playwright**: Full browser automation, can execute JavaScript, handles complex sites
   - Pros: Handles JavaScript-rendered content, can interact with the page
   - Cons: Heavier resource usage, more complex setup, slower execution, potential scalability issues

3. **Selenium**: Another full browser automation option
   - Pros: Mature, handles JavaScript well
   - Cons: Heavier than Playwright, more resource intensive, slower execution

## Consequences

**Positive:**
- BeautifulSoup approach will be faster and more resource-efficient for the common case
- Can handle async requests efficiently with httpx
- Lower operational costs due to reduced resource requirements
- Simpler debugging and maintenance

**Negative:**
- May require additional implementation if JavaScript-heavy content is encountered
- Potential need to maintain two scraping strategies
- Risk of missing content that requires JavaScript execution

## References

- plan.md: Implementation Steps section mentions "async scraping logic with httpx and BeautifulSoup"
- research.md: Notes "Study BeautifulSoup HTML cleaning techniques for Docusaurus sites"