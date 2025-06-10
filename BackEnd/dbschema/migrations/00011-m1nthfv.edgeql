CREATE MIGRATION m1nthfvjmplan357ax2vgca4odplwmkayd7jkkpa2bl76zxorg33ca
    ONTO m1nr2cc6ujtnp2oq2fwnh43jjeykf6g6kvqut7kghhhtg24kxf5cra
{
  ALTER TYPE default::Entity {
      ALTER LINK user {
          ON TARGET DELETE DELETE SOURCE;
      };
  };
  ALTER TYPE default::InternalOrg {
      ALTER LINK user {
          ON TARGET DELETE ALLOW;
      };
  };
  ALTER TYPE default::Movement {
      ALTER LINK user {
          ON TARGET DELETE DELETE SOURCE;
      };
  };
  ALTER TYPE default::Payment {
      ALTER LINK user {
          ON TARGET DELETE DELETE SOURCE;
      };
      ALTER TRIGGER update_balance_on_insert USING (UPDATE
          default::BankAccount
      FILTER
          (.id = __new__.account.id)
      SET {
          balance := (.balance + (__new__.value * (IF (__new__.type = 'income') THEN 1 ELSE -1)))
      });
  };
  ALTER TYPE default::Record {
      ALTER LINK user {
          ON TARGET DELETE DELETE SOURCE;
      };
  };
  ALTER TYPE default::Scheduler {
      ALTER LINK user {
          ON TARGET DELETE DELETE SOURCE;
      };
  };
};
