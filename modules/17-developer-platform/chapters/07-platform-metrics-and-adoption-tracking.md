# Chapter 07 - Platform Metrics and Adoption Tracking

## Why Platform Metrics Matter

A platform team that cannot measure adoption cannot tell whether the platform is succeeding. Investment in new features is wasted if existing features are not being used. Problems in the onboarding flow are invisible without instrumentation.

Platform metrics answer three questions:
1. Are teams adopting the platform?
2. Are they succeeding when they try?
3. Is the platform getting better or worse over time?

## Adoption Metrics

Adoption metrics measure how many teams and developers are using the platform and at what depth:

| Metric | Definition | Interpretation |
|---|---|---|
| Active tenants | Teams with at least one successful API call this week | Breadth of adoption |
| Active applications | Applications making platform calls this week | Depth of adoption |
| New tenants per month | Teams onboarded in the last 30 days | Growth rate |
| Feature adoption depth | % of tenants using each platform capability | Which features drive value |
| Template usage | # of applications created from each golden path | Effectiveness of templates |

## Quality Metrics

Quality metrics measure whether platform users succeed:

| Metric | Target | Signal When Degrading |
|---|---|---|
| Onboarding completion rate | > 80% | Onboarding flow is broken |
| Support requests per team per month | < 2 | Platform is confusing or unreliable |
| Developer-reported friction score | < 3/5 | Specific friction points need investigation |
| Mean time to onboarding complete | < 2 hours | Onboarding is too complex |

## DORA Metrics For Platform Teams

DORA (DevOps Research and Assessment) metrics apply to platform teams as well as product teams:

| Metric | Platform Context | Good Performance |
|---|---|---|
| Deployment frequency | How often does the platform release updates? | Weekly or more |
| Lead time for changes | Time from commit to production | < 1 week |
| Change failure rate | % of platform releases that cause incidents | < 15% |
| Mean time to recovery | Time to restore platform after an incident | < 1 hour |

Platform teams that track DORA metrics can demonstrate operational maturity to stakeholders and identify systemic improvement opportunities.

## Platform NPS

Net Promoter Score for the platform: "On a scale of 0–10, how likely are you to recommend the AI platform to a colleague?"

Collect quarterly from all active tenants. Segment results by:
- experience level (new vs veteran platform users)
- team size
- which platform features they primarily use

NPS detractors (0–6) are the most valuable feedback signal — they represent developers who are frustrated enough to be at risk of abandoning the platform or building their own alternatives.

## The Adoption Funnel

Track where developers drop off in the adoption journey:

```
100% → discovered the platform (visited the portal)
 75% → started onboarding (created an account or tenant)
 60% → completed onboarding (first successful API call)
 45% → built first application (used a golden path template)
 35% → active regular use (multiple calls per week)
 25% → platform advocate (recommends to colleagues)
```

The drop from each stage to the next reveals specific problems. A large drop from "completed onboarding" to "built first application" suggests the golden paths are not discoverable or easy enough. A large drop from "active regular use" to "platform advocate" suggests the platform is useful but not delightful.

## Making Metrics Visible

Publish platform metrics to the organization:

- Monthly platform health report distributed to engineering leads
- Dashboard visible to any developer in the portal
- Quarterly platform retrospective with development teams as participants

Transparency about platform metrics creates accountability and invites developers to contribute to improvement rather than just complain.
