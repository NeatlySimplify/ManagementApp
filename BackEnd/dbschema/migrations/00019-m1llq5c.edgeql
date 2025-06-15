CREATE MIGRATION m1llq5cmjm572htyloxboz3brmzzmrabfq2qxpso7kzx637a7qopca
    ONTO m1nwz6ocpevuprwblptg7elqlzyubikuz5cgbyl37txvm3ylgpxuxq
{
  ALTER TYPE default::InternalUser {
      CREATE PROPERTY first_access: std::bool {
          SET default := true;
      };
  };
};
