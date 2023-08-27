# This repo is built to show a Pulumi & Pulumi Kubernetes bug that occurs in connection with the ignore_changes resource option and a mutating deployment.spec property.

## Steps to repro:
1. Bring your own k8s cluster
2. Run a `pulumi up` to create the namespace and deployment
3. Using `deployment.yaml` patch file, execute `kubectl patch deployment -n nginx nginx --patch-file deployment.yaml`. This manually upates the replicas field to differ from your pulumi program.
4. At this point, the `ignore_changes` directive drives the correct behavior. That is, the spec.replicas field does not yet produce a conflict.
5. Swap the `image_tag` variable (comment/uncomment) and run a `pulumi preview`
6. A SSA conflict error should now be produced for `ignore_changes`