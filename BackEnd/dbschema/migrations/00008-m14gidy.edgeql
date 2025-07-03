CREATE MIGRATION m14gidynwnvadymer4rjcjoyyec2vncqp4y7at67ovws6ttyd2hubq
    ONTO m1rkyjlnabpl2vbbqlubsouzmxrkzts2i5lb54ogcpyibuw6bw76oq
{
  CREATE TYPE default::UserSettings {
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
      CREATE PROPERTY relationship_status: array<std::str> {
          SET default := (['Casado(a)', 'Viúvo(a)', 'Solteiro(a)', 'Divorciádo(a)', 'Em União Estável']);
      };
      CREATE PROPERTY scheduler_types: array<std::str> {
          SET default := (['Evento', 'Tarefa', 'Reunião']);
      };
      CREATE PROPERTY sex: array<std::str> {
          SET default := (['Masculino', 'Feminino', 'Outro']);
      };
  };
  CREATE ABSTRACT TYPE default::User {
      CREATE REQUIRED LINK identity: ext::auth::Identity {
          CREATE CONSTRAINT std::exclusive;
      };
      CREATE LINK settings: default::UserSettings {
          ON SOURCE DELETE DELETE TARGET;
      };
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
      CREATE PROPERTY refresh_token: std::uuid;
      CREATE PROPERTY tag_type: std::str;
      CREATE PROPERTY timestamp: std::datetime {
          SET default := (std::datetime_of_statement());
      };
      CREATE PROPERTY use_token: std::bool {
          SET default := false;
      };
  };
  CREATE GLOBAL default::current_user := (std::assert_single((SELECT
      default::User
  FILTER
      (.identity = GLOBAL ext::auth::ClientTokenIdentity)
  )));
  CREATE TYPE default::Auditable {
      CREATE ACCESS POLICY admin_only
          ALLOW UPDATE, DELETE USING (((GLOBAL default::current_user).is_admin ?? false));
      CREATE ACCESS POLICY allow_all_inserts
          ALLOW INSERT USING (true);
      CREATE PROPERTY action: std::str;
      CREATE PROPERTY details: std::json;
      CREATE PROPERTY object_id: std::uuid;
      CREATE PROPERTY user: std::uuid;
      CREATE PROPERTY timestamp: std::datetime {
          SET default := (std::datetime_of_statement());
      };
  };
  CREATE ABSTRACT TYPE default::Derived {
      CREATE LINK owner: default::User {
          SET default := (GLOBAL default::current_user);
          ON SOURCE DELETE ALLOW;
          ON TARGET DELETE DELETE SOURCE;
      };
      CREATE ACCESS POLICY allow_user
          ALLOW ALL USING ((GLOBAL default::current_user ?= __subject__.owner));
      CREATE PROPERTY type_tag: std::str;
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
  };
  CREATE TYPE default::RefreshToken {
      CREATE REQUIRED LINK identity: ext::auth::Identity;
      CREATE REQUIRED PROPERTY email: std::str;
      CREATE REQUIRED PROPERTY encrypted_password: std::str;
      CREATE REQUIRED PROPERTY expires_at: std::datetime;
      CREATE REQUIRED PROPERTY token: std::str;
  };
};
