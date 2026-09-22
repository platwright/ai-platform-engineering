# Module 14 Verification

## Check 1 - Reliability Dimensions

Without looking at the chapter, name the two reliability dimensions for AI systems and give one SLI example for each.

## Check 2 - Failure Taxonomy

Classify each scenario into the correct taxonomy category:

1. The model server container restarts due to CUDA OOM
2. The gateway returns HTTP 200 but the response contains no retrieved context because the RAG index was stale
3. The prompt was updated but the new version causes responses to be much shorter than expected
4. OpenAI's API is returning 500 errors for all requests
5. One tenant's runaway batch job fills the request queue, causing other tenants to time out

## Check 3 - SLO Design

Your SLOs from the lab:
- [ ] Each SLO has a specific measurable SLI
- [ ] Each SLO has a numeric target
- [ ] You can calculate the error budget for each
- [ ] At least one quality SLO is included alongside technical SLOs

## Check 4 - Retry Policy

Answer without looking at the chapter:

1. Why is fixed-interval retry harmful in a multi-client environment?
2. What does "jitter" add to exponential backoff and why?
3. Should a 400 Bad Request be retried? Why or why not?
4. What is the risk of retrying an agent tool execution that partially completed?

## Check 5 - Circuit Breaker

Draw the three states of a circuit breaker and the transitions between them. Explain what each state means for incoming requests.

## Check 6 - Failure Simulation

Confirm your failure simulations from the lab:
- [ ] Provider timeout simulation produced a visible delay or error
- [ ] Missing RAG index produced a specific behavior (error or degraded response)
- [ ] You documented what should happen vs what did happen
- [ ] You identified at least one improvement to make the failure behavior better

## Check 7 - Incident Runbook

Your runbook from the lab:
- [ ] Has a clearly described symptom section
- [ ] Has immediate action steps that can be done in < 5 minutes
- [ ] Has a branching diagnosis tree (not just a linear list)
- [ ] Has at least two mitigation options
- [ ] Has verification steps

## Check 8 - Quality Incident Declaration

You should be able to explain:
- [ ] Why quality incidents produce no HTTP error code
- [ ] What trigger conditions justify declaring a quality incident
- [ ] What the first three steps are after declaring a quality incident
- [ ] How a quality incident post-mortem differs from a technical incident post-mortem
