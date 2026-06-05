# Serverless

## Summary
**Serverless** is a cloud computing execution model where the cloud provider dynamically manages the allocation and provisioning of servers. Developers write and deploy code without managing infrastructure, paying only for actual usage.

## Motivation
⚠️ Reduce operational overhead for developers.
⚠️ Enable rapid scaling and cost efficiency.
⚠️ Focus on business logic, not infrastructure.

## Explanation
In serverless, code is executed in stateless compute containers triggered by events (e.g., HTTP requests, database changes). The provider handles scaling, patching, and resource management. Popular implementations include AWS Lambda, Azure Functions, and Google Cloud Functions.

## Analogy
Like ordering a taxi: you don’t own or manage the car, you just request a ride when needed and pay for the trip.

## Practical Checklist
- [x] No server management required
- [x] Event-driven execution
- [x] Automatic scaling
- [x] Pay-per-use pricing
- [ ] Have you tested cold start latency?
- [ ] Are function timeouts and resource limits configured?
- [ ] Is observability and monitoring set up?
- [ ] Have you optimized function size and dependencies?
- [ ] Is cost monitoring enabled?
- [ ] Have you tested error handling and retries?

## Watch Out For
⚠️ Cold start latency can impact performance.
⚠️ Limited execution time and resources.
⚠️ Debugging and monitoring can be challenging.



## Further Exploration

- 📖 **Best Practices** — domain-specific operating practices and decision rules
- 🎯 **Implementation Template** — sequence of implementation steps with ownership and checkpoints
- 💡 **Success Case Study** — a concrete scenario where this improved outcomes
- 💡 **Failure Case Study** — a concrete scenario where poor use caused issues
- 🔍 **Research** — key research directions and evidence to review

## Connections
- [function_as_a_service.md](function_as_a_service.md)
- [cloud_computing.md](cloud_computing.md)
- [platform_as_a_service.md](platform_as_a_service.md)

## References
- [Martin Fowler: Serverless](https://martinfowler.com/articles/serverless.html)
- [AWS Lambda Docs](https://docs.aws.amazon.com/lambda/latest/dg/welcome.html)
- [Azure Functions](https://learn.microsoft.com/en-us/azure/azure-functions/)

## Metadata
⚠️ Created: 2024-06-08
⚠️ Updated: 2024-06-08
⚠️ Author: GitHub Copilot


