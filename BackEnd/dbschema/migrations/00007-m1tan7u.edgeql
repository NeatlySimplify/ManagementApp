CREATE MIGRATION m1tan7ugi3ff4nb6dnuvdjsjdm5gmtjn5hx2lksam4zpnflgy3dv2q
    ONTO m1jpcm52ew3gkdavsw7otzamovy5x7w7nzjwxdilca3bynxlhgjtwa
{
  ALTER TYPE default::InternalUser {
      CREATE MULTI LINK payment := (.<user[IS default::Payment]);
      CREATE LINK paymente_expense := (SELECT
          __source__.movement.payment
      FILTER
          (.payment_type = 'expense')
      ORDER BY
          .payment_date DESC
      );
      CREATE LINK paymente_income := (SELECT
          __source__.movement.payment
      FILTER
          (.payment_type = 'income')
      ORDER BY
          .payment_date DESC
      );
  };
};
