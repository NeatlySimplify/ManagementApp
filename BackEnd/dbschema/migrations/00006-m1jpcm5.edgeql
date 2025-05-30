CREATE MIGRATION m1jpcm52ew3gkdavsw7otzamovy5x7w7nzjwxdilca3bynxlhgjtwa
    ONTO m1vnjhxeat7lryf5mfzo24pskb22y6j2clqf3adxmfpoaaiejpsgha
{
  ALTER TYPE default::BankAccount {
      ALTER PROPERTY accountName {
          RENAME TO account_name;
      };
  };
  ALTER TYPE default::BankAccount {
      ALTER PROPERTY bankName {
          RENAME TO bank_name;
      };
  };
  ALTER TYPE default::InternalUser {
      ALTER PROPERTY isActive {
          RENAME TO is_active;
      };
  };
  ALTER TYPE default::InternalUser {
      ALTER PROPERTY lastActiveDate {
          RENAME TO last_active_date;
      };
  };
  ALTER TYPE default::Payment {
      ALTER PROPERTY isDue {
          RENAME TO is_due;
      };
      ALTER TRIGGER create_event USING (WITH
          data := 
              (INSERT
                  default::Scheduler
                  {
                      user := __new__.user,
                      name := __new__.movement.name,
                      tag_type := __new__.payment_type,
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
  };
  ALTER TYPE default::Payment {
      ALTER PROPERTY paymentDate {
          RENAME TO payment_date;
      };
      ALTER TRIGGER update_event {
          WHEN (((__new__.status = true) OR (__old__.is_due != __new__.is_due)));
          USING (WITH
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
              name := __new__.movement.name,
              status := __new__.status,
              date := new_date
          });
      };
  };
  ALTER TYPE default::Record {
      ALTER PROPERTY id_Service {
          RENAME TO id_service;
      };
  };
  ALTER TYPE default::Scheduler {
      DROP PROPERTY date_month;
      DROP PROPERTY date_year;
  };
  ALTER TYPE default::UserSettings {
      ALTER LINK default_BankAccount {
          RENAME TO default_bank_account;
      };
  };
};
