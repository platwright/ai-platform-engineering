# Module 14 Lab

## Goal

Define SLOs for the sample-chat application, simulate two failure modes, and write a basic incident runbook.

## Prerequisites

- Project 01 and sample-chat running locally
- Project 03 running with at least one ingested RAG service
- Python 3.11+

## Step 1 - Define SLOs For The Sample-Chat Application

Based on the chapter material and what you know about the application's behavior, write SLO definitions in `my-notes/module-14-slos.md`:

Define three SLOs:

1. **Availability SLO**: what fraction of requests must succeed (not return 5xx)?
2. **Latency SLO**: what TTFT threshold must what fraction of requests meet?
3. **Quality SLO**: what eval pass rate must the application maintain (use the eval runner from Module 11)?

For each SLO, write:
- The SLI formula (what is being measured)
- The target value
- The error budget (what is allowed to violate the SLO)
- How you would measure it with the current tooling

## Step 2 - Simulate A Provider Timeout

Configure Project 01 to use the rate-limited mock provider, which introduces artificial delay:

```bash
python projects/project-01-model-api/app.py chat \
  --provider acme-rate-limited \
  --message "Explain what backpressure means in AI serving."
```

Observe:
- How long does the request take?
- What error does the application return?
- Is there a retry in the response time?

Now examine the provider configuration in `projects/project-01-model-api/config/app.example.json`. Identify:
- Is there a configured timeout for this provider?
- Is there a retry policy?
- Is there a fallback provider configured?

Write down what would need to change to implement the retry-with-backoff pattern from the chapter.

## Step 3 - Simulate A Retrieval Degradation

Check the current RAG index staleness by looking at the index file modification time:

```bash
# Find the RAG state directory
Get-ChildItem projects/project-03-rag-platform/state/ -Recurse
# On Unix:
ls -la projects/project-03-rag-platform/state/
```

Note the modification timestamp. Run a query:

```bash
python projects/project-03-rag-platform/app.py query \
  --service-name team-a-kb \
  --question "What is retrieval freshness?"
```

Now simulate index staleness: move or rename the index file and query again:

```bash
# Temporarily rename the index
mv projects/project-03-rag-platform/state/team-a-kb.json \
   projects/project-03-rag-platform/state/team-a-kb.json.bak
```

Run the same query. What happens?

Restore the index and document what the system should do when the index is missing (degrade gracefully or fail hard?):

```bash
mv projects/project-03-rag-platform/state/team-a-kb.json.bak \
   projects/project-03-rag-platform/state/team-a-kb.json
```

## Step 4 - Simulate Approval Gate Reliability

Verify the approval gate in Project 04 behaves correctly under boundary conditions:

```bash
# Should block (no token)
python projects/project-04-agent-platform/app.py run \
  --objective "Delete the team-a-kb service" --service-name team-a-kb

# Should allow (valid token)
python projects/project-04-agent-platform/app.py run \
  --objective "Delete the team-a-kb service" --service-name team-a-kb \
  --approval-token approved:delete-rag-service
```

Confirm both behaviors are correct and the run artifacts capture the outcome.

## Step 5 - Write An Incident Runbook

Write a runbook for one of the failure modes you simulated in `my-notes/module-14-runbook.md`.

Use the runbook structure from Chapter 08:
- Symptoms
- Immediate Actions (first 5 minutes)
- Diagnosis Tree
- Mitigation Options
- Verification
- Escalation criteria

## Step 6 - Reflection

In `my-notes/module-14.md`:

1. What is the most important gap in the current sample application's reliability posture?
2. Describe a scenario where the application would silently produce degraded outputs without any observable error. How would you detect it?
3. If you could add only one reliability feature to the existing stack, what would it be and why?
