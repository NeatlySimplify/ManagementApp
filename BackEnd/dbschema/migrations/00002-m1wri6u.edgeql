CREATE MIGRATION m1wri6u6sxa2wvge7d7pepg6tspcymtykyx4lvjjiqmc6gciyfbbza
    ONTO m1zvf2nuq6jth6rlef65jt25732yywhfb4s4rnn6nl3khqc2l3wu2a
{
  ALTER TYPE default::User {
      CREATE MULTI LINK movement := (.<owner[IS default::Movement]);
      CREATE LINK payment_expense := (SELECT
          __source__.movement.payment
      FILTER
          (.type_tag = 'expense')
      ORDER BY
          .payment_date DESC
      );
      CREATE LINK payment_income := (SELECT
          __source__.movement.payment
      FILTER
          (.type_tag = 'income')
      ORDER BY
          .payment_date DESC
      );
  };
};
