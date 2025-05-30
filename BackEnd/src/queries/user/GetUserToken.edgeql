select (update InternalUser filter .email = <str>$email set {
    use_token:= true,
}){
    refresh_token,
}
