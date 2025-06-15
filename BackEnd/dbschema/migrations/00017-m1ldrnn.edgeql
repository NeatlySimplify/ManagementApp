CREATE MIGRATION m1ldrnnnhhflhnjsqwrt67yx6rfrs5zttrg4vshxk2tl2fyrwclvza
    ONTO m1powmuuivi4ueip5suofhfqvgxuuwj4i7ucy72am4drusjr55a3ea
{
  ALTER TYPE default::BankAccount DROP EXTENDING default::Link;
  ALTER TYPE default::Entity DROP EXTENDING default::Link;
  ALTER TYPE default::Movement DROP EXTENDING default::Link;
  ALTER TYPE default::Scheduler DROP EXTENDING default::Link;
  ALTER TYPE default::Record DROP EXTENDING default::Link;
  ALTER TYPE default::InternalUser {
      ALTER LINK paymente_expense {
          RENAME TO payment_expense;
      };
  };
  ALTER TYPE default::InternalUser {
      ALTER LINK paymente_income {
          RENAME TO payment_income;
      };
  };
};
