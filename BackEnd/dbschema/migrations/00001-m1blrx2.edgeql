CREATE MIGRATION m1blrx22nx6np45ebymuxc5fmdn6vuixdbsnz3ge4gank6oewwamvq
    ONTO initial
{
  CREATE TYPE default::Address {
      CREATE PROPERTY city: std::str;
      CREATE PROPERTY complement: std::str;
      CREATE PROPERTY district: std::str;
      CREATE PROPERTY number: std::int64;
      CREATE PROPERTY postal: std::str;
      CREATE PROPERTY state: std::str;
      CREATE PROPERTY street: std::str;
  };
  CREATE ABSTRACT TYPE default::Link;
  CREATE ABSTRACT TYPE default::Metadata {
      CREATE REQUIRED LINK origin: default::Link {
          ON TARGET DELETE DELETE SOURCE;
      };
      CREATE PROPERTY field: std::str;
      CREATE PROPERTY title: std::str;
  };
  CREATE TYPE default::Details EXTENDING default::Metadata;
  CREATE TYPE default::PhoneNumber EXTENDING default::Metadata;
  CREATE TYPE default::Contact EXTENDING default::Link {
      CREATE MULTI LINK details := (SELECT
          default::Details
      FILTER
          (.id = __source__.id)
      );
      CREATE MULTI LINK number := (SELECT
          default::PhoneNumber
      FILTER
          (.id = __source__.id)
      );
      CREATE PROPERTY email: std::str;
      CREATE PROPERTY name: std::str;
  };
  CREATE TYPE default::BankAccount EXTENDING default::Link {
      CREATE PROPERTY balance: std::decimal {
          SET default := 0;
          CREATE CONSTRAINT std::min_value(0);
      };
      CREATE MULTI LINK details := (SELECT
          default::Details
      FILTER
          (.id = __source__.id)
      );
      CREATE REQUIRED PROPERTY account_name: std::str;
      CREATE REQUIRED PROPERTY bank_name: std::str;
      CREATE PROPERTY category: std::str;
      CREATE PROPERTY ignore_on_totals: std::bool {
          SET default := (<std::bool>false);
      };
      CREATE PROPERTY type: std::str;
  };
  CREATE TYPE default::Entity EXTENDING default::Link {
      CREATE MULTI LINK address: default::Address {
          ON SOURCE DELETE DELETE TARGET;
          ON TARGET DELETE ALLOW;
      };
      CREATE PROPERTY birth: std::cal::local_date;
      CREATE REQUIRED PROPERTY email: std::str {
          CREATE CONSTRAINT std::exclusive;
      };
      CREATE PROPERTY govt_id: std::str;
      CREATE PROPERTY id_type: std::str;
      CREATE PROPERTY name: std::str;
      CREATE PROPERTY relationship_status: std::str;
      CREATE PROPERTY sex: std::str;
      CREATE PROPERTY status: std::bool {
          SET default := true;
      };
      CREATE PROPERTY timestamp: std::datetime {
          SET default := (std::datetime_of_statement());
      };
      CREATE PROPERTY type: std::str;
      CREATE MULTI LINK phone: default::Contact {
          ON SOURCE DELETE DELETE TARGET;
          ON TARGET DELETE ALLOW;
      };
      CREATE MULTI LINK details := (SELECT
          default::Details
      FILTER
          (.id = __source__.id)
      );
  };
  CREATE ABSTRACT TYPE default::User {
      CREATE REQUIRED PROPERTY email: std::str {
          CREATE DELEGATED CONSTRAINT std::exclusive;
      };
      CREATE REQUIRED PROPERTY name: std::str;
      CREATE REQUIRED PROPERTY password: std::str;
      CREATE PROPERTY refresh_token: std::uuid;
      CREATE PROPERTY use_token: std::bool {
          SET default := false;
      };
  };
  CREATE TYPE default::UserSettings {
      CREATE LINK default_bank_account: default::BankAccount;
      CREATE PROPERTY account_types: array<std::str> {
          SET default := (['Conta Corrente', 'Conta Poupança', 'Investimentos', 'Carteira']);
      };
      CREATE PROPERTY contact_number_types: array<std::str> {
          SET default := (['Casa', 'Celular', 'Trabalho']);
      };
      CREATE PROPERTY entity_id_types: array<std::str> {
          SET default := (['CPF', 'CNPJ', 'RG', 'CNH']);
      };
      CREATE PROPERTY entity_title: std::str;
      CREATE PROPERTY entity_types: array<std::str> {
          SET default := (['Cliente', 'Parceiro']);
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
  CREATE TYPE default::InternalUser EXTENDING default::User {
      CREATE MULTI LINK account: default::BankAccount {
          ON SOURCE DELETE DELETE TARGET;
          ON TARGET DELETE ALLOW;
          CREATE CONSTRAINT std::exclusive;
      };
      CREATE LINK settings: default::UserSettings {
          ON SOURCE DELETE DELETE TARGET;
      };
      CREATE PROPERTY is_active: std::bool {
          SET default := false;
      };
      CREATE PROPERTY last_active_date: std::datetime;
  };
  ALTER TYPE default::Entity {
      CREATE LINK user: default::InternalUser;
  };
  ALTER TYPE default::InternalUser {
      CREATE MULTI LINK entity := (.<user[IS default::Entity]);
  };
  CREATE FUNCTION default::EntityNum(user_id: std::uuid) ->  std::int64 USING (WITH
      entities := 
          std::assert_single((SELECT
              default::InternalUser
          FILTER
              (.id = <std::uuid>user_id)
          ))
      ,
      total_entities := 
          (SELECT
              entities.entity
          )
  SELECT
      std::count(total_entities)
  );
  CREATE ABSTRACT TYPE default::Record_OR_Payment;
  CREATE TYPE default::Scheduler EXTENDING default::Link {
      CREATE LINK user: default::InternalUser;
      CREATE OPTIONAL LINK origin: default::Record_OR_Payment;
      CREATE PROPERTY date: std::cal::local_date;
      CREATE PROPERTY name: std::str;
      CREATE PROPERTY status: std::bool {
          SET default := false;
      };
      CREATE PROPERTY type: std::str;
      CREATE MULTI LINK details := (SELECT
          default::Details
      FILTER
          (.id = __source__.id)
      );
      CREATE PROPERTY beginning_time: std::cal::local_time;
      CREATE OPTIONAL PROPERTY ending_time: std::cal::local_time;
  };
  CREATE TYPE default::Record EXTENDING default::Record_OR_Payment, default::Link {
      CREATE LINK user: default::InternalUser;
      CREATE PROPERTY active: std::bool;
      CREATE PROPERTY id_service: std::str;
      CREATE PROPERTY name: std::str;
      CREATE PROPERTY status: std::str;
      CREATE PROPERTY type: std::str;
      CREATE PROPERTY value: std::decimal;
      CREATE MULTI LINK details := (SELECT
          default::Details
      FILTER
          (.id = __source__.id)
      );
      CREATE REQUIRED MULTI LINK entity: default::Entity {
          ON SOURCE DELETE DELETE TARGET;
          ON TARGET DELETE ALLOW;
      };
      CREATE MULTI LINK event: default::Scheduler {
          ON SOURCE DELETE DELETE TARGET;
          ON TARGET DELETE ALLOW;
      };
  };
  ALTER TYPE default::InternalUser {
      CREATE MULTI LINK record := (.<user[IS default::Record]);
  };
  CREATE FUNCTION default::RecordNum(user_id: std::uuid) ->  std::int64 USING (WITH
      recorded := 
          std::assert_single((SELECT
              default::InternalUser
          FILTER
              (.id = <std::uuid>user_id)
          ))
      ,
      total_record := 
          (SELECT
              recorded.record
          )
  SELECT
      std::count(total_record)
  );
  CREATE FUNCTION default::balanceTotal(user_id: std::uuid) ->  std::decimal USING (WITH
      total := 
          std::assert_single((SELECT
              default::InternalUser
          FILTER
              (.id = <std::uuid>user_id)
          ))
      ,
      total_balance := 
          (SELECT
              total.account.balance
          )
  SELECT
      std::sum(total_balance)
  );
  CREATE FUTURE simple_scoping;
  CREATE TYPE default::Auditable {
      CREATE PROPERTY action: std::str;
      CREATE PROPERTY details: std::json;
      CREATE PROPERTY object_id: std::uuid;
      CREATE PROPERTY timestamp: std::datetime {
          SET default := (std::datetime_of_statement());
      };
      CREATE PROPERTY user: std::uuid;
  };
  CREATE TYPE default::InternalOrg EXTENDING default::User {
      CREATE MULTI LINK user: default::InternalUser;
  };
  CREATE TYPE default::Movement EXTENDING default::Link {
      CREATE LINK user: default::InternalUser;
      CREATE PROPERTY type: std::str;
      CREATE MULTI LINK details := (SELECT
          default::Details
      FILTER
          (.id = __source__.id)
      );
      CREATE OPTIONAL SINGLE LINK record: default::Record;
  };
  CREATE TYPE default::Payment EXTENDING default::Record_OR_Payment {
      CREATE LINK user: default::InternalUser;
      CREATE REQUIRED LINK movement: default::Movement {
          ON TARGET DELETE DELETE SOURCE;
      };
      CREATE PROPERTY value: std::decimal;
      CREATE REQUIRED LINK account: default::BankAccount;
      CREATE LINK event: default::Scheduler {
          ON SOURCE DELETE DELETE TARGET;
          ON TARGET DELETE RESTRICT;
      };
      CREATE PROPERTY ignore_in_totals: std::bool {
          SET default := false;
      };
      CREATE PROPERTY is_due: std::cal::local_date;
      CREATE PROPERTY name: std::str;
      CREATE PROPERTY status: std::bool {
          SET default := false;
      };
      CREATE PROPERTY type := (__source__.movement.type);
      CREATE TRIGGER create_event
          AFTER INSERT 
          FOR EACH DO (WITH
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
              balance := (.balance + __new__.value)
          });
      CREATE PROPERTY payment_date: std::cal::local_date;
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
      CREATE PROPERTY category: std::str;
      CREATE PROPERTY interest: std::float64 {
          SET default := 0;
      };
      CREATE PROPERTY penalty: std::decimal {
          SET default := 0;
      };
      CREATE PROPERTY subcategory: std::str;
  };
  ALTER TYPE default::InternalUser {
      CREATE TRIGGER link_delete
          AFTER DELETE 
          FOR EACH DO (DELETE
              (SELECT
                  default::InternalUser.<user
              )
          );
  };
  ALTER TYPE default::Entity {
      CREATE TRIGGER log_delete
          AFTER DELETE 
          FOR EACH DO (INSERT
              default::Auditable
              {
                  user := __old__.user.id,
                  object_id := __old__.id,
                  action := 'delete',
                  details := <std::json>__old__ {
                      *
                  }
              });
      CREATE TRIGGER log_insert
          AFTER INSERT 
          FOR EACH DO (INSERT
              default::Auditable
              {
                  user := __new__.user.id,
                  object_id := __new__.id,
                  action := 'insert',
                  details := <std::json>__new__ {
                      *
                  }
              });
      CREATE TRIGGER log_update
          AFTER UPDATE 
          FOR EACH 
              WHEN ((<std::json>__old__ {
                  *
              } != <std::json>__new__ {
                  *
              }))
          DO (INSERT
              default::Auditable
              {
                  user := __old__.user.id,
                  object_id := __old__.id,
                  action := 'update',
                  details := std::to_json((((((('{' ++ '"before": ') ++ <std::str><std::json>__old__ {
                      *
                  }) ++ ',') ++ '"after": ') ++ <std::str><std::json>__new__ {
                      *
                  }) ++ '}'))
              });
  };
  ALTER TYPE default::Movement {
      CREATE MULTI LINK payment := (SELECT
          default::Payment
      FILTER
          (.movement.id = __source__.id)
      );
      CREATE PROPERTY installment := (std::count(__source__.payment));
      CREATE PROPERTY value := (std::sum(__source__.payment.value));
      CREATE TRIGGER log_delete
          AFTER DELETE 
          FOR EACH DO (INSERT
              default::Auditable
              {
                  user := __old__.user.id,
                  object_id := __old__.id,
                  action := 'delete',
                  details := <std::json>__old__ {
                      *
                  }
              });
      CREATE TRIGGER log_insert
          AFTER INSERT 
          FOR EACH DO (INSERT
              default::Auditable
              {
                  user := __new__.user.id,
                  object_id := __new__.id,
                  action := 'insert',
                  details := <std::json>__new__ {
                      *
                  }
              });
      CREATE TRIGGER log_update
          AFTER UPDATE 
          FOR EACH 
              WHEN ((<std::json>__old__ {
                  *
              } != <std::json>__new__ {
                  *
              }))
          DO (INSERT
              default::Auditable
              {
                  user := __old__.user.id,
                  object_id := __old__.id,
                  action := 'update',
                  details := std::to_json((((((('{' ++ '"before": ') ++ <std::str><std::json>__old__ {
                      *
                  }) ++ ',') ++ '"after": ') ++ <std::str><std::json>__new__ {
                      *
                  }) ++ '}'))
              });
      CREATE LINK accounts := (DISTINCT (__source__.payment.account));
  };
  ALTER TYPE default::Record {
      CREATE TRIGGER log_delete
          AFTER DELETE 
          FOR EACH DO (INSERT
              default::Auditable
              {
                  user := __old__.user.id,
                  object_id := __old__.id,
                  action := 'delete',
                  details := <std::json>__old__ {
                      *
                  }
              });
      CREATE TRIGGER log_insert
          AFTER INSERT 
          FOR EACH DO (INSERT
              default::Auditable
              {
                  user := __new__.user.id,
                  object_id := __new__.id,
                  action := 'insert',
                  details := <std::json>__new__ {
                      *
                  }
              });
      CREATE TRIGGER log_update
          AFTER UPDATE 
          FOR EACH 
              WHEN ((<std::json>__old__ {
                  *
              } != <std::json>__new__ {
                  *
              }))
          DO (INSERT
              default::Auditable
              {
                  user := __old__.user.id,
                  object_id := __old__.id,
                  action := 'update',
                  details := std::to_json((((((('{' ++ '"before": ') ++ <std::str><std::json>__old__ {
                      *
                  }) ++ ',') ++ '"after": ') ++ <std::str><std::json>__new__ {
                      *
                  }) ++ '}'))
              });
      CREATE MULTI LINK movement: default::Movement {
          ON SOURCE DELETE DELETE TARGET;
          ON TARGET DELETE ALLOW;
      };
  };
  ALTER TYPE default::User {
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
  ALTER TYPE default::InternalUser {
      CREATE OPTIONAL SINGLE LINK org: default::InternalOrg;
      CREATE MULTI LINK event := (.<user[IS default::Scheduler]);
      CREATE MULTI LINK movement := (.<user[IS default::Movement]);
      CREATE LINK paymente_expense := (SELECT
          __source__.movement.payment
      FILTER
          (.type = 'expense')
      ORDER BY
          .payment_date DESC
      );
      CREATE LINK paymente_income := (SELECT
          __source__.movement.payment
      FILTER
          (.type = 'income')
      ORDER BY
          .payment_date DESC
      );
  };
};
