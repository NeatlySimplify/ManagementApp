CREATE MIGRATION m1vdypnnqgdfe6xw2xuehnh7s6dyzyxx7hdvbouzo5se47d4ywujoq
    ONTO m17kiyx5wry4alow5xfdyucjzw5rnlvxi5insrgnixbbfdys5rlxcq
{
  ALTER TYPE default::User {
      CREATE MULTI LINK entity := (.<owner[IS default::Entity]);
  };
};
