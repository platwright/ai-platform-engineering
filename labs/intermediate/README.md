# Intermediate Labs

Labs that combine multiple platform concepts. Intermediate labs typically require Docker Compose or Kubernetes and involve more than one running service.

## Available Labs

Labs in this area will be added alongside Modules 04 through 10.

### Planned

- **multi-provider-routing**: run three mock providers behind the AI gateway and observe routing decisions and fallback behavior under simulated provider failures — covers Modules 03 and 08
- **rag-freshness**: ingest a document set, query it, then update a document and query again — observe the staleness window and how re-ingestion affects results — covers Module 09
- **gateway-rate-limit-observe**: send requests above the configured rate limit and observe how the gateway response and usage metrics change — covers Module 08
- **k8s-rollout-chat**: deploy the sample-chat application to a local Kubernetes cluster and perform a rolling update — covers Modules 04 and 05
- **agent-tool-audit**: run the agent platform with several objectives and review the tool call log for decision quality and authorization boundary verification — covers Module 10
- **context-window-pressure**: progressively grow the conversation history in a chat session and observe how performance and cost change as the context window fills — covers Module 02

## Prerequisites For Intermediate Labs

- Docker and Docker Compose
- A local Kubernetes cluster (kind or k3d) for Kubernetes-specific labs
- Project 01 through the relevant project running locally
- Basic familiarity with the module concepts the lab builds on

## Format

Each intermediate lab has its own subdirectory with a README, any necessary config overrides, and a cleanup script. Start with the lab README.
