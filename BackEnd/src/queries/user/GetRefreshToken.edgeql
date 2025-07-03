 select assert_single((SELECT RefreshToken {
    email,
    encrypted_password,
    expires_at,
    identity: { id }
}
FILTER .token = <str>$refresh_token AND .expires_at > datetime_current()))
