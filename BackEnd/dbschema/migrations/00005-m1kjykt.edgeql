CREATE MIGRATION m1kjyktpciwtys5bmahpr7hj4wfel722y47palyw6hhcunu3cg2nxa
    ONTO m1o4fca67hx6fnf7zcsfbbvuyxwsottkdwestbpi4mpaxozh3nmrtq
{
  ALTER TYPE default::Record {
      ALTER LINK entity {
          RESET OPTIONALITY;
      };
  };
};
