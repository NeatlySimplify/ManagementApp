with account:= <uuid>$account,
deleteAccount:= (
    delete BankAccount filter .id = account
)
update InternalUser filter .id = <uuid>$user set {
    account -= (select deleteAccount)
}
