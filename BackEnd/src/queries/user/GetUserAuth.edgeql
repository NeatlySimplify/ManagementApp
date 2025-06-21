select User {
    id,
    tag_type,
    password,
    refresh_token,
    use_token,
    first_access,
} filter .email = <str>$email limit 1;
