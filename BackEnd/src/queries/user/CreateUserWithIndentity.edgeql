WITH
    identity := <ext::auth::Identity><uuid>$identity_id,
    emailFactor := (
        SELECT ext::auth::EmailFactor FILTER .identity = identity
    )
INSERT Individual {
    email := emailFactor.email,
    name := <str>$name,
    identity := identity
};
