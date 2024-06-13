#!/usr/bin/env bash

export VAULT_ADDR='https://vault.apps.digilab.network'

# Initialize Vault and capture the output
INIT_OUTPUT=$(vault operator init -key-shares=8 -key-threshold=2)

# Extract the unseal keys and root token from the output
UNSEAL_KEYS=$(echo "$INIT_OUTPUT" | grep 'Unseal Key' | awk '{print $NF}')
ROOT_TOKEN=$(echo "$INIT_OUTPUT" | grep 'Initial Root Token' | awk '{print $NF}')

echo "Root token: $ROOT_TOKEN"

echo "Unseal keys: $UNSEAL_KEYS"

# # Copy the unseal keys and root token to a save environment
echo "$UNSEAL_KEYS" | head -n 1 | xargs vault operator unseal
