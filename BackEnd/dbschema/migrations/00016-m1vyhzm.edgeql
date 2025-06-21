CREATE MIGRATION m1vyhzmixxegrlvtghpln6v56pshsqzh5dxkuhelg2tq7bfdb3irtq
    ONTO m1pmnziznpkbpqjpdcvyd4a2q75bb77fedvjacp2yjgbhgywsgmoha
{
  ALTER TYPE default::Entity {
      ALTER LINK owner {
          SET REQUIRED USING (<default::User>{});
      };
  };
  ALTER TYPE default::Movement {
      ALTER LINK owner {
          SET REQUIRED USING (<default::User>{});
      };
  };
  ALTER TYPE default::Record {
      ALTER LINK owner {
          SET REQUIRED USING (<default::User>{});
      };
  };
  ALTER TYPE default::Scheduler {
      ALTER LINK owner {
          SET REQUIRED USING (<default::User>{});
      };
  };
  ALTER GLOBAL default::current_user_obj USING (std::assert_single((SELECT
      default::User
  FILTER
      (.id = GLOBAL default::current_user)
  )));
  ALTER TYPE default::BankAccount {
      ALTER LINK owner {
          SET REQUIRED USING (<default::User>{});
      };
  };
  ALTER TYPE default::Project {
      ALTER LINK owner {
          SET REQUIRED USING (<default::Account>{});
      };
  };
};
