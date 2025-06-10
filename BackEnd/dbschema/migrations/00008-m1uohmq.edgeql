CREATE MIGRATION m1uohmq74oiafoi5eazgqnyo65koy35e7nhja3uwzfkpzm6equjw7q
    ONTO m12kqmntmjiyewnhdwfpnpyt5ug42xbpalp5c2ls4beyoiopu5atxq
{
  ALTER TYPE default::Record {
      DROP TRIGGER log_delete;
      DROP TRIGGER log_insert;
      DROP TRIGGER log_update;
  };
};
