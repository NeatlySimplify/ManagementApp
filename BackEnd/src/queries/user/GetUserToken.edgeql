with user:= assert_single((select User filter .email = <str>$email))
select (update user set {
    use_token:= true,
}){
    refresh_token,
}
