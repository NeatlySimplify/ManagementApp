CREATE MIGRATION m1kwnhhx3dy4ra6f37thm45q5s27yzk6yyc6adwrnfwcusicvjkweq
    ONTO m1fihnrqkufai2744uxkgpgpwiognnr4iqnhafzytzwxj4enrsffda
{
  ALTER TYPE default::BankAccount {
      ALTER PROPERTY ignore_on_totals {
          SET default := (<std::bool>false);
      };
  };
  ALTER TYPE default::Movement {
      ALTER PROPERTY charges {
          RENAME TO interest;
      };
      ALTER PROPERTY name {
          RESET OPTIONALITY;
      };
  };
  ALTER TYPE default::Movement {
      CREATE PROPERTY penalty: std::decimal {
          SET default := 0;
      };
      ALTER PROPERTY type {
          RESET OPTIONALITY;
      };
      ALTER PROPERTY value {
          RESET OPTIONALITY;
      };
  };
  ALTER TYPE default::Scheduler {
      ALTER PROPERTY name {
          RESET OPTIONALITY;
      };
  };
  ALTER TYPE default::UserSettings {
      CREATE PROPERTY entity_id_types: array<std::str> {
          SET default := (['CPF', 'CNPJ', 'RG', 'CNH']);
      };
      ALTER PROPERTY entity_types {
          SET default := (['Cliente', 'Parceiro']);
      };
  };
};
