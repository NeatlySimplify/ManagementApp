use serde::Deserialize;
use wasm_bindgen::JsValue;

#[derive(Deserialize)]
pub struct JsOperation {
    pub op: String,
    pub param: Vec<String>,
}

pub fn validate_operations(ops: &[JsOperation], valid_ops: &[&str]) -> Result<(), JsValue> {
    let mut seen = std::collections::HashSet::new();

    if ops.len() > valid_ops.len() {
        return Err(JsValue::from_str("Too many operations provided."));
    }

    for op in ops {
        if !valid_ops.contains(&op.op.as_str()) {
            return Err(JsValue::from_str(&format!("Invalid operation: {}", op.op)));
        }
        if !seen.insert(&op.op) {
            return Err(JsValue::from_str(&format!(
                "Duplicate operation: {}",
                op.op
            )));
        }
    }

    Ok(())
}
