CREATE MIGRATION m1mglgqhilg4pmspvm6pzg73beq34naljejuqycyoe3csmmemmtcga
    ONTO m137nb55j7nd7l2rmhquu6j6f7hmk7oju4kgetoxf4awiucwswlxta
{
  ALTER TYPE default::Payment {
      DROP TRIGGER update_balance_on_insert;
  };
};
