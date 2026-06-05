# Reserved Instance

## At a Glance
| | |
|---|---|
| **Category** | Concept / Cloud Cost Management |
| **Complexity** | Beginner to Intermediate |
| **Time to Learn** | 1-2 hours |
| **Prerequisites** | Cloud computing basics, capacity planning concepts |

## One-Sentence Summary
A reserved instance is a cloud pricing commitment where you agree to use a specific amount of compute capacity for a defined period (typically 1-3 years) in exchange for a significant discount—typically 30-60%—over on-demand pricing.

## Why This Matters to You
AI infrastructure has two types of compute: the baseline that runs 24/7 (always-on inference APIs, model servers, core platform services) and the elastic capacity that varies with demand. Paying on-demand rates for the baseline is one of the most common and costly mistakes in AI platform budgeting. Reserved instances convert that always-running compute from full price to half price or less. At meaningful scale, this is typically the single largest cost optimization lever available.

## The Core Idea
### What It Is
Cloud providers—AWS, Azure, Google Cloud—offer reserved pricing contracts where you commit to using a specified amount of compute capacity over a fixed term:

- **1-year term:** Typically 30-40% discount over on-demand
- **3-year term:** Typically 50-60% discount over on-demand, with larger upfront payment options

The commitment can be structured as:
- **All upfront:** Pay the full reserved amount at contract start. Maximum discount.
- **Partial upfront:** Pay a portion upfront, the rest monthly. Moderate discount.
- **No upfront:** Pay monthly at a discounted rate. Smallest discount but no capital commitment.

**Provider-specific names:**
- AWS: Reserved Instances (EC2), Savings Plans (more flexible, covers Lambda and Fargate)
- Azure: Reserved VM Instances, Azure Savings Plan
- Google Cloud: Committed Use Discounts (CUDs)

Modern "savings plan" variants are more flexible than traditional reserved instances—they apply discounts to compute spend across instance types and sizes, not a specific instance configuration, making them easier to use with evolving infrastructure.

### What It Isn't
Reserved instances are not reserved capacity in the physical sense—they're a pricing commitment, not a guarantee that specific hardware will always be available (though capacity reservations can be added for an additional fee). They're also not appropriate for workloads that are inherently unpredictable or might be terminated—that's what spot/preemptible instances are for.

## How It Works
1. **Analyze baseline utilization:** Review the past 30-90 days of compute usage. Identify the minimum consistent utilization floor—compute that runs 24/7 regardless of traffic fluctuations.
2. **Choose the commitment level:** Reserve for the baseline floor, not the peak. Let auto scaling handle peak demand on on-demand pricing.
3. **Select term and payment option:** Balance upfront capital cost against total cost savings. 3-year terms maximize savings but reduce flexibility.
4. **Purchase and activate:** Reservations apply automatically to matching running instances—no configuration changes needed to existing workloads.
5. **Monitor utilization:** Reserved instances cost money whether used or not. Track utilization to ensure the reserved capacity is actually being consumed.
6. **Review periodically:** As workloads evolve, reservations may need to be modified, sold on the marketplace (AWS), or allowed to expire.

## Think of It Like This
An airline that buys a block of 50 seats between two cities every Monday gets a deep discount because the airline can plan around that guaranteed revenue. You, as the buyer, get cheap seats for your regular route. If you don't show up, you've still paid for the seat. Reserved instances work the same way: the cloud provider gives you a discount because your commitment lets them plan capacity more efficiently, and you benefit as long as you actually use the compute you committed to.

## The "So What?" Factor
**If you use this:**
- Baseline infrastructure costs are 30-60% lower immediately upon commitment
- Infrastructure budgets become more predictable (lower variable component)
- Engineering teams can justify keeping important services always-on without budget pressure

**If you don't:**
- Consistently running workloads pay full on-demand rates—the most expensive cloud pricing option
- Cloud bills are unnecessarily large for stable, predictable baseline compute
- Budget pressure forces over-aggressive cost-cutting in the wrong places (capability vs. pricing)

## Practical Checklist
Before purchasing reserved instances, ask yourself:
- [ ] Have I identified the stable baseline compute that runs 24/7?
- [ ] Is this workload expected to continue for the commitment term? (1 or 3 years)
- [ ] Have I selected Savings Plans over traditional reserved instances where possible for flexibility?
- [ ] Am I committing to the floor, not the peak? (Let auto scaling handle peaks on-demand)
- [ ] Do I have budget authority or approval for the upfront payment?
- [ ] Is there a process to review and right-size reservations quarterly?

## Watch Out For
⚠️ **Over-committing:** Purchasing more reserved capacity than you actually use means paying for idle reservations—negative ROI on the investment.
⚠️ **Committing before workloads are stable:** Early-stage systems change rapidly. Reserve after the architecture and scale are stable, not before.
⚠️ **Forgetting to right-size before reserving:** Reserving oversized instances locks in waste at a discount. Right-size first, then reserve.
⚠️ **Ignoring savings plan flexibility:** Traditional reserved instances tied to specific instance types are less flexible than savings plans, which apply across compatible compute. Prefer savings plans where available.

## Connections
**Builds On:** [Cloud Computing](../Cloud_and_Distributed/cloud_computing.md), [Capacity Planning](capacity_planning.md)
**Works With:** [Cost Optimization](cost_optimization.md), [Right Sizing](right_sizing.md), [Spot Instance](spot_instance.md), [Auto Scaling](auto_scaling.md), [Resource Tagging](resource_tagging.md)
**Leads To:** [Cost Optimization](cost_optimization.md)

## Quick Decision Guide
**Use this when you need to:** Reduce costs on stable, predictable baseline compute that runs continuously.
**Skip this when:** The workload is unpredictable, the architecture is still changing, or the commitment term exceeds reasonable project longevity.

## Further Exploration
- 📖 [AWS Savings Plans vs. Reserved Instances comparison](https://aws.amazon.com/savingsplans/faq/)
- 🎯 [Azure Reservations cost analysis and recommendations](https://learn.microsoft.com/en-us/azure/cost-management-billing/reservations/reservation-recommendations)
- 💡 [Google Cloud Committed Use Discounts guide](https://cloud.google.com/compute/docs/instances/signing-up-committed-use-discounts)

---
*Added: May 26, 2026 | Updated: May 26, 2026 | Confidence: High*
