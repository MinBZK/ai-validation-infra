import subprocess

import pytest
import yaml


@pytest.fixture
def manifest() -> list[dict]:
    result = subprocess.run(["kubectl", "kustomize", "tools/vault/overlays/production"], capture_output=True)  # noqa: S603, S607
    manifest = result.stdout.decode("utf-8")
    yamls = yaml.safe_load_all(manifest)
    return list(yamls)


def test_kinds(manifest):
    for m in manifest:
        assert m["kind"] in ["ConfigMap", "Service", "StatefulSet", "Ingress"]


def test_labeling(manifest):
    statefull_sets = [m for m in manifest if m["kind"] == "StatefulSet"]

    assert len(statefull_sets) == 1

    statefull_set = statefull_sets[0]
    assert statefull_set["metadata"]["labels"]["minbzk.github.io/name"] == "vault"
    assert statefull_set["metadata"]["name"] == "prod-vault-vault"


def test_namespace(manifest):
    statefull_sets = [m for m in manifest if m["kind"] == "StatefulSet"]

    assert len(statefull_sets) == 1

    statefull_set = statefull_sets[0]
    assert statefull_set["metadata"]["namespace"] == "tn-ai-validation-vault"


def test_port_mappings(manifest):
    statefull_sets = [m for m in manifest if m["kind"] == "StatefulSet"]
    services = [m for m in manifest if m["kind"] == "Service"]
    ingresses = [m for m in manifest if m["kind"] == "Ingress"]

    assert (
        services[0]["spec"]["ports"][0]["targetPort"]
        == statefull_sets[0]["spec"]["template"]["spec"]["containers"][0]["ports"][0]["name"]
    )

    assert (
        ingresses[0]["spec"]["rules"][0]["http"]["paths"][0]["backend"]["service"]["port"]["number"]
        == services[0]["spec"]["ports"][0]["port"]
    )


def test_ingress(manifest):
    ingresses = [m for m in manifest if m["kind"] == "Ingress"]

    assert len(ingresses) == 1
    assert ingresses[0]["spec"]["rules"][0]["host"] == "vault.apps.digilab.network"
    assert ingresses[0]["spec"]["rules"][0]["http"]["paths"][0]["pathType"] == "Prefix"


def test_service(manifest):
    services = [m for m in manifest if m["kind"] == "Service"]

    assert len(services) == 1
    assert services[0]["spec"]["ports"][0]["port"] == 8200
