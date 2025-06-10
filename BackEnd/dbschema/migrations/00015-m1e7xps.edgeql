CREATE MIGRATION m1e7xpsizznrpqua2boe5fygwq6hzwrvcgmer2vunnxmy4uvdckvza
    ONTO m1ijvwgi6wkmuvvnjvzrus456egkn7wimnvtace5hjus5msqhuumxq
{
  ALTER TYPE default::Payment {
      ALTER LINK event {
          USING (std::assert_single((SELECT
              default::Scheduler
          FILTER
              (.origin = __source__)
          )));
      };
  };
};
