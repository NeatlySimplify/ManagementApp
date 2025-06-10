CREATE MIGRATION m1o4fca67hx6fnf7zcsfbbvuyxwsottkdwestbpi4mpaxozh3nmrtq
    ONTO m1bvxeo53okdnprlkvb6oqgvvfqbf3y7tmfdf5j3caxab6e6jszu5a
{
  ALTER TYPE default::Payment {
      ALTER LINK event {
          ON SOURCE DELETE DELETE TARGET;
      };
  };
  ALTER TYPE default::Scheduler {
      ALTER LINK origin {
          ON TARGET DELETE DELETE SOURCE;
      };
  };
};
