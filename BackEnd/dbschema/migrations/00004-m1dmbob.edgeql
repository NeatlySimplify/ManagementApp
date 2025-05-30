CREATE MIGRATION m1dmbobumsufs44s27ahppwgyxsp6ekfed4jirwptws4hsi37ihf3a
    ONTO m1obl55dmyndkziefivs7wyid2cli47opacdlbiknp2a27ukxbymyq
{
  ALTER TYPE default::Contact {
      DROP LINK number;
  };
  ALTER TYPE default::Contact {
      CREATE PROPERTY number: std::json;
  };
  DROP TYPE default::PhoneNumber;
  ALTER TYPE default::UserSettings {
      CREATE PROPERTY contact_number_types: array<std::str> {
          SET default := (['Casa', 'Celular', 'Trabalho']);
      };
  };
};
