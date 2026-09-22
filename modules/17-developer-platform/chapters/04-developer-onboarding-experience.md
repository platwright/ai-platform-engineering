# Chapter 04 - Developer Onboarding Experience

## What Onboarding Is

Platform onboarding is the journey a developer takes from "I want to use this platform" to "my application is running successfully and calling the platform." The quality of this journey determines initial adoption and sets expectations for everything that follows.

A good onboarding experience is:
- **Fast**: time-to-first-value is measured in minutes, not days
- **Self-sufficient**: the developer completes it without asking for help
- **Verifiable**: each step has a clear success signal
- **Recoverable**: when something goes wrong, the error message explains how to fix it

## Time-To-First-Value (TTFV)

TTFV is the elapsed time from when a developer decides to try the platform until they see their first successful response from a platform service.

Target TTFV for different experience levels:

| Developer Type | Target TTFV |
|---|---|
| Experienced AI developer | < 30 minutes |
| Experienced backend developer, new to AI | < 2 hours |
| Junior developer following the golden path | < 4 hours |

Measure TTFV by observing real developer onboarding sessions or by running a timed onboarding exercise with a developer unfamiliar with the platform.

## The Onboarding Flow

A well-designed AI platform onboarding:

```
1. Access the developer portal
   → Find the AI Platform section
   → Read the 2-minute overview (not the full documentation)

2. Register your team as a tenant
   → Fill in team name, primary contact, use case
   → Receive API credentials immediately (automated)

3. Run the quickstart
   → Copy-paste a 3-line curl command
   → See "Hello from the AI Platform!" within 60 seconds

4. Follow your first golden path
   → Pick the template that matches your use case
   → Fill in 5 parameters
   → Click "Create" → git repository appears in your GitHub org

5. Run the template locally
   → Clone the repository
   → Follow the local setup (< 5 commands)
   → Application calls the platform and returns a response

6. Review your first usage metrics
   → Developer portal shows token usage and cost from step 5
```

Each step has a clear expected outcome. Steps that fail have error messages pointing to the fix, not to a generic "contact support" message.

## Documentation Design

Developer documentation fails when it:
- is organized by platform components instead of developer goals
- requires reading everything before trying anything
- uses internal platform team vocabulary instead of developer vocabulary
- has no examples

Effective platform documentation:
- starts with a quickstart that produces a visible result in under 5 minutes
- uses task-oriented sections: "How to add RAG to your app", not "RAG platform architecture"
- puts examples before explanations, not after them
- is searchable by what developers actually type (error messages, feature names, use cases)

## The "Getting Stuck" Problem

Every developer who gets stuck during onboarding and does not complete it is a failed adoption. Common stuck points:

| Stuck Point | Common Cause | Fix |
|---|---|---|
| Can't get credentials | Manual process, no automation | Automate credential provisioning |
| First request fails with 401 | Auth documentation is wrong or incomplete | Fix documentation, add troubleshooting |
| Local development stack won't start | Prerequisites not listed | List all prerequisites explicitly with versions |
| Quickstart works, template breaks | Template is outdated | Test templates in CI on every platform change |
| Error message is unhelpful | "Internal server error" tells nothing | Return actionable error messages |

Instrument the onboarding flow. Where do API calls drop off? Where do error rates spike? Those are the stuck points.

## Onboarding Success Metrics

| Metric | Measurement | Target |
|---|---|---|
| TTFV p50 | Time from signup to first successful API call | < 60 minutes |
| Onboarding completion rate | % of teams who complete all 6 onboarding steps | > 80% |
| First-week active use | % of onboarded teams still active after 7 days | > 70% |
| Support requests per new team | Number of "how do I..." requests during onboarding | < 2 |

Review these metrics quarterly. A decline in completion rate usually indicates a platform change broke the onboarding flow.
