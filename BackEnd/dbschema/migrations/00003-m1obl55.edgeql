CREATE MIGRATION m1obl55dmyndkziefivs7wyid2cli47opacdlbiknp2a27ukxbymyq
    ONTO m1ei2o4dtlo7czklp6bfepo6fdovppqx2r7ecypoa3o2suqnotzdvq
{
  ALTER TYPE default::BankAccount {
      DROP LINK user;
      ALTER PROPERTY details {
          SET TYPE std::json USING (<std::json>.details);
      };
  };
  ALTER TYPE default::Contact {
      ALTER PROPERTY details {
          SET TYPE std::json USING (<std::json>.details);
      };
  };
  ALTER TYPE default::Entity {
      ALTER PROPERTY details {
          SET TYPE std::json USING (<std::json>.details);
      };
  };
  ALTER TYPE default::Movement {
      CREATE OPTIONAL PROPERTY details: std::json;
  };
  ALTER TYPE default::Record {
      ALTER PROPERTY details {
          SET TYPE std::json USING (<std::json>.details);
      };
  };
  ALTER TYPE default::Scheduler {
      ALTER PROPERTY details {
          SET TYPE std::json USING (<std::json>.details);
      };
  };
};
