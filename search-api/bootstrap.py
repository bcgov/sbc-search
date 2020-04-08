# Copyright © 2020 Province of British Columbia
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import datetime
from search_api.models.base import db
from search_api.models.corporation import Corporation
from search_api.models.corp_op_state import CorpOpState
from search_api.models.corp_state import CorpState
from search_api.models.corp_party import CorpParty
from search_api.models.corp_name import CorpName
from search_api.models.address import Address
from search_api.models.office import Office
from search_api.models.office_type import OfficeType
from search_api.models.officer_type import OfficerType
from search_api.models.offices_held import OfficesHeld
from search_api.models.event import Event
from search_api.models.filing import Filing
from search_api.models.filing_type import FilingType


def reset():

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
    db.session.query(Event).delete(synchronize_session=False)
    db.session.query(Filing).delete(synchronize_session=False)
    db.session.query(FilingType).delete(synchronize_session=False)
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
    "abc PATTERSON",
    "abc Patterson",
    "abc PATTRERSON",
    "abc PATTISON",
    "abc Patten",
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

CORP_TYP_CDS = [
    "A",
    "B",
    "BC",
    "C",
    "CC",
    "CCC",
    "CP",
    "CS",
    "CUL",
    "EPR",
    "FOR",
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

def populate():
    office_type1 = OfficeType(
        office_typ_cd='BC',
        short_desc='BC',
        full_desc='BC',
    )
    db.session.add(office_type1)

    office_types = ['BC']

    # OfficerType
    officer_type1 = OfficerType(
        officer_typ_cd='SEC',
        short_desc='Secretary',
        full_desc='Secretary',
    )
    db.session.add(officer_type1)

    officer_type2 = OfficerType(
        officer_typ_cd='DIR',
        short_desc='Director',
        full_desc='Director',
    )
    db.session.add(officer_type2)

    officer_type3 = OfficerType(
        officer_typ_cd='INC',
        short_desc='Incorporator',
        full_desc='Incorporator',
    )
    db.session.add(officer_type3)

    officer_types = ['SEC', 'DIR', 'INC']

    # CorpOpState
    corp_op_state1 = CorpOpState(
        state_typ_cd='ACT',
        op_state_typ_cd='ACT',
        short_desc='Act',
        full_desc='Active',
    )
    db.session.add(corp_op_state1)

    corp_op_state2 = CorpOpState(
        state_typ_cd='HIS',
        op_state_typ_cd='H',
        short_desc='Hist',
        full_desc='Historical',
    )
    db.session.add(corp_op_state2)

    corp_op_states = ['ACT', 'HIS']

    # FilingType
    filing_types = [
        {
            "filing_typ_cd": "ANNBC",
            "filing_typ_class": "FILING",
            "short_desc": "File an Annual Report - BC Company",
            "full_desc": "BC Annual Report"
        },
        {
            "filing_typ_cd": "TILHO",
            "filing_typ_class": "FILING",
            "short_desc": "Change TILMA HO",
            "full_desc": "Change of Head Office (NWPTA)"
        },
        {
            "filing_typ_cd": "NOCAS",
            "filing_typ_class": "SOCFIL",
            "short_desc": "Notice of Change of Address",
            "full_desc": "Notice of Change of Address"
        },
        {
            "filing_typ_cd": "COGS1",
            "filing_typ_class": "FILING",
            "short_desc": "Good Standing Certificate",
            "full_desc": "Certificate of Good Standing"
        },
    ]
    for filing_type in filing_types:
        db.session.add(FilingType(**filing_type))

    index = 0
    while index < len(CORP_NUMS):
        print(index)
        default_date = datetime.datetime.now() + datetime.timedelta(weeks=-(1 + index))

        # ADDRESS
        address_array = ADDRESSES[index].split(",")
        address = Address(
            addr_id=index,
            province=address_array[2].strip(),
            postal_cd=address_array[3].strip(),
            addr_line_1=address_array[0].strip(),
            city=address_array[1].strip(),
        )
        db.session.add(address)

        # CORPORATION
        corporation = Corporation(
            corp_num=CORP_NUMS[index],
            recognition_dts=default_date,
            corp_typ_cd=CORP_TYP_CDS[index % 11]
        )
        db.session.add(corporation)

        # CORPNAME
        corp_name2 = CorpName(
            corp_num=CORP_NUMS[index],
            corp_name_seq_num=2,
            corp_nme=CORP_NAMES[index],
            corp_name_typ_cd="CO"
        )
        db.session.add(corp_name2)

        # CORPSTATE
        corp_state = CorpState(
            corp_num=CORP_NUMS[index],
            state_typ_cd=corp_op_states[index % 2],
            start_event_id=1,
        )
        db.session.add(corp_state)

        # OFFICE
        office = Office(
            corp_num=CORP_NUMS[index],
            office_typ_cd=office_types[0],
            start_event_id=index,
            mailing_addr_id=index,
            delivery_addr_id=index,
        )
        db.session.add(office)

        # CORPPARTY
        corp_party_name = CORP_PARTY_NAMES[index].split(" ")
        appointment_date = default_date
        cessation_date = default_date

        party_types = ['FIO', 'DIR', 'OFF']

        corp_party = CorpParty(
            corp_party_id=(index),
            party_typ_cd=(party_types[index % 3]),
            corp_num=CORP_NUMS[index],
            first_nme=corp_party_name[0],
            middle_nme=corp_party_name[1] if len(corp_party_name) == 3 else None,
            last_nme=corp_party_name[2] if len(corp_party_name) == 3 else corp_party_name[1],
            appointment_dt=appointment_date,
            cessation_dt=cessation_date,
            mailing_addr_id=index,
            delivery_addr_id=index,
            start_event_id=index,
        )
        db.session.add(corp_party)

        # EVENT
        event = Event(
            event_id=index,
            corp_num=None,
            event_type_cd=None,
            event_timestmp=None,
            trigger_dts=None,
        )
        db.session.add(event)

        # FILING
        filing = Filing(
            event_id=index,
            filing_typ_cd=filing_types[index % 4]["filing_typ_cd"],
            effective_dt=None,
            change_dt=None,
            registration_dt=None,
            period_end_dt=None,
            accession_num=None,
            arrangement_ind=None,
            auth_sign_dt=None,
            withdrawn_event_id=None,
            ods_typ_cd=None,
            dd_event_id=None,
            access_cd=None,
            nr_num=None,
            court_appr_ind=None,
            court_order_num=None,
            agm_date=None,
            new_corp_num=None,
        )
        db.session.add(filing)

        # OFFICESHELD
        officer_type_base1 = officer_types[0]
        officer_type_base2 = officer_types[0]
        if index % 3 == 0:
            officer_type_base1 = officer_types[0]
            officer_type_base2 = officer_types[1]
        elif index % 3 == 1:
            officer_type_base1 = officer_types[0]
            officer_type_base2 = officer_types[2]
        elif index % 3 == 2:
            officer_type_base1 = officer_types[1]
            officer_type_base2 = officer_types[2]

        offices_held1 = OfficesHeld(
            corp_party_id=index,
            officer_typ_cd=officer_type_base1,
        )
        db.session.add(offices_held1)

        offices_held2 = OfficesHeld(
            corp_party_id=index,
            officer_typ_cd=officer_type_base2,
        )
        db.session.add(offices_held2)

        index = index + 1

    db.session.commit()

if __name__ == "__main__":
    from search_api import create_app
    app = create_app('testing')
    with app.app_context():
        reset()
        populate()
