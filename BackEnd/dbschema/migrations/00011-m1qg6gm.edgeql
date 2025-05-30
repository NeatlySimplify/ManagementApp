CREATE MIGRATION m1qg6gms5kc2itqq5uidll64cawnyrduztby52rscxvg6addnfq7ra
    ONTO m1mglgqhilg4pmspvm6pzg73beq34naljejuqycyoe3csmmemmtcga
{
  DROP FUNCTION default::balanceTotal(user_id: std::uuid);
  ALTER TYPE default::BankAccount {
      ALTER PROPERTY balance {
          SET TYPE std::decimal USING (std::to_decimal(<std::str>.balance));
      };
  };
  CREATE FUNCTION default::balanceTotal(user_id: std::uuid) ->  std::decimal USING (WITH
      total := 
          std::assert_single((SELECT
              default::InternalUser
          FILTER
              (.id = <std::uuid>user_id)
          ))
      ,
      total_balance := 
          (SELECT
              total.account.balance
          )
  SELECT
      std::sum(total_balance)
  );
  ALTER TYPE default::Movement {
      ALTER PROPERTY value {
          SET TYPE std::decimal USING (std::to_decimal(<std::str>.value));
      };
  };
  ALTER TYPE default::Payment {
      ALTER PROPERTY value {
          SET TYPE std::decimal USING (std::to_decimal(<std::str>.value));
      };
  };
  ALTER TYPE default::Record {
      ALTER PROPERTY value {
          SET TYPE std::decimal USING (std::to_decimal(<std::str>.value));
      };
  };
};
