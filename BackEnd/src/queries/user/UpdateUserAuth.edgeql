update User filter .id=<uuid>$id set {
    email := <optional str>$email ?? .email,
    password := <optional str>$password ?? .password,
};
