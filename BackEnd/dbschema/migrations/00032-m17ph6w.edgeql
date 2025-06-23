CREATE MIGRATION m17ph6wxgp6eywz3afckvtmrzm4l5lxnhqwkwlz7qrqeah7hwrpkma
    ONTO m1iojb6pgdrpgikehgwvcyhdao23rl4mgbvtxm23qog5slsnjmbjka
{
  ALTER TYPE default::Payment {
      DROP TRIGGER insert_event;
  };
};
