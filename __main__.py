"""An AWS Python Pulumi program"""

import pulumi
import pulumi_kubernetes as k8s

stack_ref = pulumi.StackReference("team-ce/cluster/dev")
kubeconfig = stack_ref.require_output("kubeconfig")
provider = k8s.Provider(
    "provider",
    kubeconfig=kubeconfig
)

ns = k8s.core.v1.Namespace(
    "ts-ns",
    metadata=k8s.meta.v1.ObjectMetaArgs(
        name="nginx"
    ),
    opts=pulumi.ResourceOptions(
        provider=provider
    )
)

# NOTE: after initial pulumi up and after the replicas field has been patched, swap the below two lines to produce the conflict 
image_tag = "nginx:1.25.2"
# image_tag = "nginx:1.25"

app = { "app": "nginx" }
k8s.apps.v1.Deployment(
    "nginx",
    metadata=k8s.meta.v1.ObjectMetaArgs(
        namespace=ns.metadata.name,
        name="nginx",
    ),
    spec=k8s.apps.v1.DeploymentSpecArgs(
        selector=k8s.meta.v1.LabelSelectorArgs(
            match_labels=app,
        ),
        replicas=2,
        template=k8s.core.v1.PodTemplateSpecArgs(
            metadata=k8s.meta.v1.ObjectMetaArgs(
                labels=app,
            ),
            spec=k8s.core.v1.PodSpecArgs(
                containers=[k8s.core.v1.ContainerArgs(
                    name="nginx",
                    image=image_tag,
                    ports=[k8s.core.v1.ContainerPortArgs(
                        container_port=80
                    )],
                )]
            )
        )
    ),
    opts=pulumi.ResourceOptions(
        provider=provider,
        ignore_changes=["spec.replicas"]
    )
)

pulumi.export("kubeconfig", kubeconfig)
