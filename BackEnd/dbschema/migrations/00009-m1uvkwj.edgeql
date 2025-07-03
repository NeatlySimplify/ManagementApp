CREATE MIGRATION m1uvkwjlvo3jdrorxzks4utftrvhnluqvlz3wa6eor7rx4upo3moaa
    ONTO m14gidynwnvadymer4rjcjoyyec2vncqp4y7at67ovws6ttyd2hubq
{
  CREATE TYPE default::BankAccount EXTENDING default::Derived {
      CREATE PROPERTY balance: std::decimal {
          SET default := 0;
          CREATE CONSTRAINT std::min_value(0);
      };
      CREATE REQUIRED PROPERTY account_name: std::str;
      CREATE REQUIRED PROPERTY bank_name: std::str;
      CREATE PROPERTY category_tag: std::str;
      CREATE PROPERTY ignore_on_totals: std::bool {
          SET default := (<std::bool>false);
      };
      CREATE PROPERTY notes: std::json;
  };
  CREATE TYPE default::Address {
      CREATE PROPERTY city: std::str;
      CREATE PROPERTY complement: std::str;
      CREATE PROPERTY district: std::str;
      CREATE PROPERTY number: std::int64;
      CREATE PROPERTY postal: std::str;
      CREATE PROPERTY state: std::str;
      CREATE PROPERTY street: std::str;
  };
  CREATE TYPE default::Contact {
      CREATE PROPERTY complement: std::str;
      CREATE PROPERTY number: std::str;
      CREATE PROPERTY type_tag: std::str;
  };
  CREATE TYPE default::Entity EXTENDING default::Derived {
      CREATE MULTI LINK address: default::Address {
          ON SOURCE DELETE DELETE TARGET;
          ON TARGET DELETE ALLOW;
      };
      CREATE MULTI LINK phone: default::Contact {
          ON SOURCE DELETE DELETE TARGET;
          ON TARGET DELETE ALLOW;
      };
      CREATE PROPERTY birth: std::cal::local_date;
      CREATE PROPERTY document: std::str;
      CREATE PROPERTY document_type: std::str;
      CREATE REQUIRED PROPERTY email: std::str {
          CREATE CONSTRAINT std::exclusive;
      };
      CREATE PROPERTY name: std::str;
      CREATE PROPERTY notes: std::json;
      CREATE PROPERTY relationship_status: std::str;
      CREATE PROPERTY sex: std::str;
      CREATE PROPERTY status: std::bool {
          SET default := true;
      };
  };
  CREATE TYPE default::Scheduler EXTENDING default::Derived {
      CREATE PROPERTY date: std::cal::local_date;
      CREATE PROPERTY name: std::str;
      CREATE PROPERTY status: std::bool {
          SET default := false;
      };
      CREATE PROPERTY beginning_time: std::cal::local_time;
      CREATE OPTIONAL PROPERTY ending_time: std::cal::local_time;
      CREATE PROPERTY notes: std::json;
  };
  ALTER TYPE default::User {
      CREATE MULTI LINK account := (SELECT
          DETACHED default::BankAccount
      FILTER
          (.owner = __source__)
      );
      CREATE MULTI LINK entity := (.<owner[IS default::Entity]);
      CREATE MULTI LINK event := (SELECT
          DETACHED default::Scheduler
      FILTER
          (.owner = __source__)
      );
      CREATE ACCESS POLICY allow_insert
          ALLOW INSERT USING (true);
      CREATE ACCESS POLICY allow_user
          ALLOW SELECT, UPDATE, DELETE USING ((GLOBAL default::current_user ?= __subject__));
  };
  CREATE TYPE default::Account EXTENDING default::User {
      CREATE ACCESS POLICY allow_admin
          ALLOW SELECT, UPDATE, DELETE USING (((GLOBAL default::current_user).is_admin ?? false));
      ALTER PROPERTY tag_type {
          SET default := 'is_account';
          SET OWNED;
          SET TYPE std::str;
      };
  };
  CREATE TYPE default::Administator EXTENDING default::User {
      ALTER PROPERTY is_admin {
          SET default := (<std::bool>true);
          SET OWNED;
          SET TYPE std::bool;
      };
      ALTER PROPERTY tag_type {
          SET default := 'is_admin';
          SET OWNED;
          SET TYPE std::str;
      };
  };
  CREATE TYPE default::Individual EXTENDING default::User {
      CREATE ACCESS POLICY allow_admin
          ALLOW SELECT, UPDATE, DELETE USING (((GLOBAL default::current_user).is_admin ?? false));
      ALTER PROPERTY tag_type {
          SET default := 'is_individual';
          SET OWNED;
          SET TYPE std::str;
      };
  };
  CREATE TYPE default::Record EXTENDING default::Derived {
      CREATE MULTI LINK entity: default::Entity {
          ON TARGET DELETE ALLOW;
      };
      CREATE MULTI LINK event: default::Scheduler;
      CREATE PROPERTY name: std::str;
      CREATE PROPERTY notes: std::json;
      CREATE PROPERTY optional_status: std::str;
      CREATE PROPERTY service_id: std::str;
      CREATE PROPERTY status: std::bool;
      CREATE PROPERTY value: std::decimal;
  };
  ALTER TYPE default::User {
      CREATE MULTI LINK record := (SELECT
          DETACHED default::Record
      FILTER
          (.owner = __source__)
      );
  };
  ALTER TYPE default::Account {
      CREATE MULTI LINK collaborator_pool: default::Individual;
  };
  CREATE TYPE default::Project EXTENDING default::Derived {
      CREATE MULTI LINK entity: default::Entity {
          ON SOURCE DELETE ALLOW;
      };
      CREATE MULTI LINK people: default::Individual {
          CREATE PROPERTY role: std::str;
      };
      CREATE MULTI LINK schedule: default::Scheduler {
          ON SOURCE DELETE DELETE TARGET;
          ON TARGET DELETE ALLOW;
      };
      CREATE SINGLE LINK record: default::Record {
          ON SOURCE DELETE DELETE TARGET;
          ON TARGET DELETE ALLOW;
      };
      CREATE PROPERTY name: std::str;
      CREATE PROPERTY notes: std::json;
  };
  ALTER TYPE default::Account {
      CREATE MULTI LINK grouping := (.<owner[IS default::Project]);
  };
  CREATE TYPE default::Movement EXTENDING default::Derived {
      CREATE LINK record: default::Record;
      CREATE PROPERTY notes: std::json;
  };
  ALTER TYPE default::User {
      CREATE MULTI LINK movement := (.<owner[IS default::Movement]);
  };
  CREATE TYPE default::Payment EXTENDING default::Derived {
      CREATE REQUIRED LINK movement: default::Movement {
          ON TARGET DELETE DELETE SOURCE;
      };
      CREATE PROPERTY payment_date: std::cal::local_date;
      CREATE REQUIRED LINK account: default::BankAccount {
          ON TARGET DELETE RESTRICT;
      };
      CREATE PROPERTY ignore_in_totals: std::bool {
          SET default := false;
      };
      CREATE PROPERTY status: std::bool {
          SET default := false;
      };
      CREATE PROPERTY value: std::decimal;
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
                  __new__.type_tag
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
      CREATE TRIGGER update_balance_on_delete
          AFTER DELETE 
          FOR EACH 
              WHEN (((__old__.status = true) AND (__old__.ignore_in_totals = false)))
          DO (UPDATE
              default::BankAccount
          FILTER
              (.id = __old__.account.id)
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
              (.id = __new__.account.id)
          SET {
              balance := (.balance + (__new__.value * (IF (__new__.type_tag = 'income') THEN 1 ELSE -1)))
          });
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
                  __new__.type_tag
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
      CREATE LINK event: default::Scheduler {
          ON SOURCE DELETE DELETE TARGET;
      };
      CREATE PROPERTY is_due: std::cal::local_date;
      CREATE PROPERTY name: std::str;
      CREATE TRIGGER update_event
          AFTER UPDATE 
          FOR EACH 
              WHEN (((__new__.status = true) OR (__old__.is_due != __new__.is_due)))
          DO (WITH
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
      CREATE PROPERTY category_tag: std::str;
      CREATE PROPERTY interest: std::str;
      CREATE PROPERTY penalty: std::str;
      CREATE PROPERTY subcategory_tag: std::str;
  };
  ALTER TYPE default::Movement {
      CREATE MULTI LINK payment := (.<movement[IS default::Payment]);
      CREATE LINK accounts := (DISTINCT (__source__.payment.account));
      CREATE PROPERTY installment := (std::count(__source__.payment));
      CREATE PROPERTY value := (std::sum(__source__.payment.value));
  };
  ALTER TYPE default::User {
      CREATE LINK payment := (SELECT
          __source__.movement.payment
      ORDER BY
          .payment_date DESC
      );
  };
  ALTER TYPE default::UserSettings {
      CREATE LINK default_bank_account: default::BankAccount;
  };
  ALTER TYPE default::Individual {
      CREATE MULTI LINK projects := (.<people[IS default::Project]);
      CREATE MULTI LINK shared_schdeule := (__source__.projects.schedule);
  };
  ALTER TYPE default::Project {
      CREATE MULTI LINK movement: default::Movement {
          ON SOURCE DELETE DELETE TARGET;
          ON TARGET DELETE ALLOW;
      };
  };
  ALTER TYPE default::Record {
      CREATE MULTI LINK movement: default::Movement {
          ON SOURCE DELETE DELETE TARGET;
          ON TARGET DELETE ALLOW;
      };
  };
};
