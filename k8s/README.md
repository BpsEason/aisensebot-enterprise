# Kubernetes Manifests

This directory contains the basic Kubernetes manifests for deploying the aisensebot-enterprise services.

**Warning**: These are static manifests and are mainly for demonstration purposes.

For a production-grade, configurable deployment, please use the **Helm Chart** located in the `helm/` directory.

## Deploying with Helm
1. Navigate to the root of the project.
2. Ensure you have Helm installed and configured to your Kubernetes cluster.
3. Install the Helm Chart:
   ```sh
   helm install aisensebot-release ./helm
   ```
4. To customize your deployment, you can either:
   - Create a `my-values.yaml` file and override the default values:
     ```sh
     helm install aisensebot-release ./helm -f my-values.yaml
     ```
   - Override specific values directly:
     ```sh
     helm install aisensebot-release ./helm --set secrets.openAIKey="<your-key>"
     ```
5. To upgrade the deployment:
   ```sh
   helm upgrade aisensebot-release ./helm
   ```
