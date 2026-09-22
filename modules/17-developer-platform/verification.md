# Module 17 Verification

## Check 1 - Self-Service Design

Without looking at the chapter, explain in two sentences:
- What makes a platform genuinely self-service vs documentation-dependent?
- Why does self-service not mean self-management?

## Check 2 - Catalog Files

Confirm your catalog YAML files are syntactically valid:

```bash
# Validate YAML syntax
python -c "import yaml; yaml.safe_load(open('platform/backstage/catalog/ai-gateway.yaml'))"
python -c "import yaml; yaml.safe_load(open('platform/backstage/catalog/rag-platform.yaml'))"
```

- [ ] No YAML errors
- [ ] Each file has `apiVersion`, `kind`, `metadata.name`, `spec.type`, `spec.owner`
- [ ] AI gateway references an API component
- [ ] API component has a definition with at least one path

## Check 3 - Golden Path Template

Review your template YAML:

- [ ] Has at least 3 required parameters
- [ ] Has input validation (required fields, pattern constraint on appName)
- [ ] Has at least 3 scaffolder steps
- [ ] Produces at least 5 files in the skeleton
- [ ] The skeleton files use `${{ values.paramName }}` substitution correctly

## Check 4 - Onboarding Flow

Your onboarding flow from the lab:

- [ ] Has exactly 6 steps
- [ ] Each step has a clear expected outcome
- [ ] Each step has an error condition with an actionable message
- [ ] You estimate total TTFV under 60 minutes
- [ ] No step requires contacting the platform team

## Check 5 - API Stability

Explain without looking at the chapter:

1. What is the minimum deprecation notice period for a stable platform API endpoint?
2. What HTTP header communicates deprecation to API consumers?
3. What response code should a fully-sunsetted endpoint return?

## Check 6 - Governance Design

Your governance policy from the lab:

- [ ] Has at least three distinct categories (no review / async review / sync review)
- [ ] Each category has specific, concrete criteria (not vague)
- [ ] The exception process has a time bound
- [ ] At least one governance requirement is implemented as a guardrail (automated check)

## Check 7 - Team Topologies

Match each interaction mode to the correct scenario:

1. A platform engineer pair-programs with an application team for 2 weeks to help them adopt the new agent platform capability → _____
2. A team creates a new RAG service by filling in a Backstage template and clicking "Create" → _____
3. Two teams work together for 3 months to design the new model routing API → _____

## Check 8 - Platform Metrics

Name three metrics that would tell you the platform onboarding experience degraded after a platform change.
