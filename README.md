# AI Validation Infra

This is the infra repository deploying to a kubernetes cluster.

Note: Changes to this repo's MAIN branch are deployed to kubernetes.

## How to contribute

See [contributing docs](CONTRIBUTING.md)

## Secrets management

Secrets are managed with [SOPS](https://www.cncf.io/projects/sops/). Sops allows encryption of yaml (and other) files with a public key.
A private key that is set in the CI/CD can decrypt the secrets.

```shell
sops --encrypt -i apps/tad/overlays/production/secret-postgres.yaml
sops --decrypt -i apps/tad/overlays/production/secret-postgres.yaml
```

By default sops looks in the .sops.yaml to get the public key to encrypt the files.

## Deployment

The `main` branch is deployed to kubernetes with [Flux](https://www.cncf.io/projects/flux/)

## Labels

When you have a lot of resources it is important to label all your kubernetes resources because else the resources becomes un-managable. We use the [kubernetes best practices](https://kubernetes.io/docs/concepts/overview/working-with-objects/common-labels/) for labbeling.

## Kubernetes (digilab)

Every kubernetes has a slightly different setup and services available. We are currenlty working on the digilab cloud. They have the following capabilities added:

* cert-manager for tls certificate management
* flux for gitops deployment
* grafana for a metrics dashboard
* loki for logging collecter
* pinniped for authentication to kubernetes
* treafik as ingress controller
* cloudnativePG for postgres databases
* sops for secret encryption
* prometheus operator (PodMonitor & Alertmanager)

### Access

To get access you need a [pleio](https://account.pleio.nl/) account with the correct permissions and pinniped installed.

to install pinniped follow [pinniped install]( https://get.pinniped.dev) tutorial. To get correct access from your pleio account ask a collegue.

### namespaces

The AI Validation team has access to the following namespaces:

* tn-ai-validation-infra. Purpose: general infra needed for ai validation team like secrets management and identity management.
* tn-ai-validation-llm-benchmarks. Purpose:  Running LLM benchmark software
* tn-ai-validation-playground. Purpose: random stuff for fun. can be removed at any moment
* tn-ai-validation-tad. Purpose: running TAD main branch
* tn-ai-validation-tad-staging. Purpose: Running tad PRs branches

### storage classes
The following storage classes are available for persistent storage

```bash
NAME                       PROVISIONER          RECLAIMPOLICY   VOLUMEBINDINGMODE      ALLOWVOLUMEEXPANSION   AGE
azurefile                  file.csi.azure.com   Delete          Immediate              true                   364d
azurefile-csi              file.csi.azure.com   Delete          Immediate              true                   364d
azurefile-csi-nfs          file.csi.azure.com   Delete          Immediate              true                   364d
azurefile-csi-nfs-retain   file.csi.azure.com   Retain          Immediate              true                   350d
azurefile-csi-premium      file.csi.azure.com   Delete          Immediate              true                   364d
azurefile-premium          file.csi.azure.com   Delete          Immediate              true                   364d
default (default)          disk.csi.azure.com   Delete          WaitForFirstConsumer   true                   364d
managed                    disk.csi.azure.com   Delete          WaitForFirstConsumer   true                   364d
managed-csi                disk.csi.azure.com   Delete          WaitForFirstConsumer   true                   364d
managed-csi-premium        disk.csi.azure.com   Delete          WaitForFirstConsumer   true                   364d
managed-premium            disk.csi.azure.com   Delete          WaitForFirstConsumer   true                   364d
```
