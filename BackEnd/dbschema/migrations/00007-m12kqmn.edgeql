CREATE MIGRATION m12kqmntmjiyewnhdwfpnpyt5ug42xbpalp5c2ls4beyoiopu5atxq
    ONTO m1youznodei6mzliuba5wmlq3v5yrtgdvf4dhtxjiprqvwwkinmdoq
{
  ALTER TYPE default::Payment {
      ALTER TRIGGER update_any USING (WITH
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
              __old__.account.id
          ,
          new_ignore := 
              __new__.ignore_in_totals
          ,
          old_ignore := 
              __old__.ignore_in_totals
          ,
          new_account_id := 
              __new__.account.id
          ,
          same_account_block_result := 
              ((WITH
                  net_change := 
                      ((new_value IF (new_payment_status AND NOT (new_ignore)) ELSE 0) - (old_value IF (old_payment_status AND NOT (old_ignore)) ELSE 0))
              SELECT
                  ((UPDATE
                      default::BankAccount
                  FILTER
                      (.id = old_account_id)
                  SET {
                      balance := (.balance + net_change)
                  }) IF (net_change != 0) ELSE <default::BankAccount>{})
              ) IF (old_account_id ?= new_account_id) ELSE <default::BankAccount>{})
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
                      }) IF (old_payment_status AND NOT (old_ignore)) ELSE <default::BankAccount>{})
                  ,
                  new_account_addition := 
                      ((UPDATE
                          default::BankAccount
                      FILTER
                          (.id = new_account_id)
                      SET {
                          balance := (.balance + new_value)
                      }) IF (new_payment_status AND NOT (new_ignore)) ELSE <default::BankAccount>{})
              SELECT
                  (old_account_deduction UNION new_account_addition)
              ) IF (old_account_id ?!= new_account_id) ELSE <default::BankAccount>{})
      SELECT
          (same_account_block_result UNION different_accounts_block_result)
      );
  };
};
