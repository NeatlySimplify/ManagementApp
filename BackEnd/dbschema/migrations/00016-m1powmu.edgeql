CREATE MIGRATION m1powmuuivi4ueip5suofhfqvgxuuwj4i7ucy72am4drusjr55a3ea
    ONTO m1e7xpsizznrpqua2boe5fygwq6hzwrvcgmer2vunnxmy4uvdckvza
{
  ALTER TYPE default::BankAccount {
      DROP LINK details;
  };
  ALTER TYPE default::BankAccount {
      CREATE PROPERTY notes: std::json;
  };
  ALTER TYPE default::Contact {
      DROP LINK details;
  };
  ALTER TYPE default::Contact {
      CREATE PROPERTY notes: std::json;
  };
  ALTER TYPE default::Entity {
      DROP LINK details;
  };
  ALTER TYPE default::Movement {
      DROP LINK details;
  };
  ALTER TYPE default::Record {
      DROP LINK details;
  };
  ALTER TYPE default::Scheduler {
      DROP LINK details;
  };
  DROP TYPE default::Details;
  ALTER TYPE default::Entity {
      CREATE PROPERTY notes: std::json;
  };
  ALTER TYPE default::Movement {
      CREATE PROPERTY notes: std::json;
  };
  ALTER TYPE default::Record {
      CREATE PROPERTY notes: std::json;
  };
  ALTER TYPE default::Scheduler {
      CREATE PROPERTY notes: std::json;
  };
};
