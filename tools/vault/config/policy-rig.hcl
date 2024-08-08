# Allow a token to manage its own cubbyhole
path "cubbyhole/*" {
    capabilities = ["create", "read", "update", "delete", "list"]
}

path "rig/*" {
  capabilities = ["create", "read", "update", "patch", "delete", "list"]
}
