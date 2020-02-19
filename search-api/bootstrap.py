import datetime
from dateutil.relativedelta import *
from datetime import date
from search_api.models import (
    Corporation,
    CorpOpState,
    CorpState,
    CorpParty,
    CorpName,
    Address,
    Office,
    OfficeType,
    OfficerType,
    OfficesHeld,
    db,
)


db.session.query(Corporation).delete(synchronize_session=False)
db.session.query(CorpParty).delete(synchronize_session=False)
db.session.query(CorpName).delete(synchronize_session=False)
db.session.query(CorpOpState).delete(synchronize_session=False)
db.session.query(CorpState).delete(synchronize_session=False)
db.session.query(Address).delete(synchronize_session=False)
db.session.query(OfficeType).delete(synchronize_session=False)
db.session.query(Office).delete(synchronize_session=False)
db.session.query(OfficerType).delete(synchronize_session=False)
db.session.query(OfficesHeld).delete(synchronize_session=False)
db.session.commit()


CORP_NUMS = [
    "1234567890",
    "2345678901",
    "3456789012",
    "4567890123",
    "5678901234",
    "6789012345",
    "7890123456",
    "8901234567",
    "9112345678",
    "0223456789",
    "1334567890",
    "2445678901",
    "3556789012",
    "4667890123",
    "5778901234",
    "6889012345",
    "7990123456",
    "8001234567",
    "9312345678",
    "0423456789",
    "1534567890",
    "2645678901",
    "3756789012",
    "4867890123",
    "5978901234",
    "6089012345",
    "7490123456",
    "8501234567",
    "9612345678",
    "0723456789",
]

CORP_NAMES = [
    "Pembina Pipeline",
    "Imperial Oil",
    "Restaurant Brands International",
    "Loblaw Companies",
    "Great-West Lifeco",
    "CGI Group",
    "Telus Corporation",
    "West Wind Aviation",
    "Sun Life Financial",
    "Rogers Communications",
    "Canadian Natural Resources",
    "Nutrien",
    "Manulife Financial",
    "Newmont Goldcorp",
    "Canadian Pacific Railway",
    "Thomson Reuters",
    "Yamana Gold Inc.",
    "Barrick Gold",
    "Alimentation Couche-Tard",
    "BCE",
    "Shopify",
    "Suncor Energy",
    "Bank of Montreal",
    "TC Energy",
    "Brookfield Asset Management",
    "Husky Energy",
    "Jean Coutu Group",
    "Enbridge",
    "Fortis Inc.",
    "Royal Bank of Canada",
]

CORP_PARTY_NAMES = [
    "Lillian Black Kane",
    "Cadence Van Holden",
    "Gianni Dawson",
    "Hadley Sanford",
    "Brynlee Cantrell",
    "Nathalia Michael Marsh",
    "Bennett Luna",
    "Miah Van Kline",
    "Taniya Frey",
    "Kennedy Michael",
    "Shane Michael Nelson",
    "Kaiya Moreno",
    "Caden Lewis",
    "Celeste Van Madden",
    "Eveah Mcgee",
    "Gregory Black Marsh",
    "Alanna Frederick",
    "Jane Shepard",
    "Bernard Dunlap",
    "Skye Little",
    "Aleena Reeves",
    "Johanna Burton",
    "Iarslov Steele",
    "Mohamed Michael Poole",
    "Kira Black Harvey",
    "Jordin Van Carter",
    "Jonathon Bird",
    "Destinee Van Braun",
    "Falia Black",
    "Rigoberto Pitts",
    "Diego Monroe",
    "Gabriela Dawson",
    "Ava Richard",
    "Javier Michael Atkins",
    "Tobias Van Rose",
    "Anastasia Black Gray",
]

ADDRESSES = [
    "131 Rue Northview , Dollard-des-Ormeaux, QC, H9B 3J6",
    "106 Saint-Georges Rue , La Prairie, QC, J5R 2L9",
    "PO Box 273 , Beiseker, AB, T0M 0G0",
    "1586 Des Erables Rue , Chicoutimi, QC, G7H 5V8",
    "284 Yelverton Rd, Bethany, ON, L0A 1A0",
    "9623 83 St NW, Edmonton, AB, T6C 3A3",
    "109 Saskatchewan Blvd, Dauphin, MB, R7N 0M7",
    "6950 Champchevrier Ave , Anjou, QC, H1J 1W4",
    "20 Whitburn Cres, Nepean, ON, K2H 5K6",
    "4-310 6 Ave S , Creston, BC, V0B 1G3",
    "17944 Rue Foster, Pierrefonds, QC, H9K 1M2",
    "8 Ch Moore, Wentworth, QC, J8H 0E5",
    "127 Rue Houde , Kirkland, QC, H9J 3A8",
    "41 Mississauga Valley, Cooksville, ON, L5A 3N5",
    "10403 Av Vianney, Montréal, QC, H2B 2X7",
    "606 Victoria, Saskatoon, SK, H2B 2X7",
    "28 Helene St N, Mississauga, ON, L5G 3B7",
    "204 Ottawa St S, Kitchener, ON, N2G 3T4",
    "36 Tiffany Cres, Kanata, ON, K2K 1W2",
    "14956 58A Ave, Surrey, BC, V3S 0S4",
    "131 Rue Northview , Dollard-des-Ormeaux, QC, H9B 3J6",
    "106 Saint-Georges Rue , La Prairie, QC, J5R 2L9",
    "PO Box 273 , Beiseker, AB, T0M 0G0",
    "1586 Des Erables Rue , Chicoutimi, QC, G7H 5V8",
    "284 Yelverton Rd, Bethany, ON, L0A 1A0",
    "9623 83 St NW, Edmonton, AB, T6C 3A3",
    "109 Saskatchewan Blvd, Dauphin, MB, R7N 0M7",
    "6950 Champchevrier Ave , Anjou, QC, H1J 1W4",
    "20 Whitburn Cres, Nepean, ON, K2H 5K6",
    "4-310 6 Ave S , Creston, BC, V0B 1G3",
]


# OfficeType
office_type1 = OfficeType(
    office_typ_cd = 'BC',
    short_desc = 'BC',
    full_desc = 'BC',
)
db.session.add(office_type1)

# office_type2 = OfficeType(
#     office_typ_cd='DIR',
#     short_desc='Director',
#     full_desc='Director',
# )
# db.session.add(office_type2)

# office_type3 = OfficeType(
#     office_typ_cd='INC',
#     short_desc='Incorporator',
#     full_desc='Incorporator',
# )
# db.session.add(office_type3)

office_types = ['BC']

# OfficerType
officer_type1 = OfficerType(
    officer_typ_cd = 'SEC',
    short_desc = 'Secretary',
    full_desc = 'Secretary',
)
db.session.add(officer_type1)

officer_type2 = OfficerType(
    officer_typ_cd = 'DIR',
    short_desc = 'Director',
    full_desc = 'Director',
)
db.session.add(officer_type2)

officer_type3 = OfficerType(
    officer_typ_cd = 'INC',
    short_desc = 'Incorporator',
    full_desc = 'Incorporator',
)
db.session.add(officer_type3)

officer_types = ['SEC','DIR','INC']

#CorpOpState
corp_op_state1 = CorpOpState(
    state_typ_cd = 'AAA',
    op_state_typ_cd = 'ACT',
    short_desc = 'Act',
    full_desc = 'Active',
)
db.session.add(corp_op_state1)

corp_op_state2 = CorpOpState(
    state_typ_cd = 'HHH',
    op_state_typ_cd = 'H',
    short_desc = 'Hist',
    full_desc = 'Historical',
)
db.session.add(corp_op_state2)

corp_op_states = ['AAA','HHH']

index = 0
while index < len(CORP_NUMS):
    print(index)
    default_date = datetime.datetime.now() + datetime.timedelta(weeks=-(1+index))

    # ADDRESS
    address_array = ADDRESSES[index].split(",")
    address = Address(
        addr_id = index,
        province = address_array[2].strip(),
        postal_cd = address_array[3].strip(),
        addr_line_1 = address_array[0].strip(),
        city = address_array[1].strip(),
    )
    db.session.add(address)

    # CORPORATION
    corporation = Corporation(
        corp_num = CORP_NUMS[index],
        transition_dt = default_date,
    )
    db.session.add(corporation)

    # CORPNAME
    # corp_name1 = CorpName(
    #     corp_num = CORP_NUMS[index],
    #     corp_name_seq_num = 1,
    #     corp_nme = "OLD " + CORP_NAMES[index],
    #     end_event_id = index+1,
    # )
    # db.session.add(corp_name1)

    corp_name2 = CorpName(
        corp_num = CORP_NUMS[index],
        corp_name_seq_num = 2,
        corp_nme = CORP_NAMES[index],
    )
    db.session.add(corp_name2)

    #CORPSTATE
    corp_state = CorpState(
        corp_num = CORP_NUMS[index],
        state_typ_cd = corp_op_states[index%2],
        start_event_id = 1,
    )
    db.session.add(corp_state)

    # OFFICE
    office = Office(
        corp_num = CORP_NUMS[index],
        office_typ_cd = office_types[0],
        start_event_id = index,
        mailing_addr_id=index,
        delivery_addr_id=index,
    )
    db.session.add(office)

    # CORPPARTY
    corp_party_name = CORP_PARTY_NAMES[index].split(" ")
    appointment_date = default_date
    cessation_date = default_date

    party_types = ['FIO','DIR','OFF']

    corp_party = CorpParty(
        corp_party_id = (index),
        party_typ_cd = (party_types[index%3]),
        corp_num = CORP_NUMS[index],
        first_nme = corp_party_name[0],
        middle_nme = corp_party_name[1] if len(corp_party_name) == 3 else None,
        last_nme = corp_party_name[2] if len(corp_party_name) == 3 else corp_party_name[1],
        appointment_dt = appointment_date,
        cessation_dt = cessation_date,
        mailing_addr_id = index,
        delivery_addr_id = index,
    )
    db.session.add(corp_party)

    officer_type_base1 = officer_types[0]
    officer_type_base2 = officer_types[0]
    if index % 3 == 0:
        officer_type_base1= officer_types[0]
        officer_type_base2= officer_types[1]
    elif index % 3 == 1:
        officer_type_base1= officer_types[0]
        officer_type_base2= officer_types[2]
    elif  index % 3 == 2:
        officer_type_base1= officer_types[1]
        officer_type_base2= officer_types[2]

    # OFFICES_HELD
    offices_held1 = OfficesHeld(
        corp_party_id = index,
        officer_typ_cd = officer_type_base1,
    )
    db.session.add(offices_held1)

    offices_held2 = OfficesHeld(
        corp_party_id = index,
        officer_typ_cd = officer_type_base2,
    )
    db.session.add(offices_held2)

    index = index + 1

db.session.commit()

print("done")
