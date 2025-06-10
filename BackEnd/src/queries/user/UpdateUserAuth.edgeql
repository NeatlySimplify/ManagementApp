with raw_email:= <optional str>$email,
str_email:= (if exists raw_email then raw_email else <str>{}),
raw_password:= <optional str>$password,
str_password:=(if exists raw_password then raw_password else <str>{}),
update User filter .id=<uuid>$id set {
    email := str_email ?? .email,
    password := str_password ?? .password,
};
