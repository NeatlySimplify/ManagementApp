use std::str::FromStr;

use crate::features::types::payment_types::Payment;
use crate::helper::JsOperation;
use chrono::{NaiveDate, ParseError};
use rust_decimal::Decimal;
use wasm_bindgen::prelude::*;

pub enum Operation {
    FilterName(String),
    FilterStatus(bool),
    FilterTypePayment(String),
    FilterByDate(NaiveDate, NaiveDate),
    FilterByValue(Option<Decimal>, Option<Decimal>),
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
            "filter_type" => {
                let type_entry: String = params[0].parse().unwrap();
                Ok(Operation::FilterTypePayment(type_entry))
            }
            "filter_by_date" => {
                let start = NaiveDate::parse_from_str(&params[0], "%Y-%m-%d").map_err(
                    |e: ParseError| JsValue::from_str(&format!("Start date error: {e}")),
                )?;
                let end = NaiveDate::parse_from_str(&params[1], "%Y-%m-%d")
                    .map_err(|e: ParseError| JsValue::from_str(&format!("End date error: {e}")))?;
                Ok(Operation::FilterByDate(start, end))
            }
            "filter_by_value" => {
                let lower = Decimal::from_str(&params[0]).ok();
                let higher = Decimal::from_str(&params[1]).ok();
                Ok(Operation::FilterByValue(lower, higher))
            }

            _ => Err(JsValue::from_str("Unknown operation")),
        }
    }

    pub fn apply(&self, records: &mut Payment) {
        match self {
            Operation::FilterName(name) => {
                records.retain(|_, entry| entry.name.contains(name));
            }
            Operation::FilterTypePayment(type_str) => {
                records.retain(|_, entry| entry.type_payment == *type_str);
            }
            Operation::FilterStatus(flag) => {
                records.retain(|_, entry| entry.status == *flag);
            }
            Operation::FilterByDate(start, end) => {
                records.retain(|_, entry| {
                    NaiveDate::parse_from_str(&entry.payment_date, "%Y-%m-%d")
                        .map(|date| date >= *start && date <= *end)
                        .unwrap_or(false)
                });
            }
            Operation::FilterByValue(lower, higher) => {
                let lower = lower.clone();
                let higher = higher.clone();

                records.retain(|_, entry| {
                    let value = Decimal::from_str(&entry.value_str).unwrap();

                    if let Some(lo) = &lower {
                        if value < *lo {
                            return false;
                        }
                    }

                    if let Some(hi) = &higher {
                        if value > *hi {
                            return false;
                        }
                    }

                    true
                });
            }
        }
    }
}

pub fn process(input: &mut Payment, operations: Vec<JsOperation>) -> Result<(), JsValue> {
    for js_op in operations {
        let op = Operation::from_str_and_params(&js_op.op, js_op.param)?;
        op.apply(input);
    }
    Ok(())
}
