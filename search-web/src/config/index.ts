export const BACKEND_URL = process.env.VUE_APP_BACKEND_HOST;

export const FIELD_VALUES = [
  { text: "First Name", value: "firstNme" },
  { text: "Last Name", value: "lastNme" },
  { text: "Middle Name", value: "middleNme" },
  { text: "Any Name", value: "anyNme" },
  { text: "Street Address", value: "addrLine1" },
  { text: "Postal Code", value: "postalCd" },
  { text: "Company Status", value: "stateTypCd" }
];

export const OPERATOR_VALUES = [
  { text: "Contains", value: "contains" },
  { text: "Starts With", value: "startswith" },
  { text: "Ends With", value: "endswith" },
  { text: "Exact Match", value: "exact" },
  { text: "Wildcard (% or *)", value: "wildcard" }
];

export const TERM_VALUES = {
  stateTypCd: [
    { text: "Active", value: "ACT" },
    { text: "Historical", value: "HIS" }
  ]
};

export const COMPANY_HEADERS = [
  { text: "Number", value: "corpNum" },
  { text: "Status", value: "stateTypCd" },
  { text: "Admin Email", value: "adminEmail" }
];

export const CORPORATION_HEADERS = [
  {
    text: "Inc/Reg #",
    value: "corpNum",
    sortable: true,
    align: "left",
    width: 150
  },
  {
    text: "Entity Type",
    value: "corpTypCd",
    sortable: true,
    align: "left",
    width: 150
  },
  {
    text: "Company Name",
    value: "corpNme",
    sortable: true,
    align: "left",
    width: 150
  },
  {
    text: "Incorporated",
    value: "recognitionDts",
    sortable: true,
    align: "left",
    width: 150
  },
  {
    text: "Company Status",
    value: "stateTypCd",
    sortable: true,
    align: "left",
    width: 150
  },
  {
    text: "Company Address",
    value: "addr",
    sortable: false,
    align: "left",
    width: 150
  },
  {
    text: "Postal Code",
    value: "postalCd",
    sortable: true,
    align: "left",
    width: 150
  }
];

export const CORPPARTY_HEADERS = [
  {
    text: "Filing #",
    value: "corpPartyId",
    sortable: true,
    align: "left",
    width: 100
  },
  {
    text: "Surname",
    value: "lastNme",
    sortable: true,
    align: "left",
    width: 150
  },
  {
    text: "First Name",
    value: "firstNme",
    sortable: true,
    align: "left",
    width: 150
  },
  {
    text: "Middle Name",
    value: "middleNme",
    sortable: true,
    align: "left",
    width: 150
  },
  {
    text: "Address",
    value: "addr",
    sortable: false,
    align: "left",
    width: 150
  },
  {
    text: "Postal Code",
    value: "postalCd",
    sortable: true,
    align: "left",
    width: 150
  },
  {
    text: "Office Held",
    value: "partyTypCd",
    sortable: true,
    align: "left",
    width: 150
  },
  {
    text: "Appointed",
    value: "appointmentDt",
    sortable: true,
    align: "left",
    width: 150
  },
  {
    text: "Ceased",
    value: "cessationDt",
    sortable: true,
    align: "left",
    width: 150
  },
  {
    text: "Company Status",
    value: "stateTypCd",
    sortable: true,
    align: "left",
    width: 150
  },
  {
    text: "Company Name",
    value: "corpNme",
    sortable: true,
    align: "left",
    width: 150
  },
  {
    text: "Inc/Reg #",
    value: "corpNum",
    sortable: true,
    align: "left",
    width: 150
  },
  {
    text: "Mailing Address",
    value: "mailingAddr",
    sortable: true,
    align: "left",
    width: 150
  },
  {
    text: "Delivery Address",
    value: "deliveryAddr",
    sortable: true,
    align: "left"
  },
  {
    text: "Email",
    value: "corpPartyEmail",
    sortable: true,
    align: "left"
  },
  {
    text: "Company Delivery Address",
    value: "corpDeliveryAddr",
    sortable: true,
    align: "left"
  },
  {
    text: "Company Mailing Address",
    value: "corpMailingAddr",
    sortable: true,
    align: "left"
  },
  {
    text: "Company Admin Email",
    value: "corpAdminEmail",
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
    value: "corpTypCd",
    sortable: true,
    align: "left"
  }
];
