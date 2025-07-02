CREATE MIGRATION m1invy3k4ur445w7susntfx6tao5ihlqz3p32i3kjrpguqf3veh2ga
    ONTO m1zuycqz2cfjdmxbeirxm3rabz3p5xlteb42iidug7t5ucoqv32fwq
{
  ALTER TYPE default::User {
      CREATE LINK payment := (SELECT
          __source__.movement.payment
      ORDER BY
          .payment_date DESC
      );
  };
  ALTER TYPE default::User {
      DROP LINK payment_expense;
  };
  ALTER TYPE default::User {
      DROP LINK payment_income;
  };
};
