CREATE MIGRATION m1ei2o4dtlo7czklp6bfepo6fdovppqx2r7ecypoa3o2suqnotzdvq
    ONTO m1ry6ic46lmrchc2ann7fnnm2ghqkoay6emzwmg4iskfgii7cahj5a
{
  ALTER TYPE default::Payment {
      CREATE TRIGGER update_any
          AFTER UPDATE 
          FOR EACH DO (WITH
              old_payment_status := 
                  __old__.status
              ,
              new_payment_status := 
                  __new__.status
              ,
              old_value := 
                  __old__.value
              ,
              new_value := 
                  __new__.value
              ,
              old_account_id := 
                  __old__.movement.account.id
              ,
              new_ignore := 
                  __new__.ignore_in_totals
              ,
              old_ignore := 
                  __old__.ignore_in_totals
              ,
              new_account_id := 
                  __new__.movement.account.id
              ,
              same_account_block_result := 
                  ((WITH
                      net_change := 
                          ((new_value IF (new_payment_status AND NOT (new_ignore)) ELSE 0.0) - (old_value IF (old_payment_status AND NOT (old_ignore)) ELSE 0.0))
                  SELECT
                      ((UPDATE
                          default::BankAccount
                      FILTER
                          (.id = old_account_id)
                      SET {
                          balance := (.balance + net_change)
                      }) IF (net_change != 0.0) ELSE {})
                  ) IF (old_account_id ?= new_account_id) ELSE {})
              ,
              different_accounts_block_result := 
                  ((WITH
                      old_account_deduction := 
                          ((UPDATE
                              default::BankAccount
                          FILTER
                              (.id = old_account_id)
                          SET {
                              balance := (.balance - old_value)
                          }) IF (old_payment_status AND NOT (old_ignore)) ELSE {})
                      ,
                      new_account_addition := 
                          ((UPDATE
                              default::BankAccount
                          FILTER
                              (.id = new_account_id)
                          SET {
                              balance := (.balance + new_value)
                          }) IF (new_payment_status AND NOT (new_ignore)) ELSE {})
                  SELECT
                      (old_account_deduction UNION new_account_addition)
                  ) IF (old_account_id ?!= new_account_id) ELSE {})
          SELECT
              (same_account_block_result UNION different_accounts_block_result)
          );
      CREATE TRIGGER update_balance_on_delete
          AFTER DELETE 
          FOR EACH 
              WHEN (((__old__.status = true) AND (__old__.ignore_in_totals = false)))
          DO (UPDATE
              default::BankAccount
          FILTER
              (.id = __old__.movement.account.id)
          SET {
              balance := (.balance - __old__.value)
          });
      CREATE TRIGGER update_balance_on_insert
          AFTER INSERT 
          FOR EACH 
              WHEN (((__new__.status = true) AND (__new__.ignore_in_totals = false)))
          DO (UPDATE
              default::BankAccount
          FILTER
              (.id = __new__.movement.account.id)
          SET {
              balance := (.balance + __new__.value)
          });
  };
};
