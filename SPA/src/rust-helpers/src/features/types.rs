pub mod scheduler_types {
    use serde::{Deserialize, Serialize};
    use std::collections::HashMap;

    #[derive(Debug, Serialize, Deserialize)]
    pub struct PartialScheduler {
        pub id: String,
        pub type_entry: String,
        pub name: String,
        pub status: bool,
        pub date: String,
    }

    pub type Scheduler = HashMap<String, PartialScheduler>;

    pub const VALID_OPS: &[&str] = &[
        "filter_name",
        "filter_status",
        "filter_type",
        "filter_by_date",
    ];
}

pub mod entity_types {
    use serde::{Deserialize, Serialize};
    use std::collections::HashMap;

    #[derive(Debug, Serialize, Deserialize)]
    pub struct PartialAddress {
        pub state: String,
        pub city: String,
    }

    #[derive(Debug, Serialize, Deserialize)]
    pub struct ParialContact {
        pub number: String,
    }

    #[derive(Debug, Serialize, Deserialize)]
    pub struct PartialEntity {
        pub id: String,
        pub name: String,
        pub email: String,
        pub govt_id: String,
        pub type_entity: String,
        pub id_type: String,
        pub status: bool,
        pub address: PartialAddress,
        pub phone: ParialContact,
    }

    pub type Entity = HashMap<String, PartialEntity>;

    pub const VALID_OPS: &[&str] = &[
        "filter_name",
        "filter_status",
        "filter_email",
        "filter_type_entity",
        "filter_gov_id",
        "filter_id_type",
        "filter_by_local",
    ];
}

pub mod payment_types {
    use serde::{Deserialize, Serialize};
    use std::collections::HashMap;

    #[derive(Debug, Serialize, Deserialize)]
    pub struct PartialPayment {
        pub id: String,
        pub name: String,
        pub type_payment: String,
        pub value_str: String,
        pub status: bool,
        pub payment_date: String,
        pub movement: String,
    }
    pub type Payment = HashMap<String, PartialPayment>;

    pub const VALID_OPS: &[&str] = &[
        "filter_name",
        "filter_status",
        "filter_email",
        "filter_type",
        "filter_by_date",
        "filter_by_value",
    ];
}

pub mod record_types {
    use serde::{Deserialize, Serialize};
    use std::collections::HashMap;

    #[derive(Debug, Serialize, Deserialize)]
    pub struct PartialRecords {
        pub id: String,
        pub type_record: String,
        pub name: String,
        pub status: String,
        pub active: bool,
        pub id_service: String,
    }

    pub type Record = HashMap<String, PartialRecords>;

    pub const VALID_OPS: &[&str] = &[
        "filter_name",
        "filter_status",
        "filter_active",
        "filter_type",
        "filter_id",
    ];
}
