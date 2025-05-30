CREATE MIGRATION m1nwvtfvss47qugy7vonfs5ow4xzzdyonsxfwfw2v5vnoye77tq6aa
    ONTO m1kwnhhx3dy4ra6f37thm45q5s27yzk6yyc6adwrnfwcusicvjkweq
{
  ALTER TYPE default::UserSettings {
      CREATE PROPERTY movement_cycle_types: array<std::str> {
          SET default := (['Diário', 'Semanal', 'Quinzenal', 'Mensal', 'Trimestral', 'Semestral', 'Anual', 'Personalizado']);
      };
  };
};
