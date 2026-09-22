# Module 16 Challenge

## Challenge 1 - Full Cost Inventory

Build a complete cost inventory for the Acme AI platform at 1,000 requests/day.

Research current pricing and estimate monthly costs for each component:

1. Model inference (GPT-4o mini, at your estimated token counts)
2. Embedding service (for RAG queries — estimate tokens per query)
3. Vector database (choose a representative managed option: Pinecone, Qdrant Cloud, or pgvector)
4. Evaluation judge model calls (monthly eval run, 200 cases, LLM judge)
5. GPU inference (if 30% of traffic routes to self-hosted Llama 8B)

Present as a table with per-component cost, % of total, and one optimization note per component.

## Challenge 2 - Break-Even Analysis

Write a Python script that computes the monthly break-even volume for switching from hosted GPT-4o mini to self-hosted Llama 3.1 8B.

The script should:
- Accept GPU instance cost, hourly rate, and utilization as parameters
- Compute self-hosted cost per million tokens at that utilization
- Compute hosted API cost per million tokens
- Find the token volume where self-hosted becomes cheaper
- Print the result including all assumptions

Run the analysis for three utilization scenarios: 40%, 70%, and 90%.

## Challenge 3 - Per-Tenant Cost Report

Extend the `eval/cost_report.py` script to:

1. Add a simulated `tenant` field to run artifacts (or read it from artifact metadata if present)
2. Group costs by tenant and produce a per-tenant summary
3. Calculate each tenant's share of total cost as a percentage
4. Flag any tenant whose cost exceeds 50% of total (concentration risk)
5. Output a Markdown table suitable for a monthly showback report

## Challenge 4 - Environment Cost Controls

Design an environment cost control policy for the Acme AI platform.

Document in `my-solutions/module-16-env-controls.md`:

1. Dev environment: what model tier, what token quota per developer per month, shutdown policy
2. Staging environment: what model tier, what token quota, how different from production
3. CI environment: what model tier, whether to use batch API, how to manage eval cost
4. Production: how to alert on cost anomalies, what constitutes a cost incident

For each environment, estimate the expected monthly cost at your projected usage volume.

## Challenge 5 - FinOps Dashboard Design

Design a three-row FinOps dashboard for the Acme AI platform:

Row 1: Real-time cost visibility
- What 3 panels show current cost rate and trend?

Row 2: Per-tenant breakdown
- What 2 panels show cost distribution across tenants?

Row 3: Optimization metrics
- What 3 panels show whether cost controls are working (cache hit rate, routing effectiveness, GPU utilization)?

For each panel, write the metric or query it would display.
