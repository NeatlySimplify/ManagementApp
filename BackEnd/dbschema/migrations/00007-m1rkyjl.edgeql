CREATE MIGRATION m1rkyjlnabpl2vbbqlubsouzmxrkzts2i5lb54ogcpyibuw6bw76oq
    ONTO m1cf3iwyndjivuugqag36iyzhcbwzukcknlxdntfmlkgmrqeh3s7dq
{
  CREATE EXTENSION pgcrypto VERSION '1.3';
  CREATE EXTENSION auth VERSION '1.0';
  ALTER TYPE default::Account {
      DROP ACCESS POLICY admin_only;
      DROP ACCESS POLICY user_access;
      DROP LINK grouping;
      DROP LINK collaborator_pool;
  };
  ALTER TYPE default::Administator {
      DROP ACCESS POLICY admin_only;
  };
  ALTER TYPE default::Auditable {
      DROP ACCESS POLICY admin_only;
      DROP ACCESS POLICY allow_all_inserts;
  };
  ALTER TYPE default::Individual {
      DROP ACCESS POLICY admin_only;
      DROP ACCESS POLICY user_access;
      DROP LINK shared_schdeule;
      DROP LINK projects;
  };
  ALTER TYPE default::Entity {
      DROP ACCESS POLICY user_access;
      DROP LINK address;
      DROP LINK phone;
  };
  ALTER TYPE default::Movement {
      DROP ACCESS POLICY user_access;
      DROP LINK accounts;
  };
  DROP TYPE default::Project;
  ALTER TYPE default::Record {
      DROP ACCESS POLICY user_access;
      DROP LINK entity;
      DROP LINK movement;
      DROP LINK event;
  };
  ALTER TYPE default::User {
      DROP LINK account;
      DROP LINK entity;
      DROP LINK event;
      DROP LINK payment_expense;
      DROP LINK payment_income;
      DROP LINK movement;
      DROP LINK record;
      DROP TRIGGER log_insert;
      DROP TRIGGER log_update;
  };
  ALTER TYPE default::Payment {
      DROP TRIGGER update_balance_on_account_change;
      DROP TRIGGER update_balance_on_insert;
      DROP TRIGGER update_balance_on_same_account_changes;
      DROP PROPERTY type_tag;
      DROP TRIGGER update_balance_on_delete;
      DROP LINK account;
  };
  DROP GLOBAL default::current_user_obj;
  DROP GLOBAL default::current_user;
  ALTER TYPE default::User {
      DROP LINK settings;
      DROP PROPERTY email;
      DROP PROPERTY first_access;
  };
  ALTER TYPE default::Administator {
      ALTER PROPERTY is_admin {
          DROP OWNED;
      };
      ALTER PROPERTY tag_type {
          DROP OWNED;
      };
  };
  ALTER TYPE default::User {
      DROP PROPERTY is_admin;
      DROP PROPERTY name;
      DROP PROPERTY password;
      DROP PROPERTY refresh_token;
  };
  ALTER TYPE default::Account {
      ALTER PROPERTY tag_type {
          DROP OWNED;
      };
  };
  ALTER TYPE default::Individual {
      ALTER PROPERTY tag_type {
          DROP OWNED;
      };
  };
  ALTER TYPE default::User {
      DROP PROPERTY tag_type;
      DROP PROPERTY timestamp;
      DROP PROPERTY use_token;
  };
  DROP TYPE default::Account;
  DROP TYPE default::Address;
  DROP TYPE default::Administator;
  DROP TYPE default::Auditable;
  ALTER TYPE default::BankAccount {
      DROP LINK owner;
      DROP PROPERTY account_name;
      DROP PROPERTY balance;
      DROP PROPERTY bank_name;
      DROP PROPERTY category_tag;
      DROP PROPERTY ignore_on_totals;
      DROP PROPERTY notes;
      DROP PROPERTY type_tag;
  };
  DROP TYPE default::UserSettings;
  DROP TYPE default::BankAccount;
  DROP TYPE default::Contact;
  DROP TYPE default::Entity;
  DROP TYPE default::Individual;
  ALTER TYPE default::Movement {
      DROP LINK owner;
      DROP PROPERTY installment;
      DROP PROPERTY value;
      DROP LINK payment;
      DROP LINK record;
      DROP PROPERTY notes;
      DROP PROPERTY type_tag;
  };
  DROP TYPE default::Payment;
  DROP TYPE default::Movement;
  DROP TYPE default::Record;
  DROP TYPE default::Scheduler;
  DROP TYPE default::User;
};
