CREATE MIGRATION m1mqsdqrodlki6jziotuwtljapip2khc5v2w6ee3wkx54oybdnikfa
    ONTO m1todhkafke6rx6osihnuafp6tyybygyhcekbi37dpghuj34ftojrq
{
  ALTER TYPE default::Payment {
      ALTER PROPERTY type {
          USING (__source__.movement.type);
      };
  };
};
