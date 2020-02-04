import datetime
from dateutil.relativedelta import *
from datetime import date
from models import Corporation, CorpParty, CorpName, db

db.session.query(Corporation).delete(synchronize_session=False)
db.session.query(CorpParty).delete(synchronize_session=False)
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

index = 0
while index < len(CORP_NUMS):
    
    corporation = Corporation(
        CORP_NUM=CORP_NUMS[index],
    )
    db.session.add(corporation)

    corp_party_name = CORP_PARTY_NAMES[index].split(" ")
    appointment_date = datetime.datetime.now() + datetime.timedelta(weeks=-(1+index))
    cessation_date = appointment_date 
    
    corp_party = CorpParty(
        CORP_PARTY_ID=(index),
        CORP_NUM=CORP_NUMS[index],
        FIRST_NME=corp_party_name[0],
        MIDDLE_NME=corp_party_name[1] if len(corp_party_name) == 3 else None,
        LAST_NME=corp_party_name[2] if len(corp_party_name) == 3 else corp_party_name[1],
        APPOINTMENT_DT=appointment_date,
        CESSATION_DT=cessation_date,
    )
    db.session.add(corp_party)
    
    corp_name = CorpName(
        CORP_NUM=CORP_NUMS[index],
        CORP_NME=CORP_NAMES[index],
    )
    db.session.add(corp_name)

    index = index + 1

db.session.commit()

