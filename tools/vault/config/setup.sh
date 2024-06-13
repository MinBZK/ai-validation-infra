#!/usr/bin/env bash

export VAULT_ADDR='https://vault.apps.digilab.network'

if [ -z "$VAULT_TOKEN" ]; then
  echo "VAULT_TOKEN is not set"
  exit 1
fi

# enable auditing (we could use filebeat to stream it somewhere)
vault audit enable file file_path=/vault/data/vault_audit.log

# enable github auth
vault auth enable github
vault write auth/github/config organization=MinBZK organization_id=33843588 max_ttl=22h ttl=10h
vault write sys/auth/github/tune listing_visibility="unauth"

# create policies for github auth
vault policy write default policy-default.hcl
vault policy write ai-validation-team policy-ai-validation.hcl
vault policy write admin-team policy-admin.hcl


# setup team and user permissions
vault write auth/github/map/teams/ai-validation-team value=default,ai-validation-team
vault write auth/github/map/users/berrydenhartog value=admin-team
vault write auth/github/map/users/anneschuth value=admin-team

# enable kv store
vault secrets enable -path=secrets -version=2 kv


# vault login -method=github token=<key>
