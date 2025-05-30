CREATE MIGRATION m1emt4t7zkt46np2dohzfat3suulmvilcviqggcyzdszzeca4k6deq
    ONTO m1m22gxolvg2nvzln4vyjbsxr7lpeynxckgribznrmjed7pn6r727a
{
  ALTER TYPE default::BankAccount {
      CREATE PROPERTY type: std::str;
  };
  ALTER TYPE default::Entity {
      CREATE PROPERTY type: std::str;
  };
  ALTER TYPE default::Entity {
      CREATE PROPERTY id_type: std::str;
      DROP PROPERTY type_entity;
  };
  ALTER TYPE default::Payment {
      ALTER PROPERTY payment_type {
          RENAME TO type;
      };
  };
  ALTER TYPE default::Scheduler {
      ALTER PROPERTY tag_type {
          RENAME TO type;
      };
  };
  ALTER TYPE default::Record {
      CREATE PROPERTY active: std::bool;
      ALTER PROPERTY status {
          SET TYPE std::str USING (<std::str>.status);
      };
      CREATE PROPERTY type: std::str;
  };
};
