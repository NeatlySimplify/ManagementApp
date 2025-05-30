CREATE MIGRATION m1ry6ic46lmrchc2ann7fnnm2ghqkoay6emzwmg4iskfgii7cahj5a
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
  CREATE TYPE default::PhoneNumber {
      CREATE PROPERTY number: std::str;
      CREATE PROPERTY type: std::str;
  };
  CREATE TYPE default::Contact {
      CREATE MULTI LINK number: default::PhoneNumber;
      CREATE PROPERTY details: std::str;
      CREATE PROPERTY email: std::str;
      CREATE PROPERTY name: std::str;
  };
  CREATE TYPE default::Entity {
      CREATE MULTI LINK address: default::Address {
          ON SOURCE DELETE DELETE TARGET;
          ON TARGET DELETE ALLOW;
      };
      CREATE PROPERTY birth: std::cal::local_date;
      CREATE OPTIONAL PROPERTY details: std::str;
      CREATE REQUIRED PROPERTY email: std::str {
          CREATE CONSTRAINT std::exclusive;
      };
      CREATE PROPERTY govt_id: std::str;
      CREATE PROPERTY name: std::str;
      CREATE PROPERTY relationship_status: std::str;
      CREATE PROPERTY sex: std::str;
      CREATE PROPERTY status: std::bool {
          SET default := true;
      };
      CREATE PROPERTY timestamp: std::datetime {
          SET default := (std::datetime_of_statement());
      };
      CREATE PROPERTY type_entity: std::str;
      CREATE MULTI LINK phone: default::Contact {
          ON SOURCE DELETE DELETE TARGET;
          ON TARGET DELETE ALLOW;
      };
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
  CREATE TYPE default::InternalUser EXTENDING default::User {
      CREATE PROPERTY isActive: std::bool {
          SET default := false;
      };
      CREATE PROPERTY lastActiveDate: std::datetime;
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
  CREATE TYPE default::BankAccount {
      CREATE PROPERTY balance: std::float64 {
          SET default := 0;
          CREATE CONSTRAINT std::min_value(0);
      };
      CREATE REQUIRED LINK user: default::InternalUser;
      CREATE REQUIRED PROPERTY accountName: std::str;
      CREATE REQUIRED PROPERTY bankName: std::str;
      CREATE PROPERTY category: std::str;
      CREATE PROPERTY details: std::str;
      CREATE PROPERTY ignore_on_totals: std::bool;
  };
  CREATE TYPE default::Movement {
      CREATE LINK user: default::InternalUser;
      CREATE PROPERTY category: std::str;
      CREATE PROPERTY cycle: std::str;
      CREATE PROPERTY effective: std::bool {
          SET default := false;
      };
      CREATE PROPERTY installment: std::int64;
      CREATE REQUIRED PROPERTY name: std::str;
      CREATE PROPERTY subcategory: std::str;
      CREATE REQUIRED PROPERTY type: std::str;
      CREATE REQUIRED PROPERTY value: std::float64;
      CREATE REQUIRED SINGLE LINK account: default::BankAccount;
  };
  ALTER TYPE default::InternalUser {
      CREATE MULTI LINK movement := (.<user[IS default::Movement]);
  };
  CREATE FUNCTION default::MovementNum(user_id: std::uuid) ->  std::int64 USING (WITH
      movements := 
          std::assert_single((SELECT
              default::InternalUser
          FILTER
              (.id = <std::uuid>user_id)
          ))
      ,
      total_movement := 
          (SELECT
              movements.movement
          )
  SELECT
      std::count(total_movement)
  );
  CREATE ABSTRACT TYPE default::Record_OR_Payment;
  CREATE TYPE default::Record EXTENDING default::Record_OR_Payment {
      CREATE LINK user: default::InternalUser;
      CREATE OPTIONAL PROPERTY details: std::str;
      CREATE PROPERTY id_Service: std::str;
      CREATE PROPERTY name: std::str;
      CREATE PROPERTY status: std::bool;
      CREATE PROPERTY value: std::float64;
      CREATE REQUIRED MULTI LINK entity: default::Entity {
          ON SOURCE DELETE DELETE TARGET;
          ON TARGET DELETE ALLOW;
      };
      CREATE MULTI LINK movement: default::Movement {
          ON SOURCE DELETE DELETE TARGET;
          ON TARGET DELETE ALLOW;
      };
  };
  ALTER TYPE default::InternalUser {
      CREATE MULTI LINK record := (.<user[IS default::Record]);
      CREATE MULTI LINK account: default::BankAccount {
          ON SOURCE DELETE DELETE TARGET;
          ON TARGET DELETE ALLOW;
          CREATE CONSTRAINT std::exclusive;
      };
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
  CREATE FUNCTION default::balanceTotal(user_id: std::uuid) ->  std::float64 USING (WITH
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
  CREATE TYPE default::Payment EXTENDING default::Record_OR_Payment {
      CREATE LINK user: default::InternalUser;
      CREATE LINK movement: default::Movement {
          ON TARGET DELETE DELETE SOURCE;
      };
      CREATE PROPERTY isDue: std::cal::local_date;
      CREATE PROPERTY payment_type: std::str;
      CREATE PROPERTY status: std::bool {
          SET default := false;
      };
      CREATE PROPERTY paymentDate: std::cal::local_date;
      CREATE PROPERTY charges: std::float64 {
          SET default := 0;
      };
      CREATE PROPERTY ignore_in_totals: std::bool {
          SET default := false;
      };
      CREATE PROPERTY name: std::str;
      CREATE PROPERTY part: std::int64;
      CREATE PROPERTY value: std::float64;
  };
  CREATE TYPE default::Scheduler {
      CREATE LINK user: default::InternalUser;
      CREATE OPTIONAL LINK origin: default::Record_OR_Payment;
      CREATE PROPERTY date: std::cal::local_date;
      CREATE PROPERTY date_month: std::float64 {
          SET default := (std::cal::date_get(.date, 'month'));
      };
      CREATE PROPERTY date_year: std::float64 {
          SET default := (std::cal::date_get(.date, 'year'));
      };
      CREATE REQUIRED PROPERTY name: std::str;
      CREATE PROPERTY status: std::bool {
          SET default := false;
      };
      CREATE PROPERTY tag_type: std::str;
      CREATE PROPERTY beginning_time: std::cal::local_time;
      CREATE OPTIONAL PROPERTY details: std::str;
      CREATE OPTIONAL PROPERTY ending_time: std::cal::local_time;
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
      CREATE MULTI LINK payment := (SELECT
          default::Payment
      FILTER
          (.movement.id = __source__.id)
      );
      CREATE SINGLE LINK record: default::Record;
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
      CREATE MULTI LINK event: default::Scheduler {
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
  };
  CREATE TYPE default::UserSettings {
      CREATE LINK default_BankAccount: default::BankAccount;
      CREATE PROPERTY acount_types: array<std::str> {
          SET default := (['Conta Corrente', 'Conta Poupança', 'Investimentos', 'Carteira']);
      };
      CREATE PROPERTY entity_title: std::str;
      CREATE PROPERTY entity_types: array<std::str> {
          SET default := (['Cliente']);
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
  ALTER TYPE default::InternalUser {
      CREATE LINK settings: default::UserSettings;
  };
  ALTER TYPE default::Payment {
      CREATE LINK event: default::Scheduler {
          ON SOURCE DELETE DELETE TARGET;
          ON TARGET DELETE RESTRICT;
      };
      CREATE TRIGGER create_event
          AFTER INSERT 
          FOR EACH DO (WITH
              data := 
                  (INSERT
                      default::Scheduler
                      {
                          user := __new__.user,
                          name := __new__.movement.name,
                          tag_type := __new__.payment_type,
                          status := __new__.status,
                          date := __new__.isDue,
                          origin := <default::Record_OR_Payment>__new__.id
                      })
          UPDATE
              default::Payment
          FILTER
              (.id = __new__.id)
          SET {
              event := data
          });
      CREATE TRIGGER update_event
          AFTER UPDATE 
          FOR EACH 
              WHEN (((__new__.status = true) OR (__old__.isDue != __new__.isDue)))
          DO (WITH
              new_status := 
                  __new__.status
              ,
              old_status := 
                  __old__.status
              ,
              new_isDue := 
                  __new__.isDue
              ,
              payment_date := 
                  __new__.paymentDate
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
