CREATE MIGRATION m1whlsi2eirfit4cgfsjrzrtmq7qagtcx2vtq2rskepawfim4jeg7a
    ONTO m1aljomffl6sdnahdu7wfki6hqsuraodryg6apr5rxmhfbn7zurtuq
{
  ALTER TYPE default::Entity {
      ALTER PROPERTY status {
          SET default := false;
      };
  };
  ALTER TYPE default::Payment {
      DROP PROPERTY interest;
      DROP PROPERTY penalty;
      DROP PROPERTY subcategory_tag;
  };
  ALTER TYPE default::UserSettings {
      CREATE PROPERTY movement_types: array<std::str> {
          SET default := (['Entrada', 'Saída']);
      };
  };
};
