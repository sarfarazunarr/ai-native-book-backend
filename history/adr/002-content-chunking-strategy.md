# ADR-002: Content Chunking Strategy for Embedding

**Title**: Content Chunking Strategy for Embedding
**Status**: Accepted
**Date**: 2025-12-17

## Context

The system needs to break down the book content into appropriately sized chunks before creating embeddings with Cohere. This is crucial for maintaining semantic meaning while fitting within model constraints. The chunking approach will affect retrieval quality and the ability to cite specific sources in responses.

## Decision

We will use Recursive Character Text Splitter with configurable chunk size and overlap to maintain semantic context while optimizing for Cohere embeddings.

Specifically:
- Implementation: `RecursiveCharacterTextSplitter` with multiple separators
- Default chunk size: 1000 characters
- Overlap: 200 characters to maintain context across chunks
- Separators: ['#', '##', '###', '\n\n', '\n', '.', ' ', '']

## Alternatives Considered

1. **Recursive Character Text Splitter**: Breaks text recursively by separators, maintains semantic meaning
   - Pros: Maintains context by breaking at meaningful boundaries, configurable separators, preserves document structure
   - Cons: More complex than simple fixed-size splitting, requires tuning

2. **Fixed-Size Chunking**: Simple character/word count splitting
   - Pros: Simple implementation, predictable chunk sizes, uniform processing
   - Cons: May break context mid-sentence, semantic meaning lost at boundaries, poor citation accuracy

3. **Semantic Chunking**: Uses embeddings to determine semantic boundaries
   - Pros: Most contextually coherent chunks, optimal semantic boundaries
   - Cons: More computationally expensive, complex implementation, higher latency during ingestion

## Consequences

**Positive:**
- Maintains semantic meaning across chunk boundaries
- Allows for accurate citation of specific content sections
- Balances computational efficiency with contextual preservation
- Configurable parameters for optimization

**Negative:**
- More complex implementation than fixed-size chunks
- Requires parameter tuning for optimal performance
- May still have some context breaks at chunk boundaries
- Slightly higher processing time during ingestion

## References

- plan.md: Implementation Steps mentions "Implement content chunking logic"
- research.md: Notes "Determine optimal chunking strategies for book content"