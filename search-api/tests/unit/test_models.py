# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Tests for the Entity model.

Test suite to ensure that the Entity model routines are working as expected.
"""

from search_api.models import Corporation
import datetime


default_date = datetime.datetime.now() + datetime.timedelta(weeks=-1)




def test_corporation(db_session):
    """Assert that an Entity can be stored in the service."""
    corporation = Corporation(
        corp_num='BC1234567',
        recognition_dts=default_date,
        corp_typ_cd='C'
    )
    session = db_session
    session.add(corporation)
    session.commit()
    assert corporation.corp_num is not None
    assert corporation.corp_typ_cd == 'C'

