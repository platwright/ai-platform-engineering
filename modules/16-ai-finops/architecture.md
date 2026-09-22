# Module 16 Architecture

## Cost Attribution Flow

```mermaid
flowchart LR
    Request[User Request] --> GW[AI Gateway]
    GW -- "prompt_tokens\ncompletion_tokens\ntenant\nmodel" --> Log[Request Log]
    Log --> Aggregator[Cost Aggregator\nScript / Service]
    Aggregator -- "per-tenant\nper-model\nper-day" --> Report[Cost Report]
    Report --> Dashboard[FinOps Dashboard]
    Report --> Chargeback[Chargeback to Teams]
```

## Cost Composition

```mermaid
pie title AI Platform Cost Composition (example)
    "Model API (hosted)" : 65
    "GPU serving (self-hosted)" : 20
    "Embedding service" : 8
    "Vector DB" : 4
    "Other infra" : 3
```

## Break-Even Analysis

```mermaid
xychart-beta
    title "Hosted API vs Self-Hosted Cost by Monthly Token Volume"
    x-axis ["10M", "50M", "100M", "500M", "1B", "5B"]
    y-axis "Monthly Cost ($)" 0 --> 80000
    line [150, 750, 1500, 7500, 15000, 75000]
    line [3500, 3700, 4000, 4800, 6000, 12000]
```

Note: hosted API cost scales linearly with tokens; self-hosted has fixed hardware cost plus small variable cost. Break-even is typically 100M–500M tokens/month for common model tiers.

## Cost Optimization Levers

```mermaid
flowchart TD
    CostProblem[AI Costs Too High]
    CostProblem --> L1[Route cheap requests\nto smaller models]
    CostProblem --> L2[Enable prompt caching\nfor repeated prefixes]
    CostProblem --> L3[Reduce system prompt length]
    CostProblem --> L4[Set tighter max_tokens\nlimits per use case]
    CostProblem --> L5[Self-host high-volume\nworkloads]
    CostProblem --> L6[Dev/staging quotas\nto avoid waste]

    L1 --> Eval{Eval score\nstill OK?}
    L2 --> Eval
    L3 --> Eval
    Eval -- "yes" --> Deploy[Deploy change]
    Eval -- "no" --> Revert[Revert, investigate]
```
