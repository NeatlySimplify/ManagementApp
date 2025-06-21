CREATE MIGRATION m1i4efgm4v4ssp4n3qo4hhm73amjr7wrp4vrfocb2ourvkbrpxpw5q
    ONTO m1vdypnnqgdfe6xw2xuehnh7s6dyzyxx7hdvbouzo5se47d4ywujoq
{
  ALTER TYPE default::Record {
      ALTER LINK onwer {
          RENAME TO owner;
      };
  };
  ALTER TYPE default::User {
      CREATE MULTI LINK record := (SELECT
          DETACHED default::Record
      FILTER
          (.owner = __source__)
      );
  };
};
