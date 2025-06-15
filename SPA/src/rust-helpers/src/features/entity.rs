use crate::features::types::entity_types::Entity;
use crate::helper::JsOperation;
use wasm_bindgen::prelude::*;

pub enum Operation {
    FilterByName(String),
    FilterByStatus(bool),
    FilterByEmail(String),
    FilterByTypeEntity(Vec<String>),
    FilterByGovId(String),
    FilterByIdType(Vec<String>),
    FilterByLocal(String, String),
}

impl Operation {
    pub fn from_str_and_params(op: &str, params: Vec<String>) -> Result<Self, JsValue> {
        match op {
            "filter_name" => {
                let name: String = params[0].parse().unwrap();
                Ok(Operation::FilterByName(name))
            }
            "filter_status" => {
                let status: bool = params[0].parse().unwrap();
                Ok(Operation::FilterByStatus(status))
            }
            "filter_email" => {
                let email: String = params[0].parse().unwrap();
                Ok(Operation::FilterByEmail(email))
            }
            "filter_type_entity" => Ok(Operation::FilterByTypeEntity(params)),
            "filter_by_local" => {
                let local_type = params[0].parse().unwrap();
                let place = params[1].parse().unwrap();
                Ok(Operation::FilterByLocal(local_type, place))
            }
            "filter_id_type" => Ok(Operation::FilterByIdType(params)),
            "filter_gov_id" => {
                let id: String = params[0].parse().unwrap();
                Ok(Operation::FilterByGovId(id))
            }

            _ => Err(JsValue::from_str("Unknown operation")),
        }
    }

    pub fn apply(&self, records: &mut Entity) {
        match self {
            Operation::FilterByName(name) => {
                records.retain(|_, entry| entry.name.contains(name));
            }
            Operation::FilterByTypeEntity(type_str) => {
                records.retain(|_, entry| type_str.contains(&entry.type_entity));
            }
            Operation::FilterByStatus(flag) => {
                records.retain(|_, entry| entry.status == *flag);
            }
            Operation::FilterByEmail(email) => {
                records.retain(|_, entry| entry.email.contains(email));
            }
            Operation::FilterByGovId(document) => {
                records.retain(|_, entry| entry.govt_id.contains(document));
            }
            Operation::FilterByLocal(local_type, place) => {
                if local_type == "city" {
                    records.retain(|_, entry| entry.address.city == *place)
                } else {
                    records.retain(|_, entry| entry.address.state == *place)
                }
            }
            Operation::FilterByIdType(list_it_t) => {
                records.retain(|_, entry| list_it_t.contains(&entry.id_type));
            }
        }
    }
}

pub fn process(input: &mut Entity, operations: Vec<JsOperation>) -> Result<(), JsValue> {
    for js_op in operations {
        let op = Operation::from_str_and_params(&js_op.op, js_op.param)?;
        op.apply(input);
    }
    Ok(())
}
