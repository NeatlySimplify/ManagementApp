CREATE MIGRATION m1e3grvfmzkwxba7amystueczisyooqkjo2esaccyi5nv3z4hofnna
    ONTO m1bezoyh2bhcrt6glzfocrjccallmlezoetp2ullyhqy4hzamsfvqq
{
  ALTER TYPE default::Movement {
      DROP LINK account;
  };
  ALTER TYPE default::Payment {
      ALTER LINK account {
          SET REQUIRED USING (<default::BankAccount>{});
      };
  };
  ALTER TYPE default::Movement {
      CREATE LINK accounts := (DISTINCT (__source__.payment.account));
  };
};
