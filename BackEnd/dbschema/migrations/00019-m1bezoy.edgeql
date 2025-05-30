CREATE MIGRATION m1bezoyh2bhcrt6glzfocrjccallmlezoetp2ullyhqy4hzamsfvqq
    ONTO m1mqsdqrodlki6jziotuwtljapip2khc5v2w6ee3wkx54oybdnikfa
{
  ALTER TYPE default::Movement {
      CREATE REQUIRED SINGLE LINK account: default::BankAccount {
          SET REQUIRED USING (<default::BankAccount>{});
      };
      CREATE PROPERTY details: std::json;
  };
  ALTER TYPE default::Payment {
      ALTER LINK account {
          RESET CARDINALITY;
          RESET OPTIONALITY;
      };
      ALTER LINK movement {
          SET REQUIRED USING (<default::Movement>{});
      };
  };
};
