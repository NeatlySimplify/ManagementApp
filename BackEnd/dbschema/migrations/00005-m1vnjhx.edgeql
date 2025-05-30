CREATE MIGRATION m1vnjhxeat7lryf5mfzo24pskb22y6j2clqf3adxmfpoaaiejpsgha
    ONTO m1dmbobumsufs44s27ahppwgyxsp6ekfed4jirwptws4hsi37ihf3a
{
  ALTER TYPE default::UserSettings {
      ALTER PROPERTY acount_types {
          RENAME TO account_types;
      };
  };
};
