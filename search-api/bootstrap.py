
from models import Corporation, CorpParty, db



c = Corporation(
  CORP_NUM="1234567890"
)

db.session.add(c)

db.session.commit()
from models import Corporation, CorpParty, db

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
    "Lillian Kane",
    "Cadence Holden",
    "Gianni Dawson",
    "Hadley Sanford",
    "Brynlee Cantrell",
    "Nathalia Marsh",
    "Bennett Luna",
    "Miah Kline",
    "Taniya Frey",
    "Kennedy Michael",
    "Shane Nelson",
    "Kaiya Moreno",
    "Caden Lewis",
    "Celeste Madden",
    "Eveah Mcgee",
    "Gregory Marsh",
    "Alanna Frederick",
    "Jane Shepard",
    "Bernard Dunlap",
    "Skye Little",
    "Aleena Reeves",
    "Johanna Burton",
    "Iarslov Steele",
    "Mohamed Poole",
    "Kira Harvey",
    "Jordin Carter",
    "Jonathon Bird",
    "Destinee Braun",
    "Falia Black",
    "Rigoberto Pitts",
    "Diego Monroe",
    "Gabriela Dawson",
    "Ava Richard",
    "Javier Atkins",
    "Tobias Rose",
    "Anastasia Gray",
]

index = 0
while index < len(CORP_NUMS):
    corporation = Corporation(
        CORP_NUM=CORP_NUMS[index],
    )
    db.session.add(corporation)

    corp_party_name = CORP_PARTY_NAMES[index].split(" ")
    corp_party = CorpParty(
        CORP_PARTY_ID=(index),
        CORP_NUM=CORP_NUMS[index],
        LAST_NME=corp_party_name[0],
        FIRST_NME=corp_party_name[1],
    )
    db.session.add(corp_party)

    index = index + 1

db.session.commit()


# c = Corporation(
#   CORP_NUM="1234567890"
# )

# p = CorpParty(
#   CORP_PARTY_ID=1,
#   CORP_NUM="1234567890", # Foreign key to Corporation
# )

# db.session.add(c)

# db.session.commit()
