export const FIELD_VALUES = [
  { text: "Any Name", value: "ANY_NME" },
  { text: "First Name", value: "FIRST_NME" },
  { text: "Middle Name", value: "MIDDLE_NME" },
  { text: "Last Name", value: "LAST_NME" },
  { text: "Address", value: "ADDR_LINE_1" }
];

export const OPERATOR_VALUES = [
  { text: "Contains", value: "contains" },
  { text: "Starts With", value: "startswith" },
  { text: "Ends With", value: "endswith" },
  { text: "Exact Match", value: "exactmatch" }
];

export const RESULT_HEADERS = [
  {
    text: "Surname",
    value: "LAST_NME",
    sortable: true,
    align: "left"
  },
  {
    text: "Middle Name",
    value: "MIDDLE_NME",
    sortable: true,
    align: "left"
  },
  {
    text: "First Name",
    value: "FIRST_NME",
    sortable: false,
    align: "left"
  },
  {
    text: "Appointed",
    value: "APPOINTMENT_DT",
    sortable: false,
    align: "left"
  },
  {
    text: "Ceased",
    value: "CESSATION_DT",
    sortable: false,
    align: "left"
  },
  {
    text: "Act/Hist",
    value: "acchistory",
    sortable: false,
    align: "left"
  },
  {
    text: "Inc/Org #",
    value: "CORP_NUM",
    sortable: false,
    align: "left"
  },
  {
    text: "Company Name",
    value: "CORP_NME",
    sortable: false,
    align: "left"
  },
  {
    text: "Company Address",
    value: "ADDR_LINE_1",
    sortable: false,
    align: "left"
  }
];
