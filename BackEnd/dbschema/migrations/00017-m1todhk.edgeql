CREATE MIGRATION m1todhkafke6rx6osihnuafp6tyybygyhcekbi37dpghuj34ftojrq
    ONTO m1nwvtfvss47qugy7vonfs5ow4xzzdyonsxfwfw2v5vnoye77tq6aa
{
  DROP FUNCTION default::MovementNum(user_id: std::uuid);
  ALTER TYPE default::Payment {
      CREATE REQUIRED SINGLE LINK account: default::BankAccount {
          SET REQUIRED USING (<default::BankAccount>{});
      };
      ALTER TRIGGER create_event USING (WITH
          data := 
              (INSERT
                  default::Scheduler
                  {
                      user := __new__.user,
                      name := __new__.name,
                      type := __new__.type,
                      status := __new__.status,
                      date := __new__.is_due,
                      origin := <default::Record_OR_Payment>__new__.id
                  })
      UPDATE
          default::Payment
      FILTER
          (.id = __new__.id)
      SET {
          event := data
      });
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
                  }) IF (net_change != 0) ELSE {})
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
      ALTER TRIGGER update_balance_on_delete USING (UPDATE
          default::BankAccount
      FILTER
          (.id = __old__.account.id)
      SET {
          balance := (.balance - __old__.value)
      });
      ALTER TRIGGER update_balance_on_insert USING (UPDATE
          default::BankAccount
      FILTER
          (.id = __new__.account.id)
      SET {
          balance := (.balance + __new__.value)
      });
      ALTER TRIGGER update_event USING (WITH
          new_status := 
              __new__.status
          ,
          old_status := 
              __old__.status
          ,
          new_isDue := 
              __new__.is_due
          ,
          payment_date := 
              __new__.payment_date
          ,
          new_date := 
              (SELECT
                  (payment_date IF (new_status AND (new_status != old_status)) ELSE new_isDue)
              )
      UPDATE
          __old__.event
      SET {
          name := __new__.name,
          status := __new__.status,
          date := new_date
      });
  };
  ALTER TYPE default::Movement {
      DROP LINK account;
      DROP PROPERTY category;
      DROP PROPERTY cycle;
      DROP PROPERTY details;
      DROP PROPERTY effective;
      ALTER PROPERTY installment {
          USING (std::count(__source__.payment));
      };
      DROP PROPERTY interest;
      DROP PROPERTY name;
      DROP PROPERTY penalty;
      DROP PROPERTY subcategory;
      ALTER PROPERTY value {
          USING (std::sum(__source__.payment.value));
      };
  };
  ALTER TYPE default::Payment {
      CREATE PROPERTY category: std::str;
  };
  ALTER TYPE default::Payment {
      CREATE PROPERTY interest: std::float64 {
          SET default := 0;
      };
  };
  ALTER TYPE default::Payment {
      DROP PROPERTY part;
  };
  ALTER TYPE default::Payment {
      CREATE PROPERTY penalty: std::decimal {
          SET default := 0;
      };
  };
  ALTER TYPE default::Payment {
      CREATE PROPERTY subcategory: std::str;
  };
};
