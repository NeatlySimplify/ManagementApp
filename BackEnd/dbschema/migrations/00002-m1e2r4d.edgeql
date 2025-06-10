CREATE MIGRATION m1e2r4dhcbnnjm23sxfqhzwcb4mehbj7ezyrqurnlgyfyllu2hx5dq
    ONTO m1blrx22nx6np45ebymuxc5fmdn6vuixdbsnz3ge4gank6oewwamvq
{
  ALTER TYPE default::BankAccount {
      ALTER LINK details {
          USING (SELECT
              default::Details
          FILTER
              (.origin.id = __source__.id)
          );
      };
  };
  ALTER TYPE default::Contact {
      ALTER LINK details {
          USING (SELECT
              default::Details
          FILTER
              (.origin.id = __source__.id)
          );
      };
      ALTER LINK number {
          USING (SELECT
              default::PhoneNumber
          FILTER
              (.origin.id = __source__.id)
          );
      };
  };
  ALTER TYPE default::Entity {
      ALTER LINK details {
          USING (SELECT
              default::Details
          FILTER
              (.origin.id = __source__.id)
          );
      };
  };
  ALTER TYPE default::Movement {
      ALTER LINK details {
          USING (SELECT
              default::Details
          FILTER
              (.origin.id = __source__.id)
          );
      };
  };
  ALTER TYPE default::Record {
      ALTER LINK details {
          USING (SELECT
              default::Details
          FILTER
              (.origin.id = __source__.id)
          );
      };
  };
  ALTER TYPE default::Scheduler {
      ALTER LINK details {
          USING (SELECT
              default::Details
          FILTER
              (.origin.id = __source__.id)
          );
      };
  };
};
