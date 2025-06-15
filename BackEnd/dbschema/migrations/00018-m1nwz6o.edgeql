CREATE MIGRATION m1nwz6ocpevuprwblptg7elqlzyubikuz5cgbyl37txvm3ylgpxuxq
    ONTO m1ldrnnnhhflhnjsqwrt67yx6rfrs5zttrg4vshxk2tl2fyrwclvza
{
  ALTER TYPE default::Contact {
      DROP LINK number;
      DROP EXTENDING default::Link;
  };
  ALTER TYPE default::Contact {
      CREATE PROPERTY number: std::json;
  };
  ALTER TYPE default::Metadata {
      DROP LINK origin;
      DROP PROPERTY field;
      DROP PROPERTY title;
  };
  DROP TYPE default::Link;
  DROP TYPE default::PhoneNumber;
  DROP TYPE default::Metadata;
};
