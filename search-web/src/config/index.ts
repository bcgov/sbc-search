export const BACKEND_URL = process.env.VUE_APP_BACKEND_HOST;

export const FIELD_VALUES = [
  { text: "First Name", value: "first_nme" },
  { text: "Last Name", value: "last_nme" },
  { text: "Middle Name", value: "middle_nme" },
  { text: "Any Name", value: "any_nme" },
  { text: "Street Address", value: "addr_line_1" },
  { text: "Postal Code", value: "postal_code" },
  { text: "Company Status", value: "state_typ_cd" }
];

export const OPERATOR_VALUES = [
  { text: "Contains", value: "contains" },
  { text: "Starts With", value: "startswith" },
  { text: "Ends With", value: "endswith" },
  { text: "Exact Match", value: "exact" },
  { text: "Wildcard (% or *)", value: "wildcard" }
];

export const TERM_VALUES = {
  state_typ_cd: [
    { text: "Active", value: "ACT" },
    { text: "Historical", value: "HIS" }
  ]
};

export const COMPANY_HEADERS = [
  { text: "Number", value: "corp_num" },
  { text: "Status", value: "state_typ_cd" },
  { text: "Admin Email", value: "admin_email" }
];

export const CORPORATION_HEADERS = [
  {
    text: "Inc/Reg #",
    value: "corp_num",
    sortable: true,
    align: "left"
  },
  {
    text: "Entity Type",
    value: "corp_typ_cd",
    sortable: true,
    align: "left"
  },
  {
    text: "Company Name",
    value: "corp_nme",
    sortable: true,
    align: "left"
  },
  {
    text: "Incorporated",
    value: "recognition_dts",
    sortable: true,
    align: "left"
  },
  {
    text: "Company Status",
    value: "state_typ_cd",
    sortable: true,
    align: "left"
  },
  {
    text: "Company Address",
    value: "addr",
    sortable: true,
    align: "left"
  },
  {
    text: "Postal Code",
    value: "postal_cd",
    sortable: true,
    align: "left"
  }
];

export const CORPPARTY_HEADERS = [
  {
    text: "Filing #",
    value: "corp_party_id",
    sortable: true,
    align: "left",
    width: 100
  },
  {
    text: "Surname",
    value: "last_nme",
    sortable: true,
    align: "left",
    width: 150
  },
  {
    text: "First Name",
    value: "first_nme",
    sortable: true,
    align: "left",
    width: 150
  },
  {
    text: "Middle Name",
    value: "middle_nme",
    sortable: true,
    align: "left",
    width: 150
  },
  {
    text: "Address",
    value: "addr",
    sortable: true,
    align: "left",
    width: 150
  },
  {
    text: "Postal Code",
    value: "postal_cd",
    sortable: true,
    align: "left",
    width: 150
  },
  {
    text: "Office Held",
    value: "party_typ_cd",
    sortable: true,
    align: "left",
    width: 150
  },
  {
    text: "Appointed",
    value: "appointment_dt",
    sortable: true,
    align: "left",
    width: 150
  },
  {
    text: "Ceased",
    value: "cessation_dt",
    sortable: true,
    align: "left",
    width: 150
  },
  {
    text: "Company Status",
    value: "state_typ_cd",
    sortable: true,
    align: "left",
    width: 150
  },
  {
    text: "Company Name",
    value: "corp_nme",
    sortable: true,
    align: "left",
    width: 150
  },
  {
    text: "Inc/Reg #",
    value: "corp_num",
    sortable: true,
    align: "left",
    width: 150
  },
  {
    text: "Mailing Address",
    value: "mailing_addr",
    sortable: true,
    align: "left",
    width: 150
  },
  {
    text: "Delivery Address",
    value: "delivery_addr",
    sortable: true,
    align: "left"
  },
  {
    text: "Email",
    value: "corp_party_email",
    sortable: true,
    align: "left"
  },
  {
    text: "Company Delivery Address",
    value: "corp_delivery_addr",
    sortable: true,
    align: "left"
  },
  {
    text: "Company Mailing Address",
    value: "corp_mailing_addr",
    sortable: true,
    align: "left"
  },
  {
    text: "Company Admin Email",
    value: "corp_admin_email",
    sortable: true,
    align: "left"
  },
  {
    text: "Province",
    value: "province",
    sortable: true,
    align: "left"
  },
  {
    text: "Type",
    value: "corp_typ_cd",
    sortable: true,
    align: "left"
  }
];
