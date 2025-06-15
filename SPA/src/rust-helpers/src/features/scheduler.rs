use crate::features::types::scheduler_types::Scheduler;
use crate::helper::JsOperation;
use chrono::{NaiveDate, ParseError};
use wasm_bindgen::prelude::*;

pub enum Operation {
    FilterName(String),
    FilterStatus(bool),
    FilterTypeEntry(Vec<String>),
    FilterByDate(NaiveDate, NaiveDate),
}

impl Operation {
    pub fn from_str_and_params(op: &str, params: Vec<String>) -> Result<Self, JsValue> {
        match op {
            "filter_name" => {
                let name: String = params[0].parse().unwrap();
                Ok(Operation::FilterName(name))
            }
            "filter_status" => {
                let status: bool = params[0].parse().unwrap();
                Ok(Operation::FilterStatus(status))
            }
            "filter_type" => Ok(Operation::FilterTypeEntry(params)),
            "filter_by_date" => {
                let start = NaiveDate::parse_from_str(&params[0], "%Y-%m-%d").map_err(
                    |e: ParseError| JsValue::from_str(&format!("Start date error: {e}")),
                )?;
                let end = NaiveDate::parse_from_str(&params[1], "%Y-%m-%d")
                    .map_err(|e: ParseError| JsValue::from_str(&format!("End date error: {e}")))?;
                Ok(Operation::FilterByDate(start, end))
            }

            _ => Err(JsValue::from_str("Unknown operation")),
        }
    }

    pub fn apply(&self, records: &mut Scheduler) {
        match self {
            Operation::FilterName(name) => {
                records.retain(|_, entry| entry.name.contains(name));
            }
            Operation::FilterTypeEntry(type_list) => {
                records.retain(|_, entry| type_list.contains(&entry.type_entry));
            }
            Operation::FilterStatus(flag) => {
                records.retain(|_, entry| entry.status == *flag);
            }
            Operation::FilterByDate(start, end) => {
                records.retain(|_, entry| {
                    NaiveDate::parse_from_str(&entry.date, "%Y-%m-%d")
                        .map(|date| date >= *start && date <= *end)
                        .unwrap_or(false)
                });
            }
        }
    }
}

pub fn process(input: &mut Scheduler, operations: Vec<JsOperation>) -> Result<(), JsValue> {
    for js_op in operations {
        let op = Operation::from_str_and_params(&js_op.op, js_op.param)?;
        op.apply(input);
    }
    Ok(())
}
