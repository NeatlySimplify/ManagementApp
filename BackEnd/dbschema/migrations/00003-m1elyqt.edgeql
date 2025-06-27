CREATE MIGRATION m1elyqterhm5mzc4bchgrw6svzse64eb4s5hskapsndxijphafuuiq
    ONTO m1b56qxlqsvvbyh2x2dlyulzrdb3iifm2quodpkahctphzcbfyb4oa
{
  ALTER TYPE default::Contact {
      CREATE PROPERTY complement: std::str;
      DROP PROPERTY extra_email;
  };
  ALTER TYPE default::Contact {
      DROP PROPERTY notes;
  };
  ALTER TYPE default::UserSettings {
      CREATE PROPERTY relationship_status: array<std::str> {
          SET default := (['Casado(a)', 'Viúvo(a)', 'Solteiro(a)', 'Divorciádo(a)', 'Em União Estável']);
      };
      CREATE PROPERTY sex: array<std::str> {
          SET default := (['Masculino', 'Feminino', 'Outro']);
      };
  };
};
