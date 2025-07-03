INSERT RefreshToken {
    token := <str>$token,
    email := <str>$email,
    encrypted_password := <str>$enc_pw,
    identity := <ext::auth::Identity><uuid>$identity_id,
    expires_at := datetime_current() + <duration><str>$duration
}
