# ADR-004: Agent Memory and Session Management

**Title**: Agent Memory and Session Management
**Status**: Accepted
**Date**: 2025-12-17

## Context

The OpenAI Agents SDK needs to maintain conversational context for multi-turn conversations with users. This is important for providing coherent responses when users ask follow-up questions or refer to previous parts of the conversation. The system needs to balance conversation continuity with resource efficiency and privacy considerations.

## Decision

We will implement session-based memory management using the OpenAI Agents SDK's built-in conversation threading capabilities. Each user session will be identified by a UUID and maintained for the duration of the interaction.

Specifically:
- Implementation: Use OpenAI's `thread` concept for conversation continuity
- Session persistence: Store conversation history in the ChatSession entity in the database
- Session lifetime: No automatic expiration, but clients can start new sessions as needed
- Privacy: Clear conversation history can be achieved by starting a new session ID

## Alternatives Considered

1. **OpenAI Thread-based Memory**: Use OpenAI's native thread system for conversation history
   - Pros: Native integration with OpenAI Agents, handles context automatically, maintained by OpenAI
   - Cons: Dependent on OpenAI's service, potential costs based on usage, less control over retention

2. **Custom In-Memory Storage**: Maintain conversation state in application memory
   - Pros: Full control over session lifecycle, potentially faster access, cost-effective for short sessions
   - Cons: Not persistent across deployments, memory consumption with many sessions, potential data loss

3. **Database-Backed Sessions**: Store conversation history in the application database
   - Pros: Persistent across deployments, full control over retention, auditable conversations
   - Cons: More complex implementation, potential privacy considerations, additional database load

## Consequences

**Positive:**
- Natural conversation flow with context awareness
- Automatic handling of conversation history by OpenAI's system
- Scalable solution managed by OpenAI infrastructure
- Can maintain context throughout complex multi-turn conversations

**Negative:**
- Dependent on OpenAI's external service for memory management
- Potential privacy concerns for sensitive conversations
- Additional costs associated with OpenAI thread usage
- Less control over specific memory management policies

## References

- plan.md: Implementation Steps mentions "Implement session handling for conversations"
- plan.md: API Contracts specify optional "session_id" parameter for the chat endpoint
- data-model.md: Defines the ChatSession entity for storing conversation history