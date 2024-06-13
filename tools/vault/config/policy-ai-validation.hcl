# Allow a token to manage its own cubbyhole
path "cubbyhole/*" {
    capabilities = ["create", "read", "update", "delete", "list"]
}

path "secrets/*" {
  capabilities = ["create", "read", "update", "patch", "delete", "list"]
}
