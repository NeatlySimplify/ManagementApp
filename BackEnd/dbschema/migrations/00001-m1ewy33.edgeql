CREATE MIGRATION m1ewy335uiavcvrm2z7swivimluhmanxwio75diher4ihz6j6nnb2q
    ONTO initial
{
  CREATE FUTURE simple_scoping;
  CREATE GLOBAL default::current_user -> std::uuid;
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
      CREATE PROPERTY extra_email: std::str;
      CREATE PROPERTY notes: std::json;
      CREATE PROPERTY number: std::str;
      CREATE PROPERTY type_tag: std::str;
  };
  CREATE ABSTRACT TYPE default::User {
      CREATE REQUIRED PROPERTY email: std::str {
          CREATE DELEGATED CONSTRAINT std::exclusive;
      };
      CREATE PROPERTY first_access: std::bool {
          SET default := true;
      };
      CREATE PROPERTY is_admin: std::bool {
          SET default := (<std::bool>false);
      };
      CREATE REQUIRED PROPERTY name: std::str;
      CREATE REQUIRED PROPERTY password: std::str;
      CREATE PROPERTY refresh_token: std::uuid;
      CREATE PROPERTY tag_type: std::str;
      CREATE PROPERTY timestamp: std::datetime {
          SET default := (std::datetime_of_statement());
      };
      CREATE PROPERTY use_token: std::bool {
          SET default := false;
      };
  };
  CREATE TYPE default::BankAccount {
      CREATE REQUIRED LINK owner: default::User {
          ON TARGET DELETE DELETE SOURCE;
      };
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
      CREATE PROPERTY type_tag: std::str;
  };
  CREATE TYPE default::Entity {
      CREATE REQUIRED LINK owner: default::User {
          ON TARGET DELETE DELETE SOURCE;
      };
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
      CREATE PROPERTY type_tag: std::str;
  };
  CREATE TYPE default::Scheduler {
      CREATE REQUIRED LINK owner: default::User {
          ON TARGET DELETE DELETE SOURCE;
      };
      CREATE PROPERTY date: std::cal::local_date;
      CREATE PROPERTY name: std::str;
      CREATE PROPERTY status: std::bool {
          SET default := false;
      };
      CREATE PROPERTY beginning_time: std::cal::local_time;
      CREATE OPTIONAL PROPERTY ending_time: std::cal::local_time;
      CREATE PROPERTY notes: std::json;
      CREATE PROPERTY type_tag: std::str;
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
  };
  CREATE TYPE default::UserSettings {
      CREATE LINK default_bank_account: default::BankAccount;
      CREATE PROPERTY account_types: array<std::str> {
          SET default := (['Conta Corrente', 'Conta Poupança', 'Investimentos', 'Carteira']);
      };
      CREATE PROPERTY contact_number_types: array<std::str> {
          SET default := (['Casa', 'Celular', 'Trabalho']);
      };
      CREATE PROPERTY entity_document_types: array<std::str> {
          SET default := (['CPF', 'CNPJ', 'RG', 'CNH']);
      };
      CREATE PROPERTY entity_title: std::str;
      CREATE PROPERTY entity_types: array<std::str> {
          SET default := (['Cliente PF', 'Cliente PJ', 'Sócio']);
      };
      CREATE PROPERTY movement_cycle_types: array<std::str> {
          SET default := (['Diário', 'Semanal', 'Quinzenal', 'Mensal', 'Trimestral', 'Semestral', 'Anual', 'Personalizado']);
      };
      CREATE PROPERTY movement_expense_types: array<std::str> {
          SET default := (['Alimentação', 'Transporte', 'Cartão de Crédito', 'Educação', 'Família', 'Lazer', 'Moradia', 'Pagamentos', 'Saúde', 'Serviços', 'Outros']);
      };
      CREATE PROPERTY movement_income_types: array<std::str> {
          SET default := (['Benefícios', 'Comissão', 'Pagamentos', 'Rendimentos', 'Serviços', 'Outros']);
      };
      CREATE PROPERTY movement_title: std::str;
      CREATE PROPERTY record_status: array<std::str> {
          SET default := (['Em Andamento', 'Concluído']);
      };
      CREATE PROPERTY record_title: std::str;
      CREATE PROPERTY record_types: array<std::str> {
          SET default := (['Serviço']);
      };
      CREATE PROPERTY scheduler_types: array<std::str> {
          SET default := (['Evento', 'Tarefa', 'Reunião']);
      };
  };
  ALTER TYPE default::User {
      CREATE LINK settings: default::UserSettings {
          ON SOURCE DELETE DELETE TARGET;
      };
  };
  CREATE GLOBAL default::current_user_obj := (std::assert_single((SELECT
      default::User
  FILTER
      (.id = GLOBAL default::current_user)
  )));
  CREATE TYPE default::Account EXTENDING default::User {
      CREATE ACCESS POLICY admin_only
          ALLOW ALL USING (((GLOBAL default::current_user_obj).is_admin ?? false));
      CREATE ACCESS POLICY user_access
          ALLOW SELECT, UPDATE USING ((__subject__ ?= GLOBAL default::current_user_obj));
      ALTER PROPERTY tag_type {
          SET default := 'is_account';
          SET OWNED;
          SET TYPE std::str;
      };
  };
  CREATE TYPE default::Auditable {
      CREATE ACCESS POLICY admin_only
          ALLOW SELECT, UPDATE, DELETE USING (((GLOBAL default::current_user_obj).is_admin ?? false));
      CREATE PROPERTY action: std::str;
      CREATE PROPERTY details: std::json;
      CREATE PROPERTY object_id: std::uuid;
      CREATE PROPERTY user: std::uuid;
      CREATE ACCESS POLICY allow_all_inserts
          ALLOW INSERT USING (true);
      CREATE PROPERTY timestamp: std::datetime {
          SET default := (std::datetime_of_statement());
      };
  };
  CREATE TYPE default::Individual EXTENDING default::User {
      CREATE ACCESS POLICY admin_only
          ALLOW ALL USING (((GLOBAL default::current_user_obj).is_admin ?? false));
      CREATE ACCESS POLICY user_access
          ALLOW SELECT, UPDATE, DELETE USING ((__subject__ ?= GLOBAL default::current_user_obj));
      ALTER PROPERTY tag_type {
          SET default := 'is_individual';
          SET OWNED;
          SET TYPE std::str;
      };
  };
  ALTER TYPE default::Entity {
      CREATE ACCESS POLICY user_access
          ALLOW ALL USING ((__subject__.owner ?= GLOBAL default::current_user_obj));
  };
  CREATE TYPE default::Movement {
      CREATE REQUIRED LINK owner: default::User {
          ON TARGET DELETE DELETE SOURCE;
      };
      CREATE ACCESS POLICY user_access
          ALLOW ALL USING ((__subject__.owner ?= GLOBAL default::current_user_obj));
      CREATE REQUIRED PROPERTY type_tag: std::str;
      CREATE PROPERTY notes: std::json;
  };
  CREATE TYPE default::Record {
      CREATE REQUIRED LINK owner: default::User {
          ON TARGET DELETE DELETE SOURCE;
      };
      CREATE ACCESS POLICY user_access
          ALLOW ALL USING ((__subject__.owner ?= GLOBAL default::current_user_obj));
      CREATE MULTI LINK entity: default::Entity {
          ON TARGET DELETE ALLOW;
      };
      CREATE MULTI LINK movement: default::Movement {
          ON SOURCE DELETE DELETE TARGET;
          ON TARGET DELETE ALLOW;
      };
      CREATE MULTI LINK event: default::Scheduler;
      CREATE PROPERTY name: std::str;
      CREATE PROPERTY notes: std::json;
      CREATE PROPERTY optional_status: std::str;
      CREATE PROPERTY service_id: std::str;
      CREATE PROPERTY status: std::bool;
      CREATE PROPERTY type_tag: std::str;
      CREATE PROPERTY value: std::decimal;
  };
  CREATE TYPE default::Project {
      CREATE REQUIRED LINK owner: default::Account {
          ON SOURCE DELETE ALLOW;
          ON TARGET DELETE DELETE SOURCE;
      };
      CREATE ACCESS POLICY user_access
          ALLOW ALL USING ((__subject__.owner ?= GLOBAL default::current_user_obj));
      CREATE MULTI LINK people: default::Individual {
          CREATE PROPERTY role: std::str;
      };
      CREATE MULTI LINK schedule: default::Scheduler {
          ON SOURCE DELETE DELETE TARGET;
          ON TARGET DELETE ALLOW;
      };
      CREATE MULTI LINK entity: default::Entity {
          ON SOURCE DELETE ALLOW;
      };
      CREATE MULTI LINK movement: default::Movement {
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
  ALTER TYPE default::Individual {
      CREATE MULTI LINK projects := (.<people[IS default::Project]);
      CREATE MULTI LINK shared_schdeule := (__source__.projects.schedule);
  };
  CREATE TYPE default::Payment {
      CREATE REQUIRED LINK account: default::BankAccount {
          ON TARGET DELETE RESTRICT;
      };
      CREATE REQUIRED LINK movement: default::Movement {
          ON TARGET DELETE DELETE SOURCE;
      };
      CREATE PROPERTY ignore_in_totals: std::bool {
          SET default := false;
      };
      CREATE PROPERTY status: std::bool {
          SET default := false;
      };
      CREATE PROPERTY type_tag := (__source__.movement.type_tag);
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
      CREATE PROPERTY payment_date: std::cal::local_date;
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
      CREATE LINK owner: default::User;
      CREATE PROPERTY category_tag: std::str;
      CREATE PROPERTY interest: std::str;
      CREATE PROPERTY penalty: std::str;
      CREATE PROPERTY subcategory_tag: std::str;
  };
  ALTER TYPE default::User {
      CREATE MULTI LINK record := (SELECT
          DETACHED default::Record
      FILTER
          (.owner = __source__)
      );
      CREATE MULTI LINK movement := (.<owner[IS default::Movement]);
  };
  ALTER TYPE default::Account {
      CREATE MULTI LINK collaborator_pool: default::Individual;
      CREATE MULTI LINK grouping := (.<owner[IS default::Project]);
  };
  ALTER TYPE default::Movement {
      CREATE MULTI LINK payment := (.<movement[IS default::Payment]);
      CREATE LINK accounts := (DISTINCT (__source__.payment.account));
      CREATE PROPERTY installment := (std::count(__source__.payment));
      CREATE PROPERTY value := (std::sum(__source__.payment.value));
      CREATE LINK record: default::Record;
  };
  ALTER TYPE default::User {
      CREATE LINK payment_expense := (SELECT
          __source__.movement.payment
      FILTER
          (.type_tag = 'expense')
      ORDER BY
          .payment_date DESC
      );
      CREATE LINK payment_income := (SELECT
          __source__.movement.payment
      FILTER
          (.type_tag = 'income')
      ORDER BY
          .payment_date DESC
      );
      CREATE TRIGGER log_insert
          AFTER INSERT 
          FOR EACH DO (INSERT
              default::Auditable
              {
                  user := __new__.id,
                  object_id := __new__.id,
                  action := 'insert',
                  details := <std::json>__new__ {
                      *
                  }
              });
      CREATE TRIGGER log_update
          AFTER UPDATE 
          FOR EACH 
              WHEN ((__old__.password != __new__.password))
          DO (INSERT
              default::Auditable
              {
                  user := __old__.id,
                  object_id := __old__.id,
                  action := 'update',
                  details := std::to_json((('{' ++ '"Action": "Password Updated"') ++ '}'))
              });
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
};
