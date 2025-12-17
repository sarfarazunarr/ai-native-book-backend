# ADR-003: Search Strategy with Relevance Threshold

**Title**: Search Strategy with Relevance Threshold
**Status**: Accepted
**Date**: 2025-12-17

## Context

The system needs to perform similarity searches in the vector database (Qdrant) to retrieve relevant book content for answering user queries. Without proper relevance controls, the agent might use irrelevant results, leading to hallucinations or inaccurate answers when no relevant content exists for a query.

## Decision

We will implement Qdrant's search with a configurable relevance threshold to prevent the agent from using irrelevant results. The search will return results only if their similarity score exceeds a minimum threshold, otherwise the agent will respond appropriately indicating no relevant content was found.

Specifically:
- Implementation: Use Qdrant's `search_params` with a configurable `score_threshold`
- Default threshold: 0.7 (on a 0-1 scale)
- Response behavior: When no results meet threshold, respond with "I couldn't find relevant information about this topic in the book"

## Alternatives Considered

1. **Threshold-based Search**: Only return results above a minimum similarity threshold
   - Pros: Prevents hallucinations, maintains accuracy, clear signal when content isn't available
   - Cons: May need frequent threshold tuning, could miss relevant content with lower scores

2. **Top-k Only**: Return top-k results regardless of similarity score
   - Pros: Simple implementation, always provides some results
   - Cons: Risk of hallucination with poor matches, may provide inaccurate information

3. **Score-based Ranking**: Always return results but rank by score, with score visibility to agent
   - Pros: More nuanced approach, allows agent to handle low-confidence results
   - Cons: Relies on agent handling low-confidence responses properly, still potential for hallucination

## Consequences

**Positive:**
- Reduces hallucinations when no relevant content exists
- Maintains accuracy of responses by filtering low-quality matches
- Provides clear user feedback when information isn't available in the source
- Prevents the system from making up information

**Negative:**
- May result in more "no answer found" responses
- Requires tuning of threshold value based on testing
- Could miss relevant content if threshold is set too high
- Additional complexity in response logic

## References

- plan.md: Implementation Steps mentions "Implement similarity search functionality"
- plan.md: Risk Analysis notes "Query response quality: Agent may provide inaccurate responses"
- data-model.md: VectorEmbedding contains metadata including source references