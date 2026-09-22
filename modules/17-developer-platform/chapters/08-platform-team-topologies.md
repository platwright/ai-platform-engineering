# Chapter 08 - Platform Team Topologies

## What Team Topologies Is

Team Topologies is a framework for organizing software teams to reduce cognitive load and improve flow. It identifies four team types and three interaction modes, and provides clear guidance about when each applies.

The framework is directly relevant to platform engineering because the relationship between a platform team and the teams it serves is one of its primary design concerns.

## The Four Team Types

### Stream-Aligned Teams

Teams aligned to a flow of work — a product, a customer segment, a feature area. These teams deliver value directly. In the Acme AI context, application teams building products for end users are stream-aligned teams.

### Platform Teams

Teams that enable stream-aligned teams to deliver with higher autonomy and lower cognitive load. The platform team builds and operates the AI platform. Its outputs are services, APIs, templates, and documentation that stream-aligned teams consume.

The platform team's goal: reduce the cognitive load of AI infrastructure on every application team.

### Enabling Teams

Specialist teams that temporarily assist stream-aligned or platform teams to acquire new capabilities. For AI platform work, an enabling team might be a group of AI engineers who help application teams adopt new model capabilities before those capabilities are productized into the platform.

### Complicated Subsystem Teams

Teams that own parts of the system that require deep specialist knowledge to develop and maintain. A GPU cluster operations team or a vector database performance team might be complicated subsystem teams.

## The Three Interaction Modes

### Collaboration Mode

Two teams work closely together for a limited period to achieve a specific outcome. Used when building new platform capabilities that require input from both platform and application teams.

### X-as-a-Service Mode

One team consumes the output of another team with minimal interaction. This is the steady-state mode between the platform team and application teams: application teams consume AI platform capabilities without needing to understand how they work internally.

### Facilitating Mode

One team helps another team become more effective. Used temporarily when introducing new platform capabilities that application teams need support to adopt.

## Platform Team Size and Staffing

A rough guide to platform team sizing:

| Developers Served | Platform Team Size |
|---|---|
| < 20 | 2–3 engineers, part-time platform focus |
| 20–50 | 3–5 dedicated platform engineers |
| 50–200 | 5–10 engineers, some specialization |
| 200+ | Multiple platform sub-teams by domain |

The AI platform domain may warrant a dedicated sub-team at scale, distinct from a broader platform engineering team.

## When To Split The Platform Team

A single platform team serving both core infrastructure (Kubernetes, CI/CD) and AI-specific capabilities eventually splits under the load. Split signals:

- AI platform changes require different expertise from core infrastructure changes
- Context switching between the two domains reduces quality in both
- Response time for AI-specific requests is unacceptably slow due to queue mixing

When to split: when the two domains have divergent skill requirements and different natural change cadences.

## The Inverse Conway's Law

Conway's Law: systems reflect the communication structure of the organizations that build them. Applied to platform design: if you want a well-integrated AI platform, the platform team must be organized in a way that encourages cross-capability thinking rather than siloed component ownership.

A platform team where each engineer "owns" one component (one person for the gateway, one for RAG, one for agents) produces components that are individually good but poorly integrated. Rotate ownership, run design reviews across capabilities, and explicitly document the interfaces between components.

## Evolving The Topology

Platform team topology should evolve with the organization:

- **Early stage**: one or two platform engineers helping teams ad hoc
- **Growth stage**: dedicated platform team in X-as-a-Service mode, golden paths available
- **Scaled stage**: platform sub-teams by domain (AI platform, CI/CD, data platform)
- **Enterprise stage**: product management, developer relations, and engineering in the platform organization

The transition from one stage to the next requires deliberate organizational design, not just adding headcount.
