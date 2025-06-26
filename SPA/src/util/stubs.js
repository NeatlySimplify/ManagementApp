import faker from "@faker/faker.js";
import getDateOffsetsISO from "./dateOffset";

const fakeAddress = () => ({
  id: faker.string.uuid(),
  state: faker.location.state(),
  city: faker.location.city(),
  district: "",
  street: "",
  number: 0,
  complement: "",
  postal: "",
});

const fakeContact = () => ({
  id: faker.string.uuid(),
  type_tag: faker.helpers.arrayElement(baseSetting.account_types),
  number: faker.phone.number(),
  extra_email: "",
  notes: {},
});

export const fakeEntity = () => ({
  id: faker.string.uuid(),
  name: faker.string.name(),
  email: faker.internet.email(),
  document: faker.helpers.fromRegExp(/[0-9]{3}.[0-9]{3}.[0-9]{3}-[0-9]{2}/),
  type_tag: faker.helpers.arrayElement(baseSetting.entity_types),
  document_type: faker.arrayElement(baseSetting.entity_document_types),
  status: faker.datatype.bolean(0.5),
  sex: faker.helpers.arrayElement(["Male", "Female"]),
  relationship_status: "",
  birth: "",
  address: faker.helpers.multiple(() => fakeAddress(), { count: 3 }),
  phone: faker.helpers.multiple(() => fakeContact(), { count: 5 }),
});
export const bulkEntities = faker.helpers.multiple(() => fakeEntity(), { count: 7 });

export const fakeRecord = (values) => ({
  id: faker.string.uuid(),
  name: faker.string.name(),
  service_id: "",
  status: true,
  type_tag: faker.helpers.arrayElement(baseSetting.record_types),
  value: faker.finance.amount({ min: 4000, max: 10000, dec: 2 }),
  entity: values,
  movement: [],
});

export const fakeScheduler = () => ({
  id: faker.string.uuid(),
  name: faker.string.name(),
  date: faker.date.anytime(),
  status: true,
  type_tag: faker.helpers.arrayElement(baseSetting.scheduler_types),
});

export const fakeBankAccount = (balance = "0") => ({
  id: faker.string.uuid(),
  bank_name: faker.word.noun(),
  account_name: faker.word.noun(),
  balance_str: balance,
});

const fakePayment = (type_tag, value, is_due) => ({
  id: faker.string.uuid(),
  type_tag: type_tag,
  value: value,
  interest: "",
  penalty: "",
  category_tag: faker.helpers.arrayElement(baseSetting.movement_income_types),
  event: {},
  payment: [],
  account: "",
  is_due: is_due,
});

export const fakeMovement = () => ({
  type_tag: "income",
  value: faker.finance.amount(),
  installment: faker.number.int({ min: 1, max: 30 }),
  payment: createPayment(faker.date.anytime(), installment, value, type_tag),
});

const createPayment = (dates, installment, value, type_tag) => {
  const dates_list = getDateOffsetsISO(
    dates,
    installment,
    faker.helpers.arrayElement(["daily", "weekly", "monthly", "yearly"]),
  );
  const value_divided = value / installment;
  const payments = dates_list.map((one_date) => fakePayment(type_tag, value_divided, one_date));
  return payments;
};

export const fakeSettings = (bank_id, record, movement, entity) => ({
  account_types: ["Conta Corrente", "Conta Poupança", "Investimentos", "Carteira"],
  default_bank_account: bank_id,
  record_title: record,
  movement_title: movement,
  entity_title: entity,
  entity_types: ["Cliente PF", "Cliente PJ", "Sócio"],
  entity_document_types: ["CPF", "CNPJ", "RG", "CNH"],
  contact_number_types: ["Casa", "Celular", "Trabalho"],
  record_types: ["Serviço"],
  record_status: ["Em Andamento", "Concluído"],
  movement_income_types: [
    "Benefícios",
    "Comissão",
    "Pagamentos",
    "Rendimentos",
    "Serviços",
    "Outros",
  ],
  movement_expense_types: [
    "Alimentação",
    "Transporte",
    "Cartão de Crédito",
    "Educação",
    "Família",
    "Lazer",
    "Moradia",
    "Pagamentos",
    "Saúde",
    "Serviços",
    "Outros",
  ],
  scheduler_types: ["Evento", "Tarefa", "Reunião"],
  movement_cycle_types: [
    "Diário",
    "Semanal",
    "Quinzenal",
    "Mensal",
    "Trimestral",
    "Semestral",
    "Anual",
    "Personalizado",
  ],
});
const baseSetting = fakeSettings();
