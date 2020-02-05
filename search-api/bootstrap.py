import datetime
from dateutil.relativedelta import *
from datetime import date
from models import (
    Corporation, 
    CorpParty, 
    CorpName, 
    Address, 
    OfficerType, 
    OfficesHeld, 
    db,
)


db.session.query(Corporation).delete(synchronize_session=False)
db.session.query(CorpParty).delete(synchronize_session=False)
db.session.query(CorpName).delete(synchronize_session=False)
db.session.query(Address).delete(synchronize_session=False)
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

# OfficerType
officer_type1 = OfficerType(
    OFFICER_TYP_CD='SEC',
    SHORT_DESC='Secretary',
    FULL_DESC='Secretary',
)
db.session.add(officer_type1)

officer_type2 = OfficerType(
    OFFICER_TYP_CD='DIR',
    SHORT_DESC='Director',
    FULL_DESC='Director',
)
db.session.add(officer_type2)

officer_type3 = OfficerType(
    OFFICER_TYP_CD='INC',
    SHORT_DESC='Incorporator',
    FULL_DESC='Incorporator',
)
db.session.add(officer_type3)

officer_types = ['SEC','DIR','INC']

index = 0
while index < len(CORP_NUMS):
    
    # ADDRESS
    address_array = ADDRESSES[index].split(",")
    address = Address(
        ADDR_ID=index,
        PROVINCE=address_array[2].strip(),
        POSTAL_CD=address_array[3].strip(),
        ADDR_LINE_1=address_array[0].strip(),
        CITY=address_array[1].strip(),
    )
    db.session.add(address)
    
    # CORPORATION
    corporation = Corporation(
        CORP_NUM=CORP_NUMS[index],
    )
    db.session.add(corporation)

    # CORPPARTY
    corp_party_name = CORP_PARTY_NAMES[index].split(" ")
    appointment_date = datetime.datetime.now() + datetime.timedelta(weeks=-(1+index))
    cessation_date = appointment_date

    party_types = ['FIO','DIR','OFF']
    
    corp_party = CorpParty(
        CORP_PARTY_ID=(index),
        PARTY_TYP_CD=(party_types[index%3]),
        CORP_NUM=CORP_NUMS[index],
        FIRST_NME=corp_party_name[0],
        MIDDLE_NME=corp_party_name[1] if len(corp_party_name) == 3 else None,
        LAST_NME=corp_party_name[2] if len(corp_party_name) == 3 else corp_party_name[1],
        APPOINTMENT_DT=appointment_date,
        CESSATION_DT=cessation_date,
        MAILING_ADDR_ID=index,
    )
    db.session.add(corp_party)
    
    # CORPNAME
    corp_name = CorpName(
        CORP_NUM=CORP_NUMS[index],
        CORP_NME=CORP_NAMES[index],
    )
    db.session.add(corp_name)
    
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
        CORP_PARTY_ID=index,
        OFFICER_TYP_CD=officer_type_base1,
    )

    db.session.add(offices_held1)

    offices_held2 = OfficesHeld(
        CORP_PARTY_ID=index,
        OFFICER_TYP_CD=officer_type_base2,
    )
    db.session.add(offices_held2)

    index = index + 1

db.session.commit()

