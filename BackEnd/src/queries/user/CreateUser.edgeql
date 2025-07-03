with identity := <ext::auth::Identity><uuid>$identity_id,
emailFactor := (
    SELECT ext::auth::EmailFactor FILTER .identity = identity
),
query_todo:= (
insert Account {
    name := <str>$name,
    email:= emailFactor.email,
    refresh_token:= <uuid>$refreshe_token,
    identity := identity
}
) if <str>$type_insert = "organization" else (
insert Individual {
    name := <str>$name,
    email:= emailFactor.email,
    refresh_token:= <uuid>$refreshe_token,
    identity := identity
}
)
select query_todo
