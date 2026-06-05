# Config Map

## At a Glance
| | |
|---|---|
| **Category** | Kubernetes Resource / Configuration Management |
| **Complexity** | Beginner |
| **Time to Learn** | 30-60 minutes |
| **Prerequisites** | Kubernetes basics, YAML syntax |

## One-Sentence Summary
A ConfigMap is a Kubernetes object for storing non-sensitive configuration data as key-value pairs, enabling applications to be configured independently of their container images.

## Why This Matters to You
If you deploy applications on Kubernetes, ConfigMaps let you manage environment-specific settings without rebuilding images. They make your deployments more flexible, portable, and maintainable by separating code from configuration. This approach supports best practices for twelve-factor apps and is essential for scalable, cloud-native operations in 2026.

## The Core Idea
### What It Is
A ConfigMap is a native Kubernetes resource that holds configuration data such as environment variables, command-line arguments, or config files. Pods can consume ConfigMaps as environment variables, command-line options, or mounted files. This decouples configuration from application code, allowing updates without redeploying containers.

### What It Isn't
ConfigMaps are not for sensitive data—use Kubernetes Secrets for credentials or API keys. They’re not a replacement for version control or application-level configuration management. ConfigMaps are not encrypted by default and should not be used for confidential information.

## How It Works
1. Define a ConfigMap in YAML with key-value pairs.
2. Apply it to your cluster using `kubectl apply`.
3. Reference the ConfigMap in your Pod or Deployment spec as environment variables or mounted files.

## Think of It Like This
A ConfigMap is like a settings file you can swap out for different environments—development, staging, production—without changing your application code.

## The "So What?" Factor
**If you use this:**
- You can update app settings without rebuilding images
- You keep configuration separate from code for flexibility
- You simplify environment management in Kubernetes

**If you don't:**
- You risk hardcoding settings into images
- Configuration changes require new builds and deployments
- You lose flexibility and increase operational overhead

## Practical Checklist
Before implementing, ask yourself:
- [ ] Is this configuration non-sensitive?
- [ ] Will my app need to change settings per environment?
- [ ] Do I need to update config without redeploying containers?

## Watch Out For
⚠️ Storing secrets in ConfigMaps—use Secrets for sensitive data
⚠️ Not versioning ConfigMaps—track changes for auditability

## Connections
**Builds On:** Kubernetes, YAML
**Works With:** Pods, Deployments, Secrets
**Leads To:** Dynamic configuration, environment management

## Quick Decision Guide
**Use this when you need to:** Inject non-sensitive config into Kubernetes workloads
**Skip this when:** You need to store secrets or encrypted data

## Further Exploration
- 📖 [Kubernetes ConfigMap Documentation](https://kubernetes.io/docs/concepts/configuration/configmap/)
- 🎯 [ConfigMap Usage Examples](https://kubernetes.io/docs/tasks/configure-pod-container/configure-pod-configmap/)
- 💡 [Twelve-Factor App: Config](https://12factor.net/config)

---
*Added: May 22, 2026 | Updated: May 22, 2026 | Confidence: High*
