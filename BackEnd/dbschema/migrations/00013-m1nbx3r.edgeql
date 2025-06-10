CREATE MIGRATION m1nbx3rckbcjulg2xv6mtx6lsxhm6dzysfphumxcvkvge57vnx7aoq
    ONTO m1k4n2cnyu5q2m2ub4hcncg7zzj7rjcncbifrypjnscc44kvrk2gfq
{
  ALTER TYPE default::Payment {
      DROP TRIGGER update_any;
  };
  ALTER TYPE default::Payment {
      CREATE TRIGGER update_balance_on_account_change
          AFTER UPDATE 
          FOR EACH 
              WHEN ((__old__.account.id != __new__.account.id))
          DO (WITH
              old_value := 
                  __old__.value
              ,
              new_value := 
                  __new__.value
              ,
              old_payment_status := 
                  __old__.status
              ,
              new_payment_status := 
                  __new__.status
              ,
              old_ignore := 
                  __old__.ignore_in_totals
              ,
              new_ignore := 
                  __new__.ignore_in_totals
              ,
              new_type := 
                  __new__.type
              ,
              old_account_id := 
                  __old__.account.id
              ,
              new_account_id := 
                  __new__.account.id
              ,
              old_payment_original_impact := 
                  (old_value * (IF (new_type = 'income') THEN 1 ELSE -1))
              ,
              update_old_account := 
                  ((UPDATE
                      default::BankAccount
                  FILTER
                      (.id = old_account_id)
                  SET {
                      balance := (.balance - old_payment_original_impact)
                  }) IF (old_payment_status AND NOT (old_ignore)) ELSE <default::BankAccount>{})
              ,
              new_payment_current_impact := 
                  (new_value * (IF (new_type = 'income') THEN 1 ELSE -1))
              ,
              update_new_account := 
                  ((UPDATE
                      default::BankAccount
                  FILTER
                      (.id = new_account_id)
                  SET {
                      balance := (.balance + new_payment_current_impact)
                  }) IF (new_payment_status AND NOT (new_ignore)) ELSE <default::BankAccount>{})
          SELECT
              (update_old_account, update_new_account)
          );
  };
  ALTER TYPE default::Payment {
      CREATE TRIGGER update_balance_on_same_account_changes
          AFTER UPDATE 
          FOR EACH 
              WHEN (((__old__.account.id = __new__.account.id) AND (((__old__.value != __new__.value) OR (__old__.status != __new__.status)) OR (__old__.ignore_in_totals != __new__.ignore_in_totals))))
          DO (WITH
              old_value := 
                  __old__.value
              ,
              new_value := 
                  __new__.value
              ,
              old_payment_status := 
                  __old__.status
              ,
              new_payment_status := 
                  __new__.status
              ,
              old_ignore := 
                  __old__.ignore_in_totals
              ,
              new_ignore := 
                  __new__.ignore_in_totals
              ,
              payment_type := 
                  __new__.type
              ,
              net_impact := 
                  (((new_value IF (new_payment_status AND NOT (new_ignore)) ELSE 0) - (old_value IF (old_payment_status AND NOT (old_ignore)) ELSE 0)) * (IF (payment_type = 'income') THEN 1 ELSE -1))
          SELECT
              ((UPDATE
                  default::BankAccount
              FILTER
                  (.id = __new__.account.id)
              SET {
                  balance := (.balance + net_impact)
              }) IF (net_impact != 0) ELSE <default::BankAccount>{})
          );
  };
};
