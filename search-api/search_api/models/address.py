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
'''This model manages an Address entity.'''

from functools import reduce

from search_api.models.base import BaseModel, db


class Address(BaseModel):
    '''Address entity. Corresponds to the 'address' table.

    addr_id                   NUMBER      22     20233825
    province                  CHAR        2      18872463
    country_typ_cd            CHAR        2      19016927
    postal_cd                 VARCHAR2    15     18825296
    addr_line_1               VARCHAR2    50     16862093
    addr_line_2               VARCHAR2    50     3609613
    addr_line_3               VARCHAR2    50     482762
    city                      VARCHAR2    40     17557057
    address_format_type       VARCHAR2    10     3632701
    address_desc              VARCHAR2    300    3372387
    address_desc_short        VARCHAR2    300    3350206
    delivery_instructions     VARCHAR2    80     34510
    unit_no                   VARCHAR2    6      699964
    unit_type                 VARCHAR2    10     11488
    civic_no                  VARCHAR2    6      2210964
    civic_no_suffix           VARCHAR2    10     15768
    street_name               VARCHAR2    30     2221177
    street_type               VARCHAR2    10     2167805
    street_direction          VARCHAR2    10     292073
    lock_box_no               VARCHAR2    5      115988
    installation_type         VARCHAR2    10     47289
    installation_name         VARCHAR2    30     47036
    installation_qualifier    VARCHAR2    15     69
    route_service_type        VARCHAR2    10     146477
    route_service_no          VARCHAR2    4      27530
    province_state_name       VARCHAR2    30     362
    '''

    __tablename__ = 'address'

    addr_id = db.Column(db.Integer, primary_key=True)
    province = db.Column(db.String(2))
    country_typ_cd = db.Column(db.String(2))
    postal_cd = db.Column(db.String(15))
    addr_line_1 = db.Column(db.String(50))
    addr_line_2 = db.Column(db.String(50))
    addr_line_3 = db.Column(db.String(50))
    city = db.Column(db.String(40))
    address_format_type = db.Column(db.String(10))
    address_desc = db.Column(db.String(300))
    address_desc_short = db.Column(db.String(300))
    delivery_instructions = db.Column(db.String(80))
    unit_no = db.Column(db.String(6))
    unit_type = db.Column(db.String(10))
    civic_no = db.Column(db.String(6))
    civic_no_suffix = db.Column(db.String(10))
    street_name = db.Column(db.String(30))
    street_type = db.Column(db.String(10))
    street_direction = db.Column(db.String(10))
    lock_box_no = db.Column(db.String(5))
    installation_type = db.Column(db.String(10))
    installation_name = db.Column(db.String(30))
    installation_qualifier = db.Column(db.String(15))
    route_service_type = db.Column(db.String(10))
    route_service_no = db.Column(db.String(4))
    province_state_name = db.Column(db.String(30))

    @staticmethod
    def get_address_by_id(address_id):
        '''Get an Address by id.'''
        return Address.query.filter(Address.addr_id == address_id).add_columns(
            Address.addr_line_1,
            Address.addr_line_2,
            Address.addr_line_3,
            Address.postal_cd,
            Address.city,
            Address.province,
            Address.country_typ_cd,
        ).one()[0]

    @staticmethod
    def normalize_addr(address_id):
        '''Merge Address fields into a standardized format of street address, city, province, and postal code.'''
        if not address_id:
            return ''

        address = Address.get_address_by_id(address_id)

        def address_reducer(accumulator, address_field):
            if address_field:
                return ((accumulator or '') + ', ' if accumulator else '') + (address_field or '')
            return accumulator or ''

        return reduce(
            address_reducer, [address.addr_line_1, address.addr_line_2, address.addr_line_3,
                              address.city, address.province, address.country_typ_cd])
