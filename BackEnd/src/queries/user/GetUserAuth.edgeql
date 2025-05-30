select User {
    id,
    password,
    refresh_token,
    use_token,
} filter .email = <str>$email limit 1;
