CREATE MIGRATION m1youznodei6mzliuba5wmlq3v5yrtgdvf4dhtxjiprqvwwkinmdoq
    ONTO m1kjyktpciwtys5bmahpr7hj4wfel722y47palyw6hhcunu3cg2nxa
{
  ALTER TYPE default::Payment {
      ALTER PROPERTY interest {
          RESET default;
          SET TYPE std::str USING (<std::str>.interest);
      };
      ALTER PROPERTY penalty {
          RESET default;
          SET TYPE std::str USING (<std::str>.penalty);
      };
  };
};
