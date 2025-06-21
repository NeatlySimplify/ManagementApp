with query_todo:= (
insert Account {
    name := <str>$name,
    email:= <str>$email,
    password:= <str>$password,
    refresh_token:= <uuid>$refreshe_token
}
) if <str>$type_insert = "organization" else (
insert Individual {
    name := <str>$name,
    email:= <str>$email,
    password:= <str>$password,
    refresh_token:= <uuid>$refreshe_token
}
)
select query_todo
