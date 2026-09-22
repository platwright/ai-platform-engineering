# Module 03 Solution

This solution guide focuses on what your reasoning and project behavior should show.

## Expected Conceptual Outcomes

You should finish the module with these ideas clear:

- an AI application is more than a model call; it has application, orchestration, provider, and state concerns
- statefulness is not a property to accept casually; it is a design choice to make explicit
- synchronous and asynchronous AI paths should not share the same assumptions about latency and user experience
- configuration materially changes AI behavior and belongs under disciplined control
- twelve-factor principles still apply, but prompts, models, and evaluations become part of the runtime contract

## Expected Project 01 Behavior

The same application interface should be able to:

- list multiple provider aliases
- send a chat request to different providers without changing the application code path
- produce a normalized response shape across success and failure cases
- optionally expose the same behavior over a local HTTP API

## Strong Workbook Answers Usually Include

- prompts treated as explicit files or artifacts
- provider transport hidden behind adapters
- state moved to explicit stores rather than application memory
- asynchronous work proposed for indexing or batch jobs, not user-facing chat
- configuration separated from code for models, prompts, and request defaults

## Project Interpretation

Project 01 is not a full AI gateway yet. It is an application-level abstraction that prepares the path for later platform capabilities such as routing, policy, fallback, and quotas.