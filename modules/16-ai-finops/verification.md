# Module 16 Verification

## Check 1 - Cost Calculation

Without a calculator, estimate: a team sends 5,000 requests/day with 1,500 avg input tokens and 400 avg output tokens using GPT-4o mini ($0.15/M input, $0.60/M output).

- Daily cost?
- Monthly cost?
- Annual cost?

If you cannot do this quickly from memory, re-read Chapter 02.

## Check 2 - Cost Report Script

Confirm your cost report works:

```bash
python eval/cost_report.py
```

- [ ] Script reads run artifacts without errors
- [ ] Output shows cost per provider
- [ ] Output shows total cost across all requests
- [ ] You can explain why the numbers are what they are

## Check 3 - Routing Simulation

Confirm you ran the routing simulation from the lab:
- [ ] You have numbers for all-fast, all-smart, and 80/20 blended scenarios
- [ ] You calculated the percentage savings of 80/20 vs all-smart
- [ ] You can explain why the savings are not exactly 80%

## Check 4 - GPU Utilization

Explain without looking at the chapter:

1. An A10G costs $1.50/hour and runs at 30% utilization. What is the effective per-hour cost?
2. What are two practical ways to improve GPU utilization in a development environment?
3. Why is 100% GPU utilization not necessarily the target?

## Check 5 - Break-Even Intuition

You should be able to explain in one paragraph:
- [ ] Why self-hosting is cheaper per token at high volume
- [ ] Why it is more expensive per token at low volume
- [ ] What factors shift the break-even point

## Check 6 - Caching ROI

You have a RAG application where users sometimes ask the same question. The question embedding takes 100 tokens. The full RAG request costs $0.002.

- If semantic cache hit rate is 5%, does caching save or lose money?
- What hit rate makes caching cost-neutral?
- What hit rate would you need to see before adding semantic caching complexity?

## Check 7 - Chargeback Basics

Describe the difference between showback and chargeback. Which should you implement first and why?

## Check 8 - Environment Controls

List three specific cost control measures that should be applied to development environments but NOT production environments.
