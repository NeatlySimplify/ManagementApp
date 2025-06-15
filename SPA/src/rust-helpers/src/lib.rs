mod features;
mod helper;

use crate::helper::{JsOperation, validate_operations};
use serde_wasm_bindgen::{from_value as from_serde, to_value as to_serde};
use wasm_bindgen::prelude::*;

#[wasm_bindgen]
pub fn process_dispatcher(
    input: JsValue,
    module: String,
    params: JsValue,
) -> Result<JsValue, JsValue> {
    match module.as_str() {
        "scheduler" => {
            use features::scheduler::process;
            use features::types::scheduler_types::{Scheduler, VALID_OPS};
            let mut records: Scheduler = from_serde(input)
                .map_err(|e| JsValue::from_str(&format!("Deserialization failed: {}", e)))?;

            let ops: Vec<JsOperation> = from_serde(params)
                .map_err(|e| JsValue::from_str(&format!("Invalid operations array: {}", e)))?;

            validate_operations(&ops, &VALID_OPS)?;
            let _ = process(&mut records, ops)?;
            to_serde(&records)
                .map_err(|e| JsValue::from_str(&format!("Serialization failed: {}", e)))
        }
        "entity" => {
            use features::entity::process;
            use features::types::entity_types::{Entity, VALID_OPS};
            let mut records: Entity = from_serde(input)
                .map_err(|e| JsValue::from_str(&format!("Deserialization failed: {}", e)))?;

            let ops: Vec<JsOperation> = from_serde(params)
                .map_err(|e| JsValue::from_str(&format!("Invalid operations array: {}", e)))?;

            validate_operations(&ops, &VALID_OPS)?;

            let _ = process(&mut records, ops)?;
            to_serde(&records)
                .map_err(|e| JsValue::from_str(&format!("Serialization failed: {}", e)))
        }
        "record" => {
            use features::record::process;
            use features::types::record_types::{Record, VALID_OPS};
            let mut records: Record = from_serde(input)
                .map_err(|e| JsValue::from_str(&format!("Deserialization failed: {}", e)))?;

            let ops: Vec<JsOperation> = from_serde(params)
                .map_err(|e| JsValue::from_str(&format!("Invalid operations array: {}", e)))?;

            validate_operations(&ops, &VALID_OPS)?;
            let _ = process(&mut records, ops)?;
            to_serde(&records)
                .map_err(|e| JsValue::from_str(&format!("Serialization failed: {}", e)))
        }
        "payment" => {
            use features::payment::process;
            use features::types::payment_types::{Payment, VALID_OPS};
            let mut records: Payment = from_serde(input)
                .map_err(|e| JsValue::from_str(&format!("Deserialization failed: {}", e)))?;

            let ops: Vec<JsOperation> = from_serde(params)
                .map_err(|e| JsValue::from_str(&format!("Invalid operations array: {}", e)))?;

            validate_operations(&ops, &VALID_OPS)?;
            let _ = process(&mut records, ops)?;
            to_serde(&records)
                .map_err(|e| JsValue::from_str(&format!("Serialization failed: {}", e)))
        }
        _ => Err(input),
    }
}
