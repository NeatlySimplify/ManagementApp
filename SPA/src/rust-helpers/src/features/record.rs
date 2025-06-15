use crate::features::types::record_types::Record;
use crate::helper::JsOperation;
use wasm_bindgen::prelude::*;

pub enum Operation {
    FilterName(String),
    FilterActive(bool),
    FilterByStatus(String),
    FilterByTypeRecord(Vec<String>),
    FilterByIdService(String),
}

impl Operation {
    pub fn from_str_and_params(op: &str, params: Vec<String>) -> Result<Self, JsValue> {
        match op {
            "filter_name" => {
                let name: String = params[0].parse().unwrap();
                Ok(Operation::FilterName(name))
            }
            "filter_status" => {
                let name: String = params[0].parse().unwrap();
                Ok(Operation::FilterByStatus(name))
            }
            "filter_active" => {
                let status: bool = params[0].parse().unwrap();
                Ok(Operation::FilterActive(status))
            }
            "filter_type" => Ok(Operation::FilterByTypeRecord(params)),
            "filter_id" => {
                let id: String = params[0].parse().unwrap();
                Ok(Operation::FilterByIdService(id))
            }

            _ => Err(JsValue::from_str("Unknown operation")),
        }
    }

    pub fn apply(&self, records: &mut Record) {
        match self {
            Operation::FilterName(name) => {
                records.retain(|_, entry| entry.name.contains(name));
            }
            Operation::FilterByStatus(status) => {
                records.retain(|_, entry| entry.status == *status);
            }
            Operation::FilterActive(flag) => {
                records.retain(|_, entry| entry.active == *flag);
            }
            Operation::FilterByIdService(id) => {
                records.retain(|_, entry| entry.id_service.contains(id));
            }
            Operation::FilterByTypeRecord(type_list) => {
                records.retain(|_, entry| type_list.contains(&entry.type_record));
            }
        }
    }
}

pub fn process(input: &mut Record, operations: Vec<JsOperation>) -> Result<(), JsValue> {
    for js_op in operations {
        let op = Operation::from_str_and_params(&js_op.op, js_op.param)?;
        op.apply(input);
    }
    Ok(())
}
