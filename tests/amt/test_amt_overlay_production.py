import subprocess

import pytest
import yaml


@pytest.fixture
def manifest() -> list[dict]:
    result = subprocess.run(["kubectl", "kustomize", "apps/amt/overlays/production"], capture_output=True)  # noqa: S607
    manifest = result.stdout.decode("utf-8")
    yamls = yaml.safe_load_all(manifest)
    return list(yamls)


def test_kinds(manifest):
    for m in manifest:
        assert m["kind"] in [
            "ScheduledBackup",
            "Cluster",
            "Secret",
            "ConfigMap",
            "Deployment",
            "Service",
            "Ingress",
            "PersistentVolumeClaim",
            "HorizontalPodAutoscaler",
        ]


def test_labeling(manifest):
    deployments = [m for m in manifest if m["kind"] == "Deployment"]

    assert len(deployments) == 3

    deployment = deployments[0]
    assert deployment["metadata"]["labels"]["minbzk.github.io/name"] == "amt"
    assert deployment["metadata"]["name"] == "amt-dpl"


def test_environment(manifest):
    deployments = [m for m in manifest if m["kind"] == "Deployment"]
    deployment = deployments[0]
    assert deployment["spec"]["template"]["spec"]["containers"][0]["env"][9]["name"] == "ENVIRONMENT"
    assert deployment["spec"]["template"]["spec"]["containers"][0]["env"][9]["value"] == "production"


def test_namespace(manifest):
    deployments = [m for m in manifest if m["kind"] == "Deployment"]

    assert len(deployments) == 3

    deployment = deployments[0]
    assert deployment["metadata"]["namespace"] == "tn-ai-validation-amt"


def test_port_mappings(manifest):
    deployments = [m for m in manifest if m["kind"] == "Deployment"]
    services = [m for m in manifest if m["kind"] == "Service"]
    ingresses = [m for m in manifest if m["kind"] == "Ingress"]

    assert (
        services[0]["spec"]["ports"][0]["targetPort"]
        == deployments[0]["spec"]["template"]["spec"]["containers"][0]["ports"][0]["containerPort"]
    )

    assert (
        ingresses[0]["spec"]["rules"][0]["http"]["paths"][0]["backend"]["service"]["port"]["number"]
        == services[0]["spec"]["ports"][0]["port"]
    )


def test_deployment(manifest):
    deployments = [m for m in manifest if m["kind"] == "Deployment"]

    assert len(deployments) == 3


def test_horizontal_pod_autoscaler(manifest):
    hpas = [m for m in manifest if m["kind"] == "HorizontalPodAutoscaler"]

    assert len(hpas) == 1


def test_persistant_volume_claim(manifest):
    pvcs = [m for m in manifest if m["kind"] == "PersistentVolumeClaim"]

    assert len(pvcs) == 2

    assert pvcs[0]["spec"]["accessModes"] == ["ReadWriteOnce"]


def test_ingress(manifest):
    ingresses = [m for m in manifest if m["kind"] == "Ingress"]

    assert len(ingresses) == 3
    assert ingresses[0]["spec"]["rules"][0]["host"] == "amt.prd.apps.digilab.network"
    assert ingresses[0]["spec"]["rules"][0]["http"]["paths"][0]["pathType"] == "Prefix"
    assert ingresses[1]["spec"]["rules"][0]["host"] == "pgadmin.prd.apps.digilab.network"
    assert ingresses[1]["spec"]["rules"][0]["http"]["paths"][0]["pathType"] == "Prefix"


def test_service(manifest):
    services = [m for m in manifest if m["kind"] == "Service"]

    assert len(services) == 3
    assert services[0]["spec"]["ports"][0]["port"] == 8000
