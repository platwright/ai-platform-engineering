# Module 11 Verification

## Check 1 - LLMOps Conceptual Understanding

Answer without looking at the chapters:

1. Name three things that LLMOps adds on top of standard MLOps.
2. Why is exact-match scoring insufficient for evaluating open-ended LLM outputs?
3. What is "silent model drift" and how do you detect it?

## Check 2 - Evaluation Script

Confirm the eval runner from the lab is working:

```bash
python eval/run_eval.py \
  --dataset eval/datasets/rag-smoke.json \
  --service-name team-a-kb \
  --threshold 0.60
```

- [ ] Script runs without errors
- [ ] Script outputs per-case pass/fail status
- [ ] Script outputs an aggregate pass rate
- [ ] Script exits with code 1 when the threshold is not met (test by lowering threshold to 0.99)

```bash
# Verify exit code behavior
python eval/run_eval.py --dataset eval/datasets/rag-smoke.json --service-name team-a-kb --threshold 0.99
echo "Exit code: $?"  # Should be 1
```

## Check 3 - Prompt Versioning

Confirm you can describe a prompt versioning workflow:

- [ ] You can explain what fields a prompt version record should contain
- [ ] You can describe the promotion workflow from dev to production
- [ ] You can explain how a rollback to the previous version would work
- [ ] You can show where the model pin should be stored relative to the prompt version

## Check 4 - Regression Simulation

Verify you can detect a regression:

1. Note the current eval pass rate
2. Modify the RAG system configuration to degrade output (e.g., reduce retrieved context, simplify the system prompt)
3. Rerun the eval
4. Confirm the pass rate dropped

- [ ] Pass rate dropped detectably after the degradation
- [ ] You can explain which cases failed and why
- [ ] You can explain what would trigger an automatic CI block in this scenario

## Check 5 - CI Gate Understanding

Without looking at the chapter, sketch a CI pipeline for an AI application. Include:

- [ ] What triggers the pipeline
- [ ] What the smoke eval stage does and when it blocks
- [ ] What the full eval stage does and when it runs
- [ ] What artifacts the pipeline produces
- [ ] How a failed eval differs from a regular test failure in terms of team response

## Check 6 - Human Feedback

Confirm you can explain:

- [ ] The difference between implicit and explicit feedback
- [ ] How negative feedback becomes an eval dataset case
- [ ] Why human feedback alone is not sufficient to measure quality
- [ ] What privacy concern applies to production feedback data
