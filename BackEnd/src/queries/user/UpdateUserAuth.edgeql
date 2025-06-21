with user := (select global current_user_obj)
update user set {
    email := <optional str>$email ?? .email,
    password := <optional str>$password ?? .password,
};
